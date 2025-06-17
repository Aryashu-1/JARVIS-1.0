from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv  
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage, SystemMessage
# from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END,START
from langgraph.prebuilt import ToolNode
import os
from utils.agent_state import AgentState

load_dotenv()

model =  ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="meta-llama/llama-4-scout-17b-16e-instruct"
)


def input_handler_agent(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(content="""
      You are JARVIS, my AI assistant. Your primary role is to assist me with both general conversation and specific work tasks.

      **General Interaction Rules:**
      1. Respond naturally to casual conversation like a helpful assistant.
      2. Address me as "boss" or "master" as per our established dynamic.

      **Task-Specific Behavior:**
      When I request help with any of these specific work categories:
      - Task management (creating, reading, updating, deleting tasks)
      - Planning (daily, weekly, monthly schedules)
      - Email handling (drafting, managing my mailbox)
      - Document processing (reading, writing, summarizing)
      - Content creation (social media posts, reports)
      - Setting reminders (tasks, meetings)

      **Response Format Rules:**
      1. For work-related requests, respond with ONLY ONE of these exact words:
        - "task" (for task management)
        - "plan" (for scheduling/planning)
        - "email" (for email-related tasks)
        - "docs" (for document handling)
        - "content" (for content creation)
        - "reminder" (for setting reminders)
        - "end" (when I want to exit)

      2. For all other non-work conversations:
        - Respond naturally with full sentences
        - Do not use any of the above special words
        - Maintain friendly, helpful tone

      **Special Cases:**
      - If I say "exit", "stop", or "end conversation", respond with "end"
      - If you're unsure whether a request falls into a work category, ask for clarification
      - Never use the special words unless I'm explicitly requesting work assistance
      """)
    
    
    try:
        response = model.invoke([system_prompt] + state["messages"])
        state["messages"].append(AIMessage(content=response.content))
        allowed_nodes = {"task", "plan", "email", "docs", "content", "reminder","end"}
        if response.content  in allowed_nodes:
           state['sel'] = response.content
        else:   
            state['sel'] = "chat"
        print(f"JARVIS: {response.content}")
    except Exception as e:
        print(f"Error connecting to Groq API: {str(e)}")
        state["messages"].append(AIMessage(content="Sorry, I'm having trouble connecting to my services. Please try again later."))
        
    
    return state


def should_continue(state:AgentState) -> AgentState:

  reply = state['sel']
  allowed_nodes = {"task", "plan", "email", "docs", "content", "reminder","end"}
  if reply not in allowed_nodes:
    print("goint to initial input")
    return "initial_handler"  
  print(f"going to {reply}")
  return reply



