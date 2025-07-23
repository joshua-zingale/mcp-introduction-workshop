from mcp.server.fastmcp import FastMCP
from io import StringIO
from contextlib import redirect_stdout
from typing import (
    Mapping,
    Sequence,
)


mcp = FastMCP("Python Interpreter")


@mcp.tool()
def execute_code(python_source: str) -> str:
    """Call this to execute Python source code and get back the standard output.
    Only math, datetime, and requests are available for import.

    Args:
        python_source: The Python source code to be executed.
            Note: You must use print statements to get any return values back.

    Returns:
        str: The standard output of the evaluated sourcecode.
    """
    output_string = StringIO()

    exec_globals = safe_builtins.copy()
    exec_locals = dict()
    with redirect_stdout(output_string):
        exec(python_source, globals=exec_globals, locals=exec_locals)

    output_string = output_string.getvalue()
    if len(output_string) == 0:
        raise ValueError("No output. Hint: Did you forget to use a print statement?")
    return output_string


def safe_import(
    name: str,
    globals: Mapping[str, object] | None = None,
    locals: Mapping[str, object] | None = None,
    fromlist: Sequence[str] = (),
    level: int = 0,
):
    allowable_imports = ["math", "datetime", "requests"]
    if name not in allowable_imports:
        raise ImportError(
            f"{name} is not a valid import module. Must be one of {allowable_imports}."
        )
    module = __import__(name, globals, locals, fromlist, level)
    globals[name] = module
    return module


builtins = dir(__builtins__)

safe_builtins = {
    builtin: getattr(__builtins__, builtin)
    for builtin in dir(__builtins__)
    if builtin not in ["open"]
}

safe_builtins["__import__"] = safe_import
import math
import datetime
import requests

safe_builtins["math"] = math
safe_builtins["datetime"] = datetime
safe_builtins["requests"] = requests
