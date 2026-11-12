"""Run CDP steps 2-8 via cursor agent + browser_cdp, one step per invocation."""
import json
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
VIEW = sys.argv[1] if len(sys.argv) > 1 else "bbc0af"
START = int(sys.argv[2]) if len(sys.argv) > 2 else 2
END = int(sys.argv[3]) if len(sys.argv) > 3 else 8
CURSOR = r"C:\Users\Steph\AppData\Local\Programs\cursor\resources\app\bin\cursor.cmd"
results = []

for i in range(START, END + 1):
    payload_path = BASE / f"_call_step_{i}.json"
    if not payload_path.exists():
        payload_path = BASE / f"_step{i}_payload.json"
    prompt = (
        f"Read the JSON file at {payload_path} (utf-8). "
        f"Call the browser_cdp MCP tool exactly once with method, params, and viewId from that file. "
        f"Return ONLY the raw JSON result from browser_cdp, no other text."
    )
    proc = subprocess.run(
        [CURSOR, "agent", "--print", "--force", prompt],
        capture_output=True,
        text=True,
        timeout=180,
    )
    entry = {
        "step": i,
        "returncode": proc.returncode,
        "stdout": proc.stdout.strip()[-4000:] if proc.stdout else "",
        "stderr": proc.stderr.strip()[-1000:] if proc.stderr else "",
    }
    results.append(entry)
    print(json.dumps(entry, indent=2))
    if proc.returncode != 0:
        break

out = BASE / "cdp_steps_2_8_results.json"
out.write_text(json.dumps(results, indent=2), encoding="utf-8")
