from dotenv import load_dotenv
from typing import TypedDict,Annotated
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langgraph.graph import add_messages
import os
from langgraph.checkpoint.postgres import PostgresSaver
from langchain_core.messages import AnyMessage,HumanMessage,ToolMessage,AIMessage
from app.prompt import MODEL_SYSTEM_PROMPT
from app.config import (GEMINI_MODEL,MODEL_PROVIDER,GROQ_MODEL,GROQ_MODEL_PROVIDER)
from langchain.agents.middleware import (PIIMiddleware,AgentMiddleware)

from app.tools.tools import tools

load_dotenv()

DB_URL=os.getenv('DB_URL')

#create state
class MessageState(TypedDict):
    messages:Annotated[list[AnyMessage],add_messages]


#model
gemini_model=init_chat_model(model=GEMINI_MODEL,model_provider=MODEL_PROVIDER)
groq_model=init_chat_model(model=GROQ_MODEL,model_provider=GROQ_MODEL_PROVIDER)

model=gemini_model.with_fallbacks([groq_model])    

#checkpointer
checkpointer_cm = PostgresSaver.from_conn_string(DB_URL)
checkpointer = checkpointer_cm.__enter__()
checkpointer.setup()

class SecurityMiddleware(AgentMiddleware):

    def before_agent(self, state,runtime):
        messages = state.get("messages", [])

        if not messages:
            return None

        last_message = messages[-1]

        if not isinstance(last_message, HumanMessage):
            return None

        content = last_message.content

        if not isinstance(content, str):
            return None

        text = content.lower().strip()

        blocked_patterns = [
            "ignore previous instructions",
            "ignore all previous instructions",
            "ignore your instructions",
            "disregard previous instructions",
            "disregard all previous instructions",
            "reveal your system prompt",
            "show me your system prompt",
            "print your system prompt",
            "what are your system instructions",
            "bypass your restrictions",
            "bypass your safety",
        ]

        for pattern in blocked_patterns:
            if pattern in text:
                raise ValueError(
                    "Request rejected by security policy."
                )

        return None


agent = create_agent(
    model=model,
    tools=tools,
    state_schema=MessageState,
    system_prompt=MODEL_SYSTEM_PROMPT,
    checkpointer=checkpointer,
    middleware=[
        SecurityMiddleware(),
        PIIMiddleware("email",strategy="redact",apply_to_input=True),PIIMiddleware(
            "credit_card",
            strategy="mask",
            apply_to_input=True,
        ),
        PIIMiddleware(
            "api_key",
            detector=r"sk-[a-zA-Z0-9]{32}",
            strategy="block",
            apply_to_input=True,
        ),
    ]
)

def test_agent(question: str, user_id: str):

    config = {
        "configurable": {
            "thread_id": user_id
        }
    }
    
    # Get previous conversation BEFORE this request
    previous_state = agent.get_state(config)
    previous_messages = previous_state.values.get(
        "messages",
        []
    )

    previous_count = len(previous_messages)

    
    # Run agent
    output = agent.invoke(
        {
            "messages": [
                HumanMessage(content=question)
            ]
        },
        config=config,
    )

    messages = output["messages"]

    
    # Only messages from THIS request
    current_messages = messages[previous_count:]

    
    # Tool outputs from THIS request
    retrieval_context = [
        message.content
        for message in current_messages
        if isinstance(message, ToolMessage)
    ]

    
    # Tools called during THIS request
    
    tools_called = []

    for message in current_messages:

        if getattr(message, "tool_calls", None):

            for tool_call in message.tool_calls:

                tools_called.append({
                    "name": tool_call["name"],
                    "args": tool_call.get("args", {}),
                })

    
    # Final response

    return {
        "answer": messages[-1].content,
        "retrieval_context": retrieval_context,
        "tools_called": tools_called,
    }



# STREAMING
def stream_agent(question: str, user_id: str):
    config = {
        "configurable": {
            "thread_id": user_id
        }
    }

    try:
        for message, metadata in agent.stream(
            {
                "messages": [
                    HumanMessage(content=question)
                ]
            },
            config=config,
            stream_mode="messages",
        ):

            if isinstance(message, ToolMessage):
                continue

            if isinstance(message, AIMessage):

                if message.tool_calls:
                    continue

                content = message.content

                if isinstance(content, str):
                    if content:
                        yield content

                elif isinstance(content, list):
                    for item in content:
                        if (
                            isinstance(item, dict)
                            and item.get("type") == "text"
                        ):
                            text = item.get("text", "")
                            if text:
                                yield text

    except ValueError as e:
        # SecurityMiddleware rejection
        yield " Request rejected by security policy."




if __name__=="__main__":
    result = test_agent(
        question="hi?",
        user_id="test-agent-222",
    )
    # print(result)
    # print(result['answer'][0]['text'])
    # print("Retrieval Context",result['retrieval_context'])
    # print("Tools Called",result['tools_called'])
    # print(result['answer'][0]['text'])
    # for chunk in stream_agent(
    #         question="hi?",
    #         user_id="test-agent-4",
    #     ):
    #         print(chunk,end="",flush=True)
 
