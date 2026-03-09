# 第二阶段 Backlog（仅设计，不在第一阶段实现）

> 说明：以下能力全部作为 TODO，不进入第一阶段代码实现。

1. **Observability / tracing**  
   - TODO: 引入链路追踪（如 OpenTelemetry）和调用耗时采集。
2. **Guardrails**  
   - TODO: 增加敏感内容规则和回答约束校验。
3. **Benchmark / evaluation set**  
   - TODO: 建立结算问答评测集与自动评测脚本。
4. **工程化 persistence / durable execution**  
   - TODO: 将关键状态迁移到更稳健的持久化方案。
5. **Human-in-the-loop**  
   - TODO: 增加人工审核、人工确认的回路节点。
6. **多 agent / subagent**  
   - TODO: 引入术语解释子 Agent、对账规则子 Agent。
7. **Structured output schema 强约束**  
   - TODO: 对回答输出做 JSON Schema 严格校验。
8. **Metadata filtering / reranker**  
   - TODO: 增加 metadata 过滤和重排模型。
9. **Admin config UI**  
   - TODO: 提供后台配置页面。
10. **Auth / RBAC / tenant isolation**  
    - TODO: 增加鉴权、角色权限和多租户隔离。
11. **审计日志**  
    - TODO: 增加问答、工具调用与配置变更审计日志。
12. **文档增量更新与重建索引机制**  
    - TODO: 支持增量导入、删除和异步重建索引。
13. **更强 embedding / rerank provider 抽象**  
    - TODO: 扩展更多 embedding/rerank 服务商并统一接口。
14. **Prompt versioning**  
    - TODO: 增加 prompt 版本管理、回滚与 A/B 实验。
