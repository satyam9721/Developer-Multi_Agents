import os
import pytest
from app.tools.calculator import calculator_tool
from app.tools.filesystem import filesystem_tool

def test_calculator_tool():
    res = calculator_tool.execute_with_policy("coder", expression="10 + 20 * 2")
    assert res["status"] == "success"
    assert res["result"] == 50.0

def test_filesystem_tool(tmp_path):
    workspace = str(tmp_path)
    file_path = "test.txt"
    content = "Hello, Multi-Agent System!"

    # Write file
    write_res = filesystem_tool.execute_with_policy(
        "coder", action="write", workspace_dir=workspace, file_path=file_path, content=content
    )
    assert write_res["status"] == "success"

    # Read file
    read_res = filesystem_tool.execute_with_policy(
        "coder", action="read", workspace_dir=workspace, file_path=file_path
    )
    assert read_res["status"] == "success"
    assert read_res["content"] == content
