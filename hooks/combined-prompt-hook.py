#!/usr/bin/env python3
"""
Combined Hook for Claude Code
Chains skill-activation and orchestrator-interceptor hooks.
This ensures both hooks run on user prompt submit and combines their outputs.
"""

import sys
import json
import subprocess
from pathlib import Path


def main() -> None:
    try:
        script_dir = Path(__file__).parent.resolve()
        input_data = sys.stdin.read()
        skill_script = script_dir / "skill-activation-prompt.py"
        orchestrator_script = script_dir / "orchestrator_interceptor.py"
        skill_result = subprocess.run(
            [sys.executable, str(skill_script)],
            input=input_data,
            capture_output=True,
            text=True,
            check=False,
        )
        skill_output_json = {}
        if skill_result.returncode == 0 and skill_result.stdout:
            try:
                skill_output_json = json.loads(skill_result.stdout)
            except json.JSONDecodeError:
                print("Warning: Skill hook returned invalid JSON", file=sys.stderr)
        orchestrator_result = subprocess.run(
            [sys.executable, str(orchestrator_script)],
            input=input_data,
            capture_output=True,
            text=True,
            check=True,
        )
        orchestrator_output_json = {}
        if orchestrator_result.stdout:
            orchestrator_output_json = json.loads(orchestrator_result.stdout)
        skill_context = skill_output_json.get("hookSpecificOutput", {}).get(
            "additionalContext", ""
        )
        orchestrator_context = orchestrator_output_json.get(
            "hookSpecificOutput", {}
        ).get("additionalContext", "")
        if skill_context and orchestrator_context:
            combined_context = f"{skill_context}\n\n{orchestrator_context}"
        elif skill_context:
            combined_context = skill_context
        else:
            combined_context = orchestrator_context
        response = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": combined_context,
            }
        }
        print(json.dumps(response))
        sys.exit(0)
    except Exception as e:
        print(f"Error in combined-prompt-hook: {e}", file=sys.stderr)
        response = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": "",
            }
        }
        print(json.dumps(response))
        sys.exit(0)


if __name__ == "__main__":
    main()
