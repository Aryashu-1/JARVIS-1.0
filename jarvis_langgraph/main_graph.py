from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv  
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage, SystemMessage
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode
import os

from utils.agent_state import AgentState
from agents.initial_handler import initial_handler
from agents.input_handler_agent import input_handler_agent, should_continue
from agents.content_gen_agent import content_gen_agent
from agents.document_agent import document_agent
from agents.email_agent import email_agent
from agents.planner_agent import planner_agent
from agents.reminder_agent import reminder_agent
from agents.tasks_agent import tasks_react_agent
from agents.researcher_agent import research_agent
from langchain_core.messages import AIMessage
from IPython.display import Image, display
from utils.message_print import pretty_print_messages
from utils.groq_model import groq_model
from langgraph_supervisor import create_supervisor
from langchain.chat_models import init_chat_model

load_dotenv()

# # Step 1: Create the model
# model = ChatGroq(
#     groq_api_key=os.getenv("GROQ_API_KEY"),
#     model_name="meta-llama/llama-4-scout-17b-16e-instruct"
# )
supervisor = create_supervisor(
    model=groq_model,
    agents=[research_agent, tasks_react_agent],
    prompt=(
        "You are a supervisor managing two agents:\n"
        "- a research agent. Assign research-related tasks to this agent\n"
        "- a math agent. Assign math-related tasks to this agent\n"
        "Assign work to one agent at a time, do not call agents in parallel.\n"
        "Do not do any work yourself."
    ),
    add_handoff_back_messages=True,
    output_mode="full_history",
).compile()


with open("graph.png", "wb") as f:
    f.write(supervisor.get_graph().draw_mermaid_png())
print("✅ Graph saved as graph.png")


for chunk in supervisor.stream(
    {
        "messages": [
            
            {
                "role":"user",
                "content":"display my tasks"
            }
        ]
    },
):
    pretty_print_messages(chunk, last_message=True)

final_message_history = chunk["supervisor"]["messages"]




# # Step 4: Define and wire the LangGraph
# main_graph = StateGraph(AgentState)

# # --- Main nodes ---
# main_graph.add_node("initial_handler", initial_handler)
# main_graph.add_node("input_handler", input_handler_agent)
# main_graph.add_node("task_manager", tasks_agent)
# main_graph.add_node("planner", planner_agent)
# main_graph.add_node("email", email_agent)
# main_graph.add_node("docs", document_agent)
# main_graph.add_node("content", content_gen_agent)
# main_graph.add_node("reminder", reminder_agent)

# # --- Task-specific loop nodes ---
# main_graph.add_node("task_input", task_input_handler)
# main_graph.add_node("task_llm_agent", task_llm_agent)
# main_graph.add_node("task_tools", ToolNode(tools=task_tools))

# # --- Initial Routing ---
# main_graph.add_edge(START, "initial_handler")
# main_graph.add_edge("initial_handler", "input_handler")
# main_graph.add_conditional_edges(
#     "input_handler",
#     should_continue,
#     {
#         "task": "task_manager",
#         "plan": "planner",
#         "email": "email",
#         "docs": "docs",
#         "content": "content",
#         "reminder": "reminder",
#         "initial_handler": "initial_handler",
#         "end": END,
#     }
# )

# # --- Task Agent Loop ---
# main_graph.add_edge("task_manager", "task_input")
# main_graph.add_edge("task_input", "task_llm_agent")
# main_graph.add_edge("task_llm_agent", "task_tools")
# main_graph.add_edge("task_tools", "task_manager")

# # --- End conditions for task loop ---
# main_graph.add_conditional_edges(
#     "task_manager",
#     should_continue_tasks,
#     {
#         "continue": "task_input",
#         "end": END
#     }
# )

# # --- End for other domains ---
# for node in ["planner", "email", "docs", "content", "reminder"]:
#     main_graph.add_edge(node, END)

# # Step 5: Compile and visualize
# main_graph_app = main_graph.compile()

# with open("graph.png", "wb") as f:
#     f.write(main_graph_app.get_graph().draw_mermaid_png())
# print("✅ Graph saved as graph.png")

# # Step 6: Run the graph
# state: AgentState = {}
# state = main_graph_app.invoke(state)
# print("\nFinal State:\n", state)