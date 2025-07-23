# Model Context Protocol Workshop

This repository contains code and a slide presentation for a workshop that I gave on July the Twenty-Third, 2025, during the Data Science Fellowship Program at UC Riverside.


## Code

Inside `hosts/` are three [chainlit](https://docs.chainlit.io/get-started/overview) apps of differing complexity. `hosts/ollama_with_tools.py` can be run with

```bash
uv run chainlit run hosts/ollama_with_tools.py
```

This starts up a local chat interface with a language model. Using the UI, an MCP server can be connected. As the host is written to be basic, it only supports calling tools, lacking elicitation, sampling, or the calling of resources.

The host script depends on [Ollama](https://ollama.com) to work. [qwen3:4b](https://ollama.com/library/qwen3) must be installed in Ollama.

To add one of the MCP servers to the Host's environment, add it via the web UI for chainlit. For the Python Interpreter, click the MCP servers button in the UI and then add the MCP server by inputting the following for its command:

```bash
uv run mcp run /path/to/python_interpreter.py
```

Your LLM should now have the ability to run Python code. Try asking it a computational question.


## Workshop

Create a new MCP server using FastMCP called "Weather". It should have a tool that accesses the following web endpoint to get active weather alerts for California:
```
https://api.weather.gov/alerts/active/area/CA
```


## What Is MCP?

[Model Context Protocol](https://modelcontextprotocol.io) (MCP) is a standard for communication between components in LLM-powered agentic workflows. MCP defines three main components:
- Host — e.g. IDEs, the application that uses functionality provided by MCP servers 
- Client — The process controled by Host that manages stateful connection to MCP servers 
- Server — e.g. data retrieval or expression evaluation, a provider of some functionality available for Hosts, either locally hosted or via HTTP

MCP standardizes how these components can interact, meaning that so long as a Host implements Client protocols, any MCP server can be seamlessly integrated into the Host's ecosystem.

For more information, refer to the [official website](https://modelcontextprotocol.io/).

## Why Does MCP Matter?

Just as web standards allow any complient browser to access any complient website, so does MCP allow LLMs to be empowered by arbitrary data and tooling access. To provide a comercial usecase, as it is, a company offers web endpoints for a website, that customers could shop its products, and for mobile apps, that customers moreover could shop its products. With MCP, the same company may offer an MCP endpoint, that customers (via their AI agents) could yet another way shop its products. 

Even now, MCP being in an early stage, there exist [many MCP tools available for download](https://mcpservers.org/).
