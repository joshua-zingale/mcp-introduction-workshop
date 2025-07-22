"""A chainlit host application that uses Ollama to converse.
This is an MCP host that supports only tool calls.
Resources, sampling, elicitation, etc are not supported.

To run this MCP host, use `chainlit run path/to/this/app.py`.
Ollama must be running and you must have "qwen3:4B" installed.
"""

import mcp
import chainlit as cl
import ollama
from chainlit.mcp import McpConnection
import json

OLLAMA_URL = "localhost:11434"
OLLAMA_MODEL = "qwen3:4b"

SYSTEM_PROMPT = """You are a helpful assistant with access to a Python Interpreter. The user will ask you questions and you will answer the question by
* Deciding whether code would be useful for answer the user's question.
* If so, write code for use by the interpreter

After you get the result from the Python interpreter, relay the result to the user, explain the formula that you used in natural language, and clearly state the answer. Do NOT re-evaluate the problem or continue the thought process after obtaining the result.

* Do NOT call the same tool multiple times with the same arguments.
* Do NOT forget to use the tool tags when calling a tool.
* Do NOT double escape newlines when calling a tool. Simply use "\\n".
* When the tool provides a result use it to answer the question, do not ignore the result.
* When you say you will use a tool, use it before finishing your turn.
"""

client = ollama.AsyncClient(OLLAMA_URL)

with open(__file__, "r") as f:
    SOURCE_CODE = f.read()


def flatten(xss):
    return [x for xs in xss for x in xs]


@cl.on_mcp_connect
async def on_mcp(connection: McpConnection, session: mcp.ClientSession):
    result = await session.list_tools()
    tools = [
        {
            "type": "function",
            "function": {
                "name": t.name,
                "description": t.description,
                "parameters": t.inputSchema,
            },
        }
        for t in result.tools
    ]

    cl.user_session.get("mcp_tools")[connection.name] = tools


@cl.step(name="Checking for Tools", show_input=False)
async def get_tool_calls_if_appropriate():
    response, _ = await chat_ollama(
        chat_messages=cl.user_session.get("chat_messages")
        + [
            {
                "role": "user",
                "content": 'Did you mean to call a tool? If so, respond by calling it and with nothing else. Otherwise, respond with "No."',
            }
        ],
        think=False,
        silent=True,
    )
    await cl.context.current_step.remove()
    if response.message.tool_calls:
        return response.message.tool_calls
    else:
        return None


@cl.step(type="tool")
async def call_tool(tool_use: ollama.Message.ToolCall):
    tool_name = tool_use.function.name
    tool_input = tool_use.function.arguments

    current_step = cl.context.current_step
    current_step.name = tool_name

    # Identify which mcp is used
    mcp_tools = cl.user_session.get("mcp_tools")
    mcp_name = None

    for connection_name, tools in mcp_tools.items():
        if any(tool.get("function").get("name") == tool_name for tool in tools):
            mcp_name = connection_name
            break

    if not mcp_name:
        current_step.output = json.dumps(
            {"error": f"Tool {tool_name} not found in any MCP connection"}
        )
        return current_step.output

    mcp_session, _ = cl.context.session.mcp_sessions.get(mcp_name)

    if not mcp_session:
        current_step.output = json.dumps(
            {"error": f"MCP {mcp_name} not found in any MCP connection"}
        )
        return current_step.output

    try:
        current_step.output = await mcp_session.call_tool(tool_name, tool_input)
    except Exception as e:
        current_step.output = json.dumps({"error": str(e)})

    return current_step.output

@cl.step(name="Generating Response")
async def chat_ollama(chat_messages, think=True, silent=False):
    msg = cl.Message(content="")
    mcp_tools = cl.user_session.get("mcp_tools")
    tools = flatten([tools for _, tools in mcp_tools.items()])

    stream = await client.chat(
        messages=chat_messages,
        tools=tools,
        model=OLLAMA_MODEL,
        stream=True,
        think=None if think else False,
    )
    
    if think:
        with cl.Step(name="Thinking") as step:
            async for chunk in stream:
                if not silent:
                    await step.stream_token(chunk.message.content)

                if "</think>" in chunk.message.content:
                    break

    total_content = ""
    final_chunk = None
    async for chunk in stream:
        partial_content = chunk.message.content
        total_content += partial_content

        if not silent:
            await msg.stream_token(partial_content)
        if not chunk.done:
            final_chunk = chunk

    if not silent:
        await msg.send()

    return final_chunk, total_content


@cl.on_chat_start
async def chat_start():
    cl.user_session.set(
        "chat_messages",
        [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }
        ],
    )
    cl.user_session.set("mcp_tools", {})


@cl.on_message
async def on_message(msg: cl.Message):
    if msg.content == "/source":
        await cl.Message(f"```python\n{SOURCE_CODE}\n").send()
        return

    chat_messages = cl.user_session.get("chat_messages")
    chat_messages.append({"role": "user", "content": msg.content})

    while True:
        response, full_content = await chat_ollama(chat_messages, think=False)
        if not response:
            break

        chat_messages.append({"role": "assistant", "content": full_content})

        tool_calls = (
            response.message.tool_calls or await get_tool_calls_if_appropriate()
        )

        if tool_calls:
            tool_call = next(iter(tool_calls))
            tool_result = await call_tool(tool_call)
            chat_messages.append(
                {
                    "role": "tool_use",
                    "content": tool_call.model_dump_json()
                }
            )
            chat_messages.append(
                {
                    "role": "tool",
                    "name": tool_call.function.name,
                    "content": f"{tool_result}",
                }
            )
        else:
            break
