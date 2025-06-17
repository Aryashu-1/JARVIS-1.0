from typing import TypedDict, Optional, List, Dict,Annotated,Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from datetime import datetime

class AgentState(TypedDict, total=False):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    sel: str
    given : str
    # General metadata
    # user_id: str
    # timestamp: datetime
    # current_task: str
    # history: List[str]

    # # Input handler data
    # raw_input: Optional[str]
    # parsed_intent: Optional[str]
    # extracted_entities: Optional[Dict[str, str]]

    # # Planner-specific
    # daily_plan: Optional[List[str]]
    # weekly_plan: Optional[Dict[str, List[str]]]

    # # Task management
    # task_list: Optional[List[Dict[str, str]]]  # [{title, status, deadline}]
    # completed_tasks: Optional[List[str]]
    # priority_tasks: Optional[List[str]]

    # # Reminders
    # reminders: Optional[List[Dict[str, str]]]  # [{message, time}]
    # next_reminder: Optional[str]

    # # Calendar
    # calendar_events: Optional[List[Dict[str, str]]]  # [{title, date, time}]
    # upcoming_event: Optional[str]

    # # Email
    # unread_emails: Optional[List[str]]
    # email_drafts: Optional[List[str]]
    # email_summary: Optional[str]

    # # Voice interaction
    # voice_input: Optional[str]
    # voice_output: Optional[str]

    # # Content generation
    # content_type: Optional[str]  # e.g., 'instagram', 'blog', 'brochure'
    # content_topic: Optional[str]
    # generated_content: Optional[str]

    # # Documents
    # document_type: Optional[str]  # e.g., 'mom', 'report'
    # document_text: Optional[str]
    # document_path: Optional[str]
