"""A chainlit client application that uses Ollama to converse.

To run this client, use `chainlit run path/to/this/app.py`.
Ollama must be running and you must have "qwen3:1.7b" installed.

Typing "/list" as your prompt will result in all available Ollama models being output.
Typing "/setmodel MODEL_NAME" as your prompt will switch the current language model to MODEL_NAME.
"""

import chainlit as cl
import ollama

OLLAMA_URL = "localhost:11434"

client = ollama.AsyncClient(OLLAMA_URL)

with open(__file__, "r") as f:
    SOURCE_CODE = f.read()


@cl.on_chat_start
async def chat_start():
    cl.user_session.set("model", "qwen3:1.7b")
    cl.user_session.set("messages", [])


@cl.on_message
async def on_message(msg: cl.Message):
    if msg.content == "/source":
        response = f"```python\n{SOURCE_CODE}\n"
    elif msg.content == "/list":
        models = (await client.list()).get("models")
        model_list = "\n".join(map(lambda x: f"- {x.model}", models))
        response = f"""### Installed Ollama Models\n{model_list}"""
    elif msg.content.startswith("/setmodel"):
        args = msg.content.split(" ")
        if len(args) != 2:
            response = "`/setmodel` takes one argument, the name of a model."
        else:
            cl.user_session.set("model", args[1])
            response = f"Now using {args[1]}"
    else:
        cl.user_session.get("messages").append(
            ollama.Message(role="user", content=msg.content)
        )
        chat_response = await client.chat(
            model=cl.user_session.get("model"),
            messages=cl.user_session.get("messages"),
        )
        cl.user_session.get("messages").append(chat_response.message)
        response = chat_response.message.content

    await cl.Message(response).send()
