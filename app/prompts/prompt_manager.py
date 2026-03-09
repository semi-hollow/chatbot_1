"""Prompt 模块（prompt）。动态加载中英文 system prompt。"""
from pathlib import Path


class PromptManager:
    def __init__(self, prompt_dir: Path) -> None:
        self.prompt_dir = prompt_dir

    def build_system_prompt(self, language: str, profile: dict, skill_context: str) -> str:
        normalized = "en-US" if language == "en-US" else "zh-CN"
        template_path = self.prompt_dir / f"{normalized}.txt"
        template = template_path.read_text(encoding="utf-8")
        return template.format(
            language=normalized,
            domain_role=profile.get("domain_role", "财务运营"),
            preferred_answer_style=profile.get("preferred_answer_style", "简洁"),
        ) + "\n\n技能上下文：\n" + skill_context
