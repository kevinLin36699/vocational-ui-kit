# 高职教 UI 组件库与页面生成 Skill

本目录提供一套可以本地运行的 UI 组件库和配套 `vocational-page-builder` Skill，用于新建高职教页面、整改旧页面和局部修改。Skill 消费组件库，不重新设计整套系统。

组件库版本 **2.7.1**，Skill 版本 **1.2.0**。本次快照：**2026-10-28**。包含 **118 类组件、15 个页面模式、122 个设计变量**；三批业务组件共 **22 类、86 组配置**。配色以蓝白为主，AI 入口少量使用蓝紫。

## 目录

```text
vocational-ui-kit/
├── README.md
├── high-school-ui/                 # 完整组件库：源码、规范、索引、示例、历史证据
│   ├── index.html                  # 组件展示站入口
│   ├── css/、js/、data/、design/
│   ├── examples/teacher-input.html  # 当前教师输入区组合
│   └── examples/process-record.html # 详细处理记录，独立可选示例
├── skills/vocational-page-builder/ # 可安装的 Skill
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── references/
│   ├── scripts/
│   └── assets/
└── scripts/install_skill.py        # 安装时绑定当前 checkout 的组件库
```

运行时不需要原始高职教工程、参考平台账号或外部模型。原平台源码及参考 DESIGN.md 没有随本目录重复分发；组件库中保留相关研究结论、来源索引与历史校验记录。

## 本地预览

在本目录运行（Python 3）：

```bash
python3 -m http.server 8789 --bind 127.0.0.1 --directory high-school-ui
```

然后打开：

- 组件库：<http://127.0.0.1:8789/index.html>
- 业务示例总览：<http://127.0.0.1:8789/index.html#/examples>
- 表格与表单：<http://127.0.0.1:8789/examples/table-form.html>
- 课程与教学、学习与考核：`examples/education.html`、`examples/education-next.html`
- 成长就业、评估运营：<http://127.0.0.1:8789/examples/education-platform.html>
- 三批联动：<http://127.0.0.1:8789/examples/education-integration.html>
- 教师输入区：<http://127.0.0.1:8789/examples/teacher-input.html>
- 详细处理记录：<http://127.0.0.1:8789/examples/process-record.html>
- 管理组合：<http://127.0.0.1:8789/examples/management.html>
- AI 组合：<http://127.0.0.1:8789/examples/ai-workspace.html>

端口被占用时自行换端口。无需安装本仓库的 Next.js/pnpm 依赖；这些 HTML 原型独立运行，不会自动改动教师端应用。

## 安装与发现 Skill

保持整个目录在本地，执行：

```bash
python3 scripts/install_skill.py
```

默认安装到 `$CODEX_HOME/skills/vocational-page-builder`，未配置 `CODEX_HOME` 时使用 `~/.codex/skills/vocational-page-builder`。已有同名技能时默认拒绝覆盖；确认更新后执行：

```bash
python3 scripts/install_skill.py --replace
```

已有独立维护的组件库时，可以加 `--library-root /absolute/high-school-ui` 绑定该目录；默认使用本仓库内的副本。

旧技能会备份到 Codex 目录下的 `skill-backups/`。可用 `--codex-home /your/codex-home` 指定其他位置。脚本只安装技能，组件库继续引用当前 checkout，不会额外复制长期失配的标准。安装后在 Codex 新会话中通过 `$vocational-page-builder` 调用；若列表尚未刷新，重新打开会话或重启应用。

## 当前配置与业务能力

表格支持自定义 rows/columns/rowKey、筛选排序分页、选择、编辑和远程读写回执；表单支持 fields/values、条件联动、分步、重复项、校验和提交回执。三批业务组件支持目录与记录配置、业务操作、异常恢复及显式跨组件关联。正式服务、权限、上传和持久化由调用方接入，未确认的请求不会自动显示成功。

详情页、家族预览与业务实验室提供可替换示例数据；空数据作为独立状态。示例专用 showcaseRuntime/showcaseStyles 不进入实际业务的默认 runtime。参数见 `high-school-ui/design/TABLE_FORM.md`、`EDUCATION.md`、`EDUCATION_NEXT.md`、`EDUCATION_PLATFORM.md`；展示数据规则见 `BUSINESS_EXAMPLES.md`。

## 当前生成规则

- 「＋ 资源」为浅蓝入口，「技能」为浅蓝紫入口；使用同一套尺寸和主题变量。
- 资源支持输入 `/` 唤起，**先选类型再选对象**，目录随身份和业务配置。
- 技能提供内置／我的列表；选中标签位于所有正文前，可移除，不自动发送。
- 教师可按业务配置产业、就业、政策、技术等 Agent 选项，不显示“教学关联”标题。选择只改草稿，发送才携带本轮关联；生成中锁定，原轮重试沿用原轮选择。其他角色不强制显示。
- 输入正文默认最小高度 **112px**，聚焦 **128px**；内容自然增高，达到上限后内部滚动。
- **生成内容区默认只预留通用容器与空插槽**，不预装教学大纲、PPT、试题等业务编辑器。用户给出具体业务需求时，由页面在容器内实现或挂载相应内容、字段、编辑器和业务流程；不是所有任务都只交付空壳。
- 保存、版本、审核、发布、权限及数据归业务层；公共容器不擅加这些行为。
- 详细处理记录目前是可选的单项预览，不是已升级的公共 `process` API，不强制所有页面套用。

组件库是 **interactive-html-prototype**，不是 React/Chakra 的生产包。此仓库现有框架页面应按原架构适配，不应全局引入原型 CSS reset。AI、Agent、资料和保存均以页面标注为准，本地模拟不代表真实服务已接入。

## 三个调用示例

1. `$vocational-page-builder 新建教师课程管理页，包含院系筛选、课程表格、新增与编辑弹窗，使用本地演示数据。`
2. `$vocational-page-builder 将我提供的页面整改为当前组件库风格，保留字段、权限和必要交互，不重写无关内容。`
3. `$vocational-page-builder 生成智能备课页面，支持资源、技能和产业/政策关联；生成区复用容器，内部按我提供的教学活动业务需求实现。`

## 路径、版本与更新

仓库内 Skill 的默认绑定使用相对技能目录的 `../../high-school-ui`；无需修改用户名或系统盘符。安装脚本会将安装副本绑定到当前组件库绝对路径，原始业务工程路径留空。整改时由任务提供真实目标项目。

若移动了 checkout，请重新执行安装脚本，或通过 `VOCATIONAL_UI_LIBRARY_ROOT`、项目 `.vocational-page-builder.json` 的 `library_root`、解析器 `--library-root` 覆盖。环境变量和显式相对路径按运行工作目录解析，项目配置相对路径按配置文件目录解析。

Skill 每次解析实际 `data/library.json`、索引、规范和源码哈希。同主版本发生变化会提示重新读取；主版本变化或指定版本不符会拒绝静默降级。更新组件库后须检查 API、规范和相关示例，不能只覆盖哈希掩盖差异。

```bash
python3 skills/vocational-page-builder/scripts/resolve_library.py --component composer --component workspace
```

从仓库执行该命令可以直接检查绑定，无需先安装。新页面脚手架必须输出到本包与原业务项目之外的独立任务目录；它只是种子，不等于完成业务需求。

历史资料位于 `high-school-ui/assets/archive/`，不属于当前生成默认规范。`data/validation.json` 等是各次历史验证证据，查看时核对版本与范围；需要原业务源码或原机路径的追溯检查在其他机器上不可直接复现，不能因此宣称原平台已验证。

本次仓库打包的定向验证结果见 [validation.json](validation.json)。运行组件库静态校验和现有规则回归、Skill 路径解析及脚手架检查；没有连接生产服务。独立包的静态检查会明确跳过未随包分发的原业务源码追溯；不会改写原始扫描基线。
