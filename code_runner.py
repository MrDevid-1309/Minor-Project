"""Runs student's Python code against test cases in a separate process with a timeout.
NOTE: for a real deployment use a proper sandbox (Docker / isolated service)."""
import json, os, subprocess, sys, tempfile

HARNESS = r'''
import json, sys
tests = json.loads(sys.argv[2])
ns = {}
try:
    exec(open(sys.argv[1]).read(), ns)
    fn = ns[sys.argv[3]]
except Exception as e:
    print(json.dumps({"passed": 0, "total": len(tests), "error": "Load error: " + str(e)})); sys.exit()
passed = 0; err = ""
for args, exp in tests:
    try:
        if fn(*args) == exp: passed += 1
    except Exception as e:
        err = str(e)
print(json.dumps({"passed": passed, "total": len(tests), "error": err}))
'''


def run_code(code: str, problem: dict, timeout: int = 4) -> dict:
    total = len(problem["tests"])
    if not code or not code.strip():
        return {"passed": 0, "total": total, "error": "No code submitted"}
    with tempfile.TemporaryDirectory() as d:
        user_file, harness = os.path.join(d, "user.py"), os.path.join(d, "h.py")
        open(user_file, "w").write(code)
        open(harness, "w").write(HARNESS)
        try:
            p = subprocess.run(
                [sys.executable, harness, user_file, json.dumps(problem["tests"]), problem["func"]],
                capture_output=True, text=True, timeout=timeout, cwd=d)
            return json.loads(p.stdout.strip().splitlines()[-1])
        except subprocess.TimeoutExpired:
            return {"passed": 0, "total": total, "error": "Time limit exceeded"}
        except Exception as e:
            return {"passed": 0, "total": total, "error": "Runtime error: " + str(e)[:100]}
