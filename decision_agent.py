from typing import TypedDict, Optional
from langgraph.graph import StateGraph
from langchain_core.runnables import RunnableLambda
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    temperature=0,
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    openai_api_base=os.getenv("OPENAI_BASE_URL"),
    model="gpt-4o-mini" 
 
)

class GraphState(TypedDict):
    user_query: str
    tool_output: Optional[str]
    final_answer: Optional[str]

graph = StateGraph(GraphState)

# Tool node
def call_tool(state: GraphState) -> dict:
    user_query = state["user_query"]
    response = llm.invoke(user_query)
    return {"tool_output": response.content}


def decide_next_step(state: GraphState) -> dict:
    return {
        **state,  # keep previous keys
        "final_answer": f"Finished processing: {state['tool_output']}"
    }

# Routing logic
def route(state: GraphState) -> str:
    if state["tool_output"]:
        return "decision_node"
    else:
        return "tool_node"

# Adding nodes
graph.add_node("tool_node", RunnableLambda(call_tool))
graph.add_node("decision_node", RunnableLambda(decide_next_step))

# Entry and finish points
graph.set_entry_point("tool_node")
graph.set_finish_point("decision_node")

# Conditional edge
graph.add_conditional_edges("tool_node", route)

# Compile
compiled_graph = graph.compile()

# Run
result = compiled_graph.invoke({"user_query": "Where is Islamabad located?"})
print(result)
