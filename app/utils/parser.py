import json
import re
from typing import Any, Dict, List, Optional

def extract_json(text: str) -> Optional[Dict[str, Any]]:
    """Extract and parse JSON from a string, handling markdown code blocks."""
    if not text:
        return None
    
    # Check for markdown code blocks containing JSON
    json_block = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if json_block:
        target_str = json_block.group(1)
    else:
        # Look for first { to last }
        json_match = re.search(r"(\{.*\})", text, re.DOTALL)
        target_str = json_match.group(1) if json_match else text

    try:
        return json.loads(target_str)
    except json.JSONDecodeError:
        return None

def extract_code_blocks(text: str) -> List[Dict[str, str]]:
    """Extract code blocks with specified language annotations."""
    pattern = r"```(\w*)\n(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)
    blocks = []
    for lang, code in matches:
        blocks.append({
            "language": lang.strip().lower() or "text",
            "content": code.strip()
        })
    return blocks

def parse_diff_summary(diff_text: str) -> Dict[str, Any]:
    """Parse unified diff text into a summary of modified lines and files."""
    files_changed = set()
    additions = 0
    deletions = 0

    for line in diff_text.splitlines():
        if line.startswith("+++ b/"):
            files_changed.add(line[6:])
        elif line.startswith("+") and not line.startswith("+++"):
            additions += 1
        elif line.startswith("-") and not line.startswith("---"):
            deletions += 1

    return {
        "files_changed": list(files_changed),
        "additions": additions,
        "deletions": deletions
    }
