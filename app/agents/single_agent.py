"""单 Agent 模块（agent）。基于 LangGraph 构建最小闭环。"""
import asyncio
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from app.tools.tool_registry import build_tools


class SettlementAgent:
    def __init__(self, llm, prompt_manager, short_memory, long_memory, skills, mcp_client, vector_store) -> None:
        self.llm = llm
        self.prompt_manager = prompt_manager
        self.short_memory = short_memory
        self.long_memory = long_memory
        self.skills = skills
        self.mcp_client = mcp_client
        self.vector_store = vector_store

    def _build_mcp_tools(self, runtime_trace: dict):
        @tool
        def mcp_get_settlement_term(term_name: str) -> str:
            """通过 MCP tool 获取结算术语解释。"""
            runtime_trace.setdefault("used_tools", []).append("mcp_get_settlement_term")
            runtime_trace.setdefault("used_mcp", {}).setdefault("tools", []).append("get_settlement_term")
            return asyncio.run(self.mcp_client.call_tool("get_settlement_term", {"term_name": term_name}))

        @tool
        def mcp_read_glossary() -> str:
            """通过 MCP resource 获取最新术语表。"""
            runtime_trace.setdefault("used_tools", []).append("mcp_read_glossary")
            runtime_trace.setdefault("used_mcp", {}).setdefault("resources", []).append("settlement://glossary/latest")
            return asyncio.run(self.mcp_client.read_resource("settlement://glossary/latest"))

        @tool
        def mcp_prompt_explain_rule(rule_name: str, language: str = "zh-CN") -> str:
            """通过 MCP prompt 获取规则解释模板。"""
            runtime_trace.setdefault("used_tools", []).append("mcp_prompt_explain_rule")
            runtime_trace.setdefault("used_mcp", {}).setdefault("prompts", []).append("explain_settlement_rule")
            return asyncio.run(
                self.mcp_client.get_prompt("explain_settlement_rule", {"rule_name": rule_name, "language": language})
            )

        return [mcp_get_settlement_term, mcp_read_glossary, mcp_prompt_explain_rule]

    def chat(self, user_id: str, session_id: str, message: str, language: str) -> dict[str, Any]:
        profile = self.long_memory.get_profile(user_id)
        runtime_trace: dict[str, Any] = {"used_tools": [], "retrieved_chunks": [], "used_mcp": {"tools": [], "resources": [], "prompts": []}}

        state = {"profile": profile, "message": message, "used_skills": []}
        skill_context = []
        for s in self.skills:
            s.run(state)
            skill_context.append(f"- {s.name}: {s.build_context(state)}")

        system_prompt = self.prompt_manager.build_system_prompt(language, profile, "\n".join(skill_context))

        base_tools = build_tools(self.vector_store, runtime_trace)
        tools = base_tools + self._build_mcp_tools(runtime_trace)
        agent = create_react_agent(self.llm, tools)

        history = self.short_memory.get_recent_messages(session_id)
        messages = [SystemMessage(content=system_prompt)]
        for item in history:
            if item["role"] == "user":
                messages.append(HumanMessage(content=item["content"]))
            else:
                messages.append(AIMessage(content=item["content"]))
        messages.append(HumanMessage(content=message))

        result = agent.invoke({"messages": messages})
        answer = result["messages"][-1].content

        self.short_memory.add_message(session_id, "user", message)
        self.short_memory.add_message(session_id, "assistant", answer)

        citations = [
            {"source_file": c["metadata"].get("source_file"), "chunk_id": c["chunk_id"]}
            for c in runtime_trace.get("retrieved_chunks", [])
        ]

        return {
            "answer": answer,
            "used_language": language,
            "citations": citations,
            "retrieved_chunks": runtime_trace.get("retrieved_chunks", []),
            "used_tools": runtime_trace.get("used_tools", []),
            "used_skills": state.get("used_skills", []),
            "used_mcp": runtime_trace.get("used_mcp", {}),
        }
