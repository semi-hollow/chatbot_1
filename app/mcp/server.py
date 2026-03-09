"""最小 MCP Server 模块（mcp）。"""
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("settlement-mcp")

GLOSSARY = {
    "T+1": "交易日后第一个工作日进行清算或资金交收。",
    "轧差": "将应收应付在同一维度下抵消后，按净额结算。",
    "对账": "交易双方核对交易、费用与结算结果是否一致。",
}


@mcp.tool()
def get_settlement_term(term_name: str) -> str:
    """返回结算术语的简短解释。"""
    return GLOSSARY.get(term_name, f"未找到术语 {term_name} 的定义")


@mcp.resource("settlement://glossary/latest")
def get_glossary_latest() -> str:
    """返回当前术语表全文。"""
    return "\n".join([f"- {k}: {v}" for k, v in GLOSSARY.items()])


@mcp.prompt()
def explain_settlement_rule(rule_name: str, language: str = "zh-CN") -> str:
    """解释指定结算规则。"""
    if language == "en-US":
        return f"Explain settlement rule '{rule_name}' with one definition, one example, and one risk note."
    return f"请解释结算规则“{rule_name}”：给出定义、示例和风险提示。"


def run() -> None:
    mcp.run()


if __name__ == "__main__":
    run()
