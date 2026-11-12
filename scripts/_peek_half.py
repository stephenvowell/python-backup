"""Apply half step N via exact expression file - agent should CallMcpTool after each print."""
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
n = int(sys.argv[1])
expr = (BASE / f"_half_expr_{n}.txt").read_text(encoding="utf-8")
print(expr[:60], "...", "len", len(expr))
