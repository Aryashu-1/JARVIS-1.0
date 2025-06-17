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
import json
from pathlib import Path
from langgraph.prebuilt import create_react_agent
from functools import wraps




load_dotenv()

tasks: list[dict] = []

def with_task_io(tool_func):
    """Decorator to load before and save after tool execution"""
    @wraps(tool_func)
    def wrapper(*args, **kwargs):
        load_json_tasks()                      
        result = tool_func(*args, **kwargs)
        save_json_tasks()                     
        return result
    return wrapper

@tool
@with_task_io
def add_task(name: str,deadline: str, task_description: str="") -> str:
    """Adds a new task with name, description, and deadline"""
    global tasks
    task = {
        "name": name,
        "task_description": task_description,
        "deadline": deadline,
        "status": "Pending"
    }
    tasks.append(task)
    return "✅ Task added successfully."

@tool
@with_task_io
def delete_task(name: str) -> str:
    """Deletes a task by name"""
    global tasks
    tasks = [t for t in tasks if t["name"] != name]
    return "🗑️ Task deleted."

@tool
@with_task_io
def edit_task(name: str, new_description: str = "", new_deadline: str = "") -> str:
    """Edits task description and/or deadline"""
    for task in tasks:
        if task["name"] == name:
            if new_description:
                task["task_description"] = new_description
            if new_deadline:
                task["deadline"] = new_deadline
            return "✏️ Task updated."
    return "Task not found."

@tool
@with_task_io
def mark_done(name: str) -> str:
    """This tool marks the tasks as done"""
    for task in tasks:
        if task["name"] == name:
            task["status"] = "Done"
            return "✅ Task marked as done."
    return "Task not found."

@tool
@with_task_io
def display_all_tasks() -> str:
    """Displays the details of particular task"""
    if not tasks:
        return "📭 No tasks available."
    return "\n".join(
        [f"{t['name']} | {t['task_description']} | {t['deadline']} | {t['status']}" for t in tasks]
    )

@tool
@with_task_io
def display_task(task: str) -> str:
    """Displays all the tasks in the list"""
    for t in tasks:
        if t["name"] == task:
            return f"{t['name']} | {t['task_description']} | {t['deadline']} | {t['status']}"
    return "Task not found."

@tool
@with_task_io
def sort_tasks_by_deadline() -> str:
    """Sorts the Tasks based on the deadline i.e prioritize tasks"""
    global tasks
    tasks.sort(key=lambda t: t["deadline"])
    return "📋 Tasks sorted by deadline."



task_tools = [add_task,delete_task,edit_task,mark_done,display_all_tasks,display_task,sort_tasks_by_deadline]

taskModel =  ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="meta-llama/llama-4-scout-17b-16e-instruct"
)



# Get path to config.json relative to agent.py
current_dir = Path(__file__).parent  # agents/ folder
project_root = current_dir.parent    # your_project/ folder
json_path = project_root / 'data' / 'tasks.json'

# Load JSON data
def load_json_tasks():
    with open(json_path, 'r', encoding='utf-8') as file:
        global tasks
        tasks= json.load(file)

def save_json_tasks():
    with open(json_path, 'w', encoding='utf-8') as file:
        json.dump(tasks, file, indent=2)
    



tasks_agent=create_react_agent(
    model=taskModel,
    tools=task_tools,
    prompt=(
        "You are a Task Management Agent.\n\n"
        "INSTRUCTIONS:\n"
        "- Your sole responsibility is to manage TASK CRUD operations: Create, Read, Update, Delete.\n"
        "- Handle only task-related inputs and return the updated task state or requested task data.\n"
        "- Do NOT attempt to perform any external actions like calculations, research, or reminders.\n"
        "- Do NOT ask follow-up questions or engage in conversation.\n"
        "- Respond ONLY with the results of your task operation (e.g., a task list, confirmation message, updated task).\n"
        "- Once your task is complete, immediately pass the result back to the SUPERVISOR.\n"
        "- Remain stateless beyond the task context provided — do not assume memory across turns.\n"
        "- If the input is unclear or not related to tasks, return: 'Invalid input for task agent.\n"
        "- Never ask follow-up questions. Do not suggest further actions. Stop after the first response."
    ),
    name = "tasks_agent"
)







# def should_continue_tasks(state: AgentState):
#     messages = state["messages"]
#     last_message = messages[-1]

#     if isinstance(last_message, HumanMessage):
#         content = last_message.content.lower()
#         if any(exit_phrase in content for exit_phrase in [ "exit", "stop", "quit", "end"]):
#             state['sel']= "chat"
#             save_json_tasks()
#             return "end"
    
#     # If AI made tool calls, keep looping through tools
#     if isinstance(last_message, AIMessage) and last_message.tool_calls:
#         return "continue"

#     # If not explicitly ended and still interacting, continue
#     return "continue"

# # Create the tool-calling agent
# prompt = ChatPromptTemplate.from_messages([
#     ("system", "You are a helpful task assistant."),
#     ("user", "{input}"),
#      MessagesPlaceholder(variable_name="agent_scratchpad")
# ])
# task_llm_agent_core = create_tool_calling_agent(model, tools=task_tools,prompt=prompt)
# task_agent_executor = AgentExecutor(agent=task_llm_agent_core, tools=task_tools, verbose=True)

# # Step 3: Wrap agent logic in a node
# def task_llm_agent(state: AgentState) -> AgentState:
#     last_msg = state["messages"][-1]
#     print(f"\n[🧠 LLM Agent Handling]: {last_msg.content}\n")
    
#     result = task_agent_executor.invoke({"input": last_msg.content})
    
#     state["messages"].append(AIMessage(content=result["output"]))
#     return state

# def task_input_handler(state: AgentState) -> AgentState:
#     user_input = input("You (task): ")
#     state["messages"].append(HumanMessage(content=user_input))
#     return state



    
# def tasks_agent(state : AgentState) -> AgentState:
#     """Handles the CRUD and display operations of the User"""
#     state['sel'] = "tasks_agent"
#     print(f"inside tasks agent")
#     load_json_tasks()
#     print(tasks)    
    
#     return state
    
    


    

