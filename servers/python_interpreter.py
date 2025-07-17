from mcp.server.fastmcp import FastMCP
from io import StringIO
from contextlib import redirect_stdout
import mcp
from typing import (
    Mapping,
    Sequence,
)


mcp = FastMCP("Python Interpreter")

@mcp.tool()
def evaluate_expression(expression: str) -> str:
    """Evlauates a single Python expression and returns the output as a string.
    `import math` has already been run, so you can use its functions like `math.sqrt` or `math.sin`.
    """
    import math

    raise_if_unsafe_code(expression)
    
    return str(eval(expression, globals={"math": math}))


@mcp.tool()
def execute_code(python_source: str) -> str:
    """Call this to execute Python source code and get back the standard output.
    Only the standard library and requests are available for import.

    Args:
        python_source: The Python source code to be executed.
            Note: You must use print statements to get any return values back.

    Returns:
        str: The standard output of the evaluated sourcecode.
    """
    output_string = StringIO()
    locals = dict()
    with redirect_stdout(output_string):
        exec(python_source, globals=safe_builtins, locals=locals)
    
    output_string = output_string.getvalue()
    if len(output_string) == "":
        return str(locals)
    return output_string


def raise_if_unsafe_code(python_source: str):
    """Raises an error if the Python source is not safe to execute.

    Args:
        python_source (str): The Python source code to be checked.

    Raises:
        ValueError: If "open" or "import" is present in the source code.
    """
    if "open" in python_source:
        raise ValueError("Cannot use `open`")


def safe_import(
        name: str,
        globals: Mapping[str, object] | None = None,
        locals: Mapping[str, object] | None = None,
        fromlist: Sequence[str] = (),
        level: int = 0):
    allowable_imports = ["math", "datetime"]
    if name not in allowable_imports:
        raise ImportError(f"{name} is not a valid import module. Must be one of {allowable_imports}.")
    return __import__(name, globals, locals, fromlist, level)


builtins = dir(__builtins__)

safe_builtins = {
    builtin: getattr(__builtins__, builtin) for builtin in dir(__builtins__) if builtin not in ["open"]
}

safe_builtins["__import__"] = safe_import