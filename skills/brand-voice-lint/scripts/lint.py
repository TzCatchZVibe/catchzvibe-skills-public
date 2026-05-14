#!/usr/bin/env python3
"""brand-voice-lint · [CLIENT] brand voice 6 规则 lint

Usage:
    echo "text" | python3 lint.py
    python3 lint.py file.txt

Output: YAML report (voice_score / violations / brand_voice_passed)
Exit code: 0 if passed, 1 if any violation
"""
import re
import sys


RULES = [
    {
        "id": 1,
        "name": "不夸大功能",
        "type": "blacklist",
        "patterns": [
            r"\bamazing\b", r"\bincredible\b", r"\brevolutionary\b",
            r"\bbest\b[^.!?]*?\bever\b", r"\b100%\b", r"\bperfect\b",
            r"一定", r"绝对", r"最强", r"完美",
        ],
        "suggest": "用具体感官替代 · 比如 'tastes like real fruit' / '比苹果汁更甜一点'",
    },
    {
        "id": 2,
        "name": "保留撕扯感",
        "type": "must_have",
        "patterns": [
            r"\bpeel", r"撕", r"剥", r"拉开", r"\bstrip\b", r"\blayer\b",
            r"\bpeelable\b", r"分层",
        ],
        "suggest": "强调 peel-able 的撕扯动作 · 例 'peel the outer layer first' / '先撕外层'",
    },
    {
        "id": 3,
        "name": "真实场景锚点",
        "type": "must_have",
        "patterns": [
            r"\bcar\b", r"\bkitchen\b", r"\boffice\b", r"\bwalk\b",
            r"\bcommute\b", r"\bdesk\b", r"\bcouch\b", r"\bdriveway\b",
            r"车", r"厨房", r"办公室", r"通勤", r"沙发", r"周二",
        ],
        "suggest": "锚定真实日常场景 · 不要 'in a magical land' / 抽象时空",
    },
    {
        "id": 4,
        "name": "第二人称",
        "type": "blacklist",
        "patterns": [
            r"\bwe\b", r"\bus\b", r"\bour\b",
            r"\bWe\b", r"\bUs\b", r"\bOur\b",
        ],
        "suggest": "用 you / your / 你 · 不要 we / us / our",
    },
    {
        "id": 5,
        "name": "不直接卖货",
        "type": "blacklist",
        "patterns": [
            r"\bbuy now\b", r"\blink in bio\b", r"\bshop now\b",
            r"立即购买", r"点击购买", r"\bDM to buy\b", r"马上买",
            r"\border now\b", r"\bget yours\b",
        ],
        "suggest": "用 'find @kozed in bio' 或 'kozed.com' 间接引导 · 不直接推",
    },
    {
        "id": 6,
        "name": "Halal 合规",
        "type": "conditional",
        "trigger": r"\bhalal\b",
        "must_pair": r"halal[\s-]?certified",
        "suggest": "'halal' 必须配 'certified' · [CLIENT] 是 Halal-certified 产品 · 写完整防误导",
    },
]


def lint(text: str) -> dict:
    """Run 6 rules against text · return YAML-shaped dict."""
    violations = []
    score = 0

    for rule in RULES:
        rid = rule["id"]
        name = rule["name"]
        suggest = rule["suggest"]

        if rule["type"] == "blacklist":
            found = []
            for pat in rule["patterns"]:
                for m in re.finditer(pat, text, re.IGNORECASE):
                    found.append({"text": m.group(), "pos": m.start()})
            if found:
                violations.append({
                    "rule": rid, "name": name,
                    "found": found[:5], "suggestion": suggest,
                })
            else:
                score += 1

        elif rule["type"] == "must_have":
            hit = any(re.search(pat, text, re.IGNORECASE) for pat in rule["patterns"])
            if hit:
                score += 1
            else:
                violations.append({
                    "rule": rid, "name": name,
                    "found": "missing required term",
                    "suggestion": suggest,
                })

        elif rule["type"] == "conditional":
            triggered = re.search(rule["trigger"], text, re.IGNORECASE)
            if triggered:
                paired = re.search(rule["must_pair"], text, re.IGNORECASE)
                if paired:
                    score += 1
                else:
                    violations.append({
                        "rule": rid, "name": name,
                        "found": f"'{triggered.group()}' without certified pair",
                        "suggestion": suggest,
                    })
            else:
                # Trigger absent → rule N/A → counts as pass (don't block)
                score += 1

    return {
        "voice_score": f"{score}/{len(RULES)}",
        "violations": violations,
        "brand_voice_passed": len(violations) == 0,
    }


def format_yaml(result: dict) -> str:
    """Output YAML-shaped string · stable across runs."""
    lines = []
    lines.append(f"voice_score: {result['voice_score']}")
    if result["violations"]:
        lines.append("violations:")
        for v in result["violations"]:
            lines.append(f"  - rule: {v['rule']}")
            lines.append(f"    name: {v['name']}")
            if isinstance(v["found"], list):
                found_strs = [f"{{text: {repr(f['text'])}, pos: {f['pos']}}}" for f in v["found"]]
                lines.append(f"    found: [{', '.join(found_strs)}]")
            else:
                lines.append(f"    found: {repr(v['found'])}")
            lines.append(f"    suggestion: {repr(v['suggestion'])}")
    else:
        lines.append("violations: []")
    lines.append(f"brand_voice_passed: {str(result['brand_voice_passed']).lower()}")
    return "\n".join(lines)


def main():
    if len(sys.argv) > 1 and sys.argv[1] not in ("-", "--stdin"):
        try:
            text = open(sys.argv[1], encoding="utf-8").read()
        except FileNotFoundError:
            print(f"Error: file not found: {sys.argv[1]}", file=sys.stderr)
            sys.exit(2)
    else:
        text = sys.stdin.read()

    result = lint(text)
    print(format_yaml(result))
    sys.exit(0 if result["brand_voice_passed"] else 1)


if __name__ == "__main__":
    main()
