from mcp.server.fastmcp import FastMCP


mcp = FastMCP("Poetry")


@mcp.tool()
def write_poem(topic: str) -> str:
    """Call this to get a poem about a topic

    Args:
        topic: The topic about which the poem should be written.

    Returns:
        str: The poem.
    """
    return f"I love {topic},\n{topic} may love me\nBut well do I know that never shall {topic} forsake {topic}."
