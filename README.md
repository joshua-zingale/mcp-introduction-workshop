# Model Context Protocol Workshop

This repository contains code and a slide presentation for a workshop that I gave on July the Twenty-Third, 2025, during the Data Science Fellowship Program at UC Riverside.

The lecture slides are in `presentation.pdf`.

After the lecture, begins the workshop, which will focus on building an MCP server using FastMCP and integrating the server into a provided MCP host.

## Code Setup for the Workshop

Inside `hosts/` are three [chainlit](https://docs.chainlit.io/get-started/overview) apps of differing complexity. While two of these are present only to get an idea of how chainlit works, `hosts/ollama_with_tools.py` integrates Ollama with MCP tools. This is the host to be used for this workshop. It can be run with

```bash
uv run chainlit run hosts/ollama_with_tools.py
```

Running the above command starts up a local chat interface with a language model. Using the UI, an MCP server can be connected. As the host is written to be basic, it only supports calling tools, lacking elicitation, sampling, and the calling of resources and prompts.

The host script depends on [Ollama](https://ollama.com) to work. [qwen3:4b](https://ollama.com/library/qwen3) must be installed in Ollama, which can be done with

```bash
ollama pull qwen3:4b
```

If Ollama is not already being run as a service on your machine, you can start Ollama with

```bash
ollama serve
```

Note that this could lead to two instances of Ollama running at the same time. Make sure therefore that Ollama is not running before you start it up.

To add one of the MCP servers to the host's environment, add it via the web UI for chainlit. For the Python Interpreter, click the MCP servers button in the UI and then add the MCP server by inputting the following for its command:

```bash
uv run mcp run /path/to/python_interpreter.py
```

Your LLM should now have the ability to run Python code. Try asking it a computational question.


## Your Part of the Workshop

Create a new MCP server using FastMCP called "Weather". It should have a tool that accesses the following web endpoint to get active weather alerts for California:

```
https://api.weather.gov/alerts/active/area/CA
```

To see how to write a FastMCP server, you can refer to the [documentation](https://gofastmcp.com/servers/tools) and look at the two examples in `servers/`.
`servers/poetry.py` provides a nigh minimal example of a working server.

To get weather data from the endpoint given above, use the Python `requests` library, which should be installed in the environment if you use [uv](https://docs.astral.sh/uv/guides/install-python/) to run code inside this repository's directory.

`requests.get(url)` allows you get a web response from a `url`. To extract JSON data as a Python dictionary, you can use `dictionary = requests.get(url).json()`. You will need to look at the web endpoint in a browser or within Python to see the structure of the data returned from the endpoint.

## What Is MCP?

[Model Context Protocol](https://modelcontextprotocol.io) (MCP) is a standard for communication between components in LLM-powered agentic workflows. MCP defines three main components:
- Host — e.g. IDEs, the application that uses functionality provided by MCP servers 
- Client — The process controlled by Host that manages stateful connection to MCP servers 
- Server — e.g. data retrieval or expression evaluation, a provider of some functionality available for Hosts, either locally hosted or via HTTP

MCP standardizes how these components can interact, meaning that so long as a Host implements Client protocols, any MCP server can be seamlessly integrated into the Host's ecosystem.

For more information, refer to the [official website](https://modelcontextprotocol.io/).

## Why Does MCP Matter?

Just as web standards allow any compliant browser to access any compliant website, so does MCP allow LLMs to be empowered by arbitrary data and tooling access.

To provide a commercial usecase, as it is, a company offers web endpoints for a website, that customers could shop its products, and for mobile apps, that customers moreover could shop its products. With MCP, the same company may offer an MCP endpoint, that customers (via their AI agents) could yet another way shop its products. 

For software developers, MCP is supported in IDEs like [VSCode](https://code.visualstudio.com/docs/copilot/chat/mcp-servers) and [Curser](https://docs.cursor.com/tools/mcp) and through LLM CLI interfaces like [Gemini CLI](https://github.com/google-gemini/gemini-cli) and [oterm](https://github.com/ggozad/oterm). Such tools can greatly increase productivity in writing code.

Even now, MCP being in an early stage, there exist [many MCP tools available for download](https://mcpservers.org/).
