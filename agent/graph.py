from langgraph.graph import StateGraph, END
from langchain_community.chat_models import ChatOllama
from .state import AgentState
from .prompts import SYSTEM_PROMPT
from .tools import agent_tools
from langchain_core.messages import SystemMessage, ToolMessage
from langgraph.prebuilt import ToolExecutor, ToolInvocation
import json
import logging
from config.settings import OLLAMA_HOST, MODEL_NAME

logger = logging.getLogger(__name__)

# Initialize the LLM
try:
    llm = ChatOllama(
        base_url=OLLAMA_HOST,
        model=MODEL_NAME,
        temperature=0.1
    )
    # Bind tools to the LLM
    llm_with_tools = llm.bind_tools(agent_tools)
except Exception as e:
    logger.error(f"Failed to initialize ChatOllama: {e}")
    llm_with_tools = None

tool_executor = ToolExecutor(agent_tools)

def should_continue(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1]
    
    # LangChain > 0.1 uses tool_calls attribute directly on AIMessage often, or additional_kwargs
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "continue"
    if "tool_calls" in last_message.additional_kwargs and last_message.additional_kwargs["tool_calls"]:
        return "continue"
        
    return "end"

def call_model(state: AgentState):
    messages = state["messages"]
    if not any(isinstance(m, SystemMessage) for m in messages):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + list(messages)
    
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

def call_tool(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1]
    
    tool_calls = getattr(last_message, 'tool_calls', [])
    if not tool_calls:
        tool_calls = last_message.additional_kwargs.get("tool_calls", [])
    
    tool_messages = []
    for tool_call in tool_calls:
        # Compatibility with different Langchain versions
        name = tool_call.get("name", tool_call.get("function", {}).get("name"))
        args = tool_call.get("args", {})
        if not args and "function" in tool_call and "arguments" in tool_call["function"]:
             args = json.loads(tool_call["function"]["arguments"])
        tool_call_id = tool_call.get("id")
        
        action = ToolInvocation(
            tool=name,
            tool_input=args
        )
        try:
            response = tool_executor.invoke(action)
        except Exception as e:
            response = str(e)
            
        tool_messages.append(
            ToolMessage(
                content=str(response), 
                tool_call_id=tool_call_id,
                name=name
            )
        )
    return {"messages": tool_messages}

# Define the graph
workflow = StateGraph(AgentState)

workflow.add_node("agent", call_model)
workflow.add_node("action", call_tool)

workflow.set_entry_point("agent")

workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "action",
        "end": END
    }
)

workflow.add_edge("action", "agent")

app = workflow.compile()
