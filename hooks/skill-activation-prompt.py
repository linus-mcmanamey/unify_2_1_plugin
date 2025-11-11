#!/usr/bin/env python3
import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Literal, Optional, TypedDict


class PromptTriggers(TypedDict, total=False):
    keywords: List[str]
    intentPatterns: List[str]


class SkillRule(TypedDict):
    type: Literal["guardrail", "domain"]
    enforcement: Literal["block", "suggest", "warn"]
    priority: Literal["critical", "high", "medium", "low"]
    promptTriggers: Optional[PromptTriggers]


class SkillRules(TypedDict):
    version: str
    skills: Dict[str, SkillRule]


class HookInput(TypedDict):
    session_id: str
    transcript_path: str
    cwd: str
    permission_mode: str
    prompt: str


class MatchedSkill(TypedDict):
    name: str
    matchType: Literal["keyword", "intent"]
    config: SkillRule


def main() -> None:
    try:
        input_data = sys.stdin.read()
        data: HookInput = json.loads(input_data)
        prompt = data["prompt"].lower()
        project_dir = (
            data.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
        )
        rules_path = Path(project_dir) / ".claude" / "skills" / "skill-rules.json"
        with open(rules_path, "r", encoding="utf-8") as f:
            rules: SkillRules = json.load(f)
        matched_skills: List[MatchedSkill] = []
        for skill_name, config in rules["skills"].items():
            triggers = config.get("promptTriggers")
            if not triggers:
                continue
            keywords = triggers.get("keywords", [])
            if keywords:
                keyword_match = any(kw.lower() in prompt for kw in keywords)
                if keyword_match:
                    matched_skills.append(
                        {"name": skill_name, "matchType": "keyword", "config": config}
                    )
                    continue
            intent_patterns = triggers.get("intentPatterns", [])
            if intent_patterns:
                intent_match = any(
                    re.search(pattern, prompt, re.IGNORECASE)
                    for pattern in intent_patterns
                )
                if intent_match:
                    matched_skills.append(
                        {"name": skill_name, "matchType": "intent", "config": config}
                    )
        additional_context = ""
        if matched_skills:
            output = "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            output += "🎯 SKILL ACTIVATION CHECK\n"
            output += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            critical = [
                s for s in matched_skills if s["config"]["priority"] == "critical"
            ]
            high = [s for s in matched_skills if s["config"]["priority"] == "high"]
            medium = [s for s in matched_skills if s["config"]["priority"] == "medium"]
            low = [s for s in matched_skills if s["config"]["priority"] == "low"]
            if critical:
                output += "⚠️ CRITICAL SKILLS (REQUIRED):\n"
                for s in critical:
                    output += f"  → {s['name']}\n"
                output += "\n"
            if high:
                output += "📚 RECOMMENDED SKILLS:\n"
                for s in high:
                    output += f"  → {s['name']}\n"
                output += "\n"
            if medium:
                output += "💡 SUGGESTED SKILLS:\n"
                for s in medium:
                    output += f"  → {s['name']}\n"
                output += "\n"
            if low:
                output += "📌 OPTIONAL SKILLS:\n"
                for s in low:
                    output += f"  → {s['name']}\n"
                output += "\n"
            output += "ACTION: Use Skill tool BEFORE responding\n"
            output += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            additional_context = output
        response = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": additional_context,
            }
        }
        print(json.dumps(response))
        sys.exit(0)
    except Exception as err:
        print(f"Error in skill-activation-prompt hook: {err}", file=sys.stderr)
        response = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": "",
            }
        }
        print(json.dumps(response))
        sys.exit(0)


if __name__ == "__main__":
    import os

    main()
