# 高职教 UI 组件库 · 2.7.1

可复用 HTML/CSS/JS 交互组件。保留蓝白、少量蓝紫和页面级特色标题；真实接口、权限、持久化和模型由业务项目接入。

## 本地查看

直接打开 `index.html`，或在本目录运行：

```sh
python3 -m http.server 8789 --bind 127.0.0.1
```

- 表格表单与补充交互：`http://127.0.0.1:8789/examples/table-form.html`
- 通用配置/事件/约束：`design/TABLE_FORM.md`
- 组件家族与变体示例：`http://127.0.0.1:8789/examples/completeness.html`
- 本轮逐项检查：`design/COMPLETENESS.md`、`data/component-completeness.json`
- 交互细节修正版：`http://127.0.0.1:8789/examples/design-refinement.html`
- 品质预览：`http://127.0.0.1:8789/examples/quality-review.html`
- 全部组件：`http://127.0.0.1:8789/index.html#/components`
- 名单导入：`http://127.0.0.1:8789/examples/import.html`
- 长文本与局部容器：`http://127.0.0.1:8789/examples/stress.html`
- 日期边界：`http://127.0.0.1:8789/examples/control-states.html`

## 复用与规范

先读 `data/library.json`，按 styles/runtime 顺序加载，再调用 `VocUI.mount(host,key,props)`。页面模板另加载 patternsRuntime。数量、版本、资源入口以索引为准，不手写重复统计。

- `design/CONTROLS.md`：日期、选择、表格及新增组件真实 API。
- `design/GENERATION.md`：后续页面生成规则。
- `design/QUALITY_REVIEW.md`：逐项整改、实际验证、截图与未验收范围。
- `data/ui-review.json`：逐组件机器记录。
- `data/quality-browser-validation.json`：实际浏览器布局与交互证据。
- `data/quality-unit-validation.json`：日期、CSV与API纯逻辑验证。

生成内容区只提供容器。资源先类型后对象、技能正文前标签、教师Agent多选及原轮重试契约保持。

## 维护

先修改公共源码，再依次运行：

```sh
python3 scripts/build_tokens.py
python3 scripts/build_current.py
python3 scripts/build_completeness.py
python3 scripts/build_docs.py
TZ=Pacific/Honolulu node scripts/test_controls.mjs
node scripts/test_temporal.mjs
node scripts/test_common.mjs
python3 scripts/verify.py
python3 scripts/build_report.py
python3 scripts/summarize_quality.py
python3 scripts/build_docs.py
```

浏览器定向检查入口：`examples/completeness-checks.html`；本轮证据在 `data/completeness-2.2/`。

浏览器检查必须实际执行并更新证据，构建脚本不会替代视觉和操作验收。`verify.py`保留“原业务工程与最初扫描快照是否相同”的历史检查；独立下载包未包含原工程时跳过这两项追溯检查，可用 `--source-root /path/to/original` 明确提供原工程。当前存在差异，命令会返回非零，不应据此覆盖基线或伪造通过。其他失败应修复后再交付。

组件库与调用 Skill 的公开分发仓库：[vocational-ui-kit](https://github.com/kevinLin36699/vocational-ui-kit)。仓库同时提供源码、规范、配置示例和 Skill 安装脚本；本地维护目录与仓库分发副本分别验证后同步。

## 全家族复查 v2.4

- [全家族交互实验室](examples/families.html)：除表格/表单/toolbar外的93项组件入口，支持配置替换和适用状态验证。
- [全家族参数与边界](design/FAMILIES.md)，逐项记录data/component-families.json。
- 浏览器定向检查examples/family-checks.html，当前报告data/families-2.4/。本轮不覆盖已安装Skill或原业务工程。

## 高职教第一批业务组件 v2.5

- [业务实验室](examples/education.html)：教学对象、目录与学时、教学任务、题目与作答、提交与批阅、评分量规，22组可替换配置。
- [配置和确认回执](design/EDUCATION.md)，记录data/education-components.json。
- 定向浏览器examples/education-checks.html，业务规则校验node scripts/test_education.mjs，报告data/education-2.5/。

## 高职教第二批业务组件 v2.6

新增班级名册、任教关系、实训步骤与验收、学习进度与续学、资源版本与引用、评价问卷、成绩明细七类，28组配置，目录总数109。配置和普通业务操作均复用公共实现，正式操作需处理器明确回执。

- 交互预览：`examples/education-next.html`；类型、状态、配置替换、本地失败与回执。
- 接入规则：`design/EDUCATION_NEXT.md`；公共参数：`data/control-contracts.json`。
- 规则检查：`node scripts/test_education_next.mjs`；实际浏览器入口：`examples/education-next-checks.html`。
- 证据与边界：`data/education-next-components.json`、`data/education-2.6/`。真实服务、权限、上传与持久化由业务适配。

## 高职教第三批与三批联查 v2.7

新增成长目标、成长计划、岗位目录、投递进度、评估指标采集、佐证材料、设备借还、报修工单、招生线索九类、36组配置。三批合计22类、86组配置，目录118项。

- [第三批实验室](examples/education-platform.html)：类型、状态、JSON配置与普通业务操作。
- [三批联动实验室](examples/education-integration.html)：七条可整体配置链路，14种显式关联；目录更新、草稿/快照保护、失败回执和实际操作。
- [参数、关联及接入](design/EDUCATION_PLATFORM.md)；机器记录data/education-platform-components.json。
- 规则检查node scripts/test_education_platform.mjs；实际浏览器examples/education-platform-checks.html与examples/education-integration-checks.html；证据data/education-2.7/。

正式服务、权限、上传和持久化由业务接入；实验室明确使用本地模拟回执。维护时同时运行三批业务检查与基础/表格表单/家族回归，随后重建文档及验证记录。

## 业务示例数据修复 v2.7.1

三批22类、86组配置现在直接显示在组件详情、家族预览和业务实验室；默认有数据，空数据单独选择。详情新增示例选择、数据数量、操作提示、“示例数据”页签，以及包含完整数据的使用代码。画廊加入22个业务示例，共105例。

- [成长目标详情](index.html#/component/career-goal)；[成长与运营示例总览](examples/completeness.html#education-platform)。
- [数据与展示接入规则](design/BUSINESS_EXAMPLES.md)。展示专用依赖见data/library.json的showcaseRuntime，生产runtime不包含虚构业务记录。
- node scripts/test_business_examples.mjs；examples/business-example-checks.html；证据data/examples-2.7.1/。

侧栏入口按使用目的组织；预览统一从“业务示例”进入。后续扩展不再按开发批次增加一级菜单，新增组件归入现有分类及业务领域。
