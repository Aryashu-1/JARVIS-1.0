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

def initial_handler(state:AgentState)->AgentState:
  user_input = input("You: ")
  state["messages"].append(HumanMessage(content=user_input))
  last_msg = state["messages"][-1] if state["messages"] else None
  if isinstance(last_msg, AIMessage):
     print(f"JARVIS: {last_msg.content}")

  return state