from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv  
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage, SystemMessage
# from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
import os
from utils.agent_state import AgentState


load_dotenv()

def reminder_agent(state:AgentState) -> AgentState:
  """ This handles the reminders of the users and notify them"""
  state['sel'] = "remainders_agent"
  return state
