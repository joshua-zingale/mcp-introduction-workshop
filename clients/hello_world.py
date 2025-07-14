"""A slightly souped-up hello-world chainlit client application.

To run this client, use `chainlit run path/to/this/app.py`.
"""

import chainlit as cl

with open(__file__, "r") as f:
    SOURCE_CODE = f.read()


@cl.on_message
async def on_message(msg: cl.Message):
    if msg.content == "/source":
        response = f"```python\n{SOURCE_CODE}\n"
    else:
        response = f"You said, `{msg.content}`. I say `Hello, World!`"

    await cl.Message(response).send()
