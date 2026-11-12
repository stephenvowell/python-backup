"""Execute CDP steps 1-8 via sequential browser_cdp MCP calls using invoke JSON files."""
import json
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
VIEW = sys.argv[1] if len(sys.argv) > 1 else "bbc0af"
RESULTS = []

for i in range(1, 9):
    payload = json.loads((BASE / f"_invoke{i}.json").read_text(encoding="utf-8-sig"))
    prompt = (
        f"Call browser_cdp MCP tool exactly once with viewId {VIEW}, "
        f"method {json.dumps(payload['method'])}, "
        f"params {json.dumps(payload['params'])}. "
        f"Return only the raw JSON result from browser_cdp."
    )
    cmd = [
        r"C:\Users\Steph\AppData\Local\Programs\cursor\resources\app\bin\cursor.cmd",
        "agent",
        "--print",
        "--force",
        prompt,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    RESULTS.append(
        {
            "step": i,
            "returncode": proc.returncode,
            "stdout": proc.stdout[-2000:] if proc.stdout else "",
            "stderr": proc.stderr[-500:] if proc.stderr else "",
        }
    )
    if proc.returncode != 0:
        break

out = BASE / "cdp_mcp_results.json"
out.write_text(json.dumps(RESULTS, indent=2), encoding="utf-8")
print(json.dumps(RESULTS[-1] if RESULTS else {}, indent=2))
