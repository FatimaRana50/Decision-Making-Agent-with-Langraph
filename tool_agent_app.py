import os
from datetime import datetime
from dotenv import load_dotenv


from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage

load_dotenv()

@tool
def get_current_datetime() -> str:
    """Get the current time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

llm = ChatOpenAI(
    temperature=0,
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    openai_api_base=os.getenv("OPENAI_BASE_URL"),
    model="gpt-4o-mini" 
 
)

llm_with_tools = llm.bind_tools([get_current_datetime])

#query="What is the current time and date?"
query="tell me a joke"
response = llm_with_tools.invoke([HumanMessage(content=query)])

if hasattr(response, "tool_calls") and response.tool_calls:
    for call in response.tool_calls:
        tool_name = call["name"]
        print(f"\nLLM decided to call the tool: {tool_name}")

        if tool_name == "get_current_datetime":
            result = get_current_datetime.invoke({})
            print(f"Tool result: {result}")
else:
    print(f"\nLLM Response: {response.content}")
