# 整改映射与实施路线

data/migration-map.json / csv 登记全部 7457 条词法类名记录，包含来源、候选组件、处置理由、优先级与 verifiedMigration=false。

| 处置 | 数量 | 含义 |
| --- | --- | --- |
| candidate-mapped | 1524 | 名称或结构指示有候选，实施时复核；不是可直接全局替换的选择器映射 |
| specialized-preserve | 258 | 媒体、画布、考试、编辑器等专用类，保留原控制器与内容主题 |
| review-required | 5675 | 其余类未作自动语义结论，必须逐页核对 |

## 人工确认的迁移方向
| 现有结构 | 新组件 | 替换要点 | 优先级 |
| --- | --- | --- | --- |
| mg-btn / prep-button / upload-button | voc-button | 统一尺寸与层级，保留事件、权限和状态 | P0 |
| ui-icon / UIIcons.render | voc-icon | 复用路径；补齐可访问按钮名 | P0 |
| mg-field / mg-filters | voc-input / select / form | 规范错误和依赖；正式字段由业务控制器绑定 | P0 |
| mg-table | voc-table | 筛选排序分页口径一致，选择范围与真实导出一致 | P0 |
| data-ai-composer / composer | voc-composer | 保留草稿、输入法、原上传范围，不能重建控制节点破坏绑定 | P0 |
| message-bubble / message.assistant | voc-message / prose | 用户浅蓝；AI开放正文；历史文本安全转义 | P0 |
| AIProcessUI / ai-process-card | voc-process | 真实阶段由业务传入；本库计时不得替代真实执行状态 | P0 |
| history-actions / 协作记录 | voc-conversation | 稳定ID、草稿隔离、恢复与归档语义沿原数据 | P1 |
| modal / dialog / mg-modal | voc-dialog / confirm | 保留现有提交协议，关闭恢复焦点，确认对象与后果 | P1 |
| program-course-card | voc-course-card | 保留课程入口与16:9资源封面，分离次级操作 | P1 |
| 大纲与生成内容工作区 | voc-workspace / result | 不混淆生成、审核、保存、分发；版本与角色仍由业务提供 | P1 |
| PPT/视频/图谱/考试控件 | 专项外壳 + 原实现 | 不替换编辑引擎、画布主题、考试计分或媒体跳转 | P2 |

## 迁移步骤
1. 对目标页面记录角色、稳定对象、入口、状态、数据和权限契约。
2. 根据组件索引确定结构和变量，先在副本中替换公共外壳与低风险基础组件。
3. 给原控制器绑定适配层，保留旧节点所需 ID、事件、草稿、生成生命周期与权限。
4. 通过空/错/加载/只读/停止等适用状态检查；比较原有行为与新组件行为。
5. 有证据后将该页面映射改为已实施与已验证，记录实际覆盖范围。

本库 ui-* 变量别名仅是视觉接入辅助，不能替代迁移过程或直接覆盖原平台全部样式。
