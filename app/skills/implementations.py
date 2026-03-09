"""Skill 具体实现（skills）。"""
from app.skills.base import Skill


class DocumentQASkill(Skill):
    name = "document_qa_skill"
    description = "面向结算文档问答，优先走文档检索。"
    required_tools = ["search_documents"]

    def build_context(self, state: dict) -> str:
        return "当问题涉及制度、术语、流程时，优先调用 search_documents。"

    def run(self, state: dict) -> dict:
        state.setdefault("used_skills", []).append(self.name)
        return state


class ProfileMemorySkill(Skill):
    name = "profile_memory_skill"
    description = "根据用户画像调整语气与语言。"
    required_tools = []

    def build_context(self, state: dict) -> str:
        profile = state.get("profile", {})
        return (
            f"用户画像：角色={profile.get('domain_role')}；"
            f"偏好语言={profile.get('preferred_language')}；"
            f"回答风格={profile.get('preferred_answer_style')}。"
        )

    def run(self, state: dict) -> dict:
        state.setdefault("used_skills", []).append(self.name)
        return state


class SettlementTermExplainerSkill(Skill):
    name = "settlement_term_explainer_skill"
    description = "当问题包含术语解释时，优先调用 MCP 术语能力。"
    required_tools = ["get_settlement_term"]

    def build_context(self, state: dict) -> str:
        return "若用户要求解释术语（如 T+1、轧差），可以调用 MCP tool:get_settlement_term。"

    def run(self, state: dict) -> dict:
        state.setdefault("used_skills", []).append(self.name)
        return state


def build_skills() -> list[Skill]:
    return [DocumentQASkill(), ProfileMemorySkill(), SettlementTermExplainerSkill()]
