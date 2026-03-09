# 结算文档 AI 问答助手（第一阶段最小可用 Demo）

> 目标：提供一个可运行、可讲解、可扩展的企业内部结算文档问答助手最小闭环。  
> 第一阶段只实现 AI 核心闭环；第二阶段能力请见 `docs/phase2_backlog.md`。

## 1. 项目结构树

```text
.
├── app
│   ├── agents              # agent
│   ├── api                 # HTTP API
│   ├── config              # 配置
│   ├── mcp                 # mcp
│   ├── memory              # short-term / long-term memory
│   ├── models              # 模型提供方抽象
│   ├── prompts             # prompt
│   ├── rag                 # rag
│   ├── skills              # skills
│   ├── storage             # sqlite 持久化
│   ├── tools               # tools
│   └── utils
├── data
│   ├── chroma
│   └── documents           # 测试文档源（2 md + 1 docx 生成源）
├── docs
│   └── phase2_backlog.md
├── .env.example
├── requirements.txt
└── README.md
```

## 2. 各目录职责

- `app/agents`：单 Agent（LangGraph）编排，整合 prompt / memory / tools / skills / mcp。
- `app/rag`：文档解析（md/docx）、切块、向量索引与检索。
- `app/memory`：
  - `short_term.py`：按 `session_id` 维护最近 N 轮对话。
  - `long_term.py`：按 `user_id` 存储画像（语言、风格、角色）。
- `app/prompts`：中英文 system prompt 模板 + 动态加载器。
- `app/tools`：本地工具（search_documents/get_current_time/multiply）。
- `app/skills`：skill 抽象层与 3 个技能实现。
- `app/mcp`：最小本地 MCP Server 与 MCP Client。
- `app/api`：FastAPI 接口。
- `app/storage`：SQLite 最小存储封装。

## 3. 核心运行流程

1. 启动 FastAPI 服务。  
2. 通过 `/documents/import` 导入 md/docx 文档。  
3. 文档解析 + 切块 + 向量入库（Chroma）。  
4. `/chat` 请求进入单 Agent：
   - 读取长期记忆（用户画像）
   - 读取短期记忆（会话历史）
   - 组装 skill context
   - 加载动态 system prompt（zh-CN / en-US）
   - 模型按需调用 tools（含 RAG 工具）与 MCP 能力
   - 返回回答 + 引用 + 使用工具/技能/MCP 轨迹
5. 对话写回短期记忆；用户画像可通过 profile API 更新。

## 4. 环境准备

- Python 3.12
- Windows 本地可直接运行（PowerShell 或 CMD）
- Ollama（默认）

安装依赖：

```bash
pip install -r requirements.txt
```

复制配置：

```bash
cp .env.example .env
```

> Windows 可用：`copy .env.example .env`

## 5. Ollama 启动说明（默认推荐）

1. 启动 Ollama 服务（默认 `http://localhost:11434`）。
2. 拉取模型：

```bash
ollama pull qwen3:8b
```

如需本地 embedding：

```bash
ollama pull nomic-embed-text
```

并在 `.env` 中设置：

```env
EMBEDDING_PROVIDER=ollama
```

默认 `EMBEDDING_PROVIDER=hash`，无需额外模型，保证最小可运行。

## 6. MCP 本地启动说明

可单独启动 MCP Server：

```bash
python -m app.mcp.server
```

主应用中默认通过 `MCP_SERVER_COMMAND=python -m app.mcp.server` 自动拉起并通信。

## 7. 启动 API

```bash
uvicorn app.main:app --reload --port 8000
```

## 8. curl 示例

### 8.1 导入 Markdown

```bash
curl -X POST http://127.0.0.1:8000/documents/import \
  -H "Content-Type: application/json" \
  -d '{"file_path":"data/documents/settlement_rules.md"}'
```

### 8.2 先生成 Word 示例，再导入

```bash
python scripts/generate_sample_docx.py
```

```bash
curl -X POST http://127.0.0.1:8000/documents/import \
  -H "Content-Type: application/json" \
  -d '{"file_path":"data/documents/settlement_checklist.docx"}'
```

### 8.3 更新用户画像

```bash
curl -X POST http://127.0.0.1:8000/users/u1/profile \
  -H "Content-Type: application/json" \
  -d '{"preferred_language":"zh-CN","preferred_answer_style":"结构化","domain_role":"清结算专员"}'
```

### 8.4 发起问答

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id":"u1","session_id":"s1","message":"请解释 T+1 的含义","language":"zh-CN"}'
```

### 8.5 查询会话

```bash
curl http://127.0.0.1:8000/conversations/s1
```

## 9. 第一阶段范围声明

第一阶段已实现：

- 文档导入（md/docx）+ 切块 + metadata（docx 示例通过脚本本地生成）
- 向量检索 RAG
- LangGraph 单 Agent
- tool calling（本地工具 + 搜索工具）
- skill 抽象层（3 个技能）
- 短期记忆（session）
- 长期记忆（user profile）
- 动态 system prompt（中英文模板）
- Ollama 优先 + OpenAI-compatible 抽象
- 最小 MCP（tool/resource/prompt）
- 最小 HTTP API

第二阶段仅 backlog，不在本项目实现：见 `docs/phase2_backlog.md`。
