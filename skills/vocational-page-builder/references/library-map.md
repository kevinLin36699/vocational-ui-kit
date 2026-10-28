# 组件库导航与版本

路径与版本只来自 library-binding.json 和解析器，不在本文件复制绝对路径或色值标准。源码和规范是主依据，技能不携带组件库副本。

## 每次最少读取

resolve_library.py 输出：实际根目录、library 元数据、版本策略、generation_standard、standard、api、limitations 及变化提示。先读这四份，再按需深入。

| 场景 | 解析参数 | 继续读取 |
| --- | --- | --- |
| 筛选、表格、表单 | --component table --component form --pattern list | 当前组件 parameters、controls 契约、table_form 及 api；按实例方法绑定加载/提交 |
| 三批业务组件 | --component career-goal（换成实际 key） | education / education_next / education_platform、controls 契约及对应 examples |
| 业务示例与变体 | 所需组件 | business_examples；示例数据与正式 runtime 分开 |
| AI 会话与创作 | --component chat --component composer --pattern chat | ai、相关实现和 limitations |
| 业务内嵌助手 | --pattern assistant --component chat | ai、patterns、源角色助手显隐规则 |
| 现有页面整改 | 所需组件和模式 | migration 文档；只检索相关旧选择器，不全量读取大 JSON |
| 框架或单文件 | 所需组件 | integration、api；再读本技能 generation.md |

解析器通过 manifest 的 componentIndex/tokenIndex/pagePatternIndex/styles/runtime/patternsRuntime 取实际文件；文档路径在单一 binding 中维护。命名或 schema 改变时先重新定位并更新绑定，不继续使用失效引用。

## 更新机制

默认 compatible-major：同主版本更新可解析，但必须读取实际版本的规范/API/变化文件并重新核对；不把旧参数快照当作新版本契约。主版本变化拒绝静默接入。用户明确给定的 --version 必须精确匹配当前库，不能假称已切换到磁盘不存在的旧版本。

baseline_hashes 只用于发现变化和溯源，不是组件库副本；发生变化不会写回或修复源库。确认新主版本适配时再更新 baseline_version 与基线哈希。仅更换本地位置时更新一个 library_root 或使用显式覆盖。source_project_root 也是统一配置项，目标项目明确不同路径时以该项目为准。

## 成熟度

当前库为 interactive-html-prototype。表格、表单及业务组件支持当前契约中的配置与实例操作；部分页面配方仍含固定演示字段和数据；组件 render/mount 成功不证明已经满足新业务需求。没有生产框架包、后端权限、真实模型/文档解析、永久版本或正式考试引擎。

## 公共视觉统一后的读取
组件索引中的alignment字段给出当前组件的参考条款与组合类别。需要核对参考或处理样式差异时按需读取reference_alignment和component_alignment；颜色、尺寸、Tabs、消息与生成空插槽以当前绑定版本为准，不恢复历史样式。

## 当前 AI 条件性资源
解析器直接从组件库 manifest 返回 documents.resource_composer / skill_selection / teaching_agents / generated_content，以及 contracts 对应 JSON；涉及哪类行为才读取对应文件。examples.teacher_input 是当前输入组合预览；examples.detailed_process_preview 是仅供参考的单项详细记录，不表示公共 process 配方已升级。完整路径和哈希均由解析器提供。

本次同步将已检查的当前同主版本文件更新为哈希基线；以后同版本文件变动也会提示重读。不要据历史基线覆盖磁盘上的新源码。

## 仓库分发
默认 library_root 相对技能目录解析，仓库包可整体移动。使用包内安装脚本复制技能时，它会将该字段绑定至当前 checkout 的组件库；移动 checkout 后重新安装或使用显式路径覆盖。source_project_root 允许为空，表示源业务工程未随包分发；整改时使用任务实际提供的项目。
