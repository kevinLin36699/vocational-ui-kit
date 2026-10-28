# 材料盘点与组件覆盖

扫描 327 个文本材料文件，其中业务 HTML/CSS/JS 272 个；静态资源文本和设计说明单独计入材料。提取 7457 个类名、579 条 !important。文件 SHA256、行数与路径见 data/source-manifest.json。

扫描采用词法提取，CSS .class 与 HTML/JS 中 class 属性包含动态字符串时可能存在漏提或误提；不解析完整 AST，不运行 eval。颜色和圆角统计为源声明频次，不是浏览器计算样式。源码位置为扫描当时行号。

## 核心问题
- 已有共享 ui-tokens 与 design-system，却并存大量角色/页面适配层与高优先级选择器。
- 标题旧变量28px与当前规则24px并存；按钮、卡片、输入存在历史尺寸和色值。
- 多个专用业务直接拼接 HTML 和局部样式，不能靠一次全局样式覆盖安全迁移。
- 普通过程、生成内容、输入及头像规则已有当前正文，早期页面仍需逐项对齐。
- 现有组件 API 依附全局控制器；本次独立实现可复用外观和交互，正式替换时必须保留事件及权限。

## 118 类组件
| 标识 | 名称 | 分类 | 规则 | 本地来源示例 |
| --- | --- | --- | --- | --- |
| voc-button | 按钮 | 基础 | CMP01/02/06 | css/account.css:3 |
| voc-icon | 图标与图标按钮 | 基础 | CMP08～13 | css/ui-tokens.css:9 |
| voc-link | 链接 | 基础 | NAV10/TXT06 | css/student-training-dashboard.css:165 |
| voc-tag | 标签与可移除项 | 基础 | TXT04/WID07 | css/ai-composer.css:45 |
| voc-badge | 状态徽标 | 基础 | CMP07/TXT04 | css/account.css:2 |
| voc-avatar | 头像 | 基础 | TXT05 | css/account.css:1 |
| voc-separator | 分割线 | 基础 | TXT06 | css/account.css:2 |
| voc-input | 文本输入 | 录入 | WID01/FORM | css/account.css:3 |
| voc-textarea | 多行输入 | 录入 | WID02 | css/admin-interaction-standard.css:348 |
| voc-number | 数字与单位 | 录入 | WID03 | js/ai-practice-components.js:63 |
| voc-select | 下拉选择 | 录入 | WID06 | css/admin-interaction-standard.css:137 |
| voc-checkbox | 复选框 | 录入 | WID05 | css/admin-interaction-standard.css:441 |
| voc-radio | 单选组 | 录入 | WID05 | css/admin-interaction-standard.css:538 |
| voc-switch | 开关 | 录入 | WID08 | css/admin-interaction-standard.css:222 |
| voc-date | 日期与范围 | 录入 | WID04 | js/ai-practice-course.js:532 |
| voc-multiselect | 多选标签 | 录入 | WID07 | css/ai-composer.css:45 |
| voc-cascade | 院系专业级联 | 录入 | WID07/FORM11 | js/account.js:5 |
| voc-upload | 文件上传 | 录入 | FILE/WID02 | css/assessment-authoring.css:41 |
| voc-form | 分区表单与校验 | 录入 | FORM/CON | css/account.css:1 |
| voc-search | 搜索 | 录入 | LIST01/WID01 | css/admin-interaction-standard.css:133 |
| voc-table | 数据表格 | 展示 | TBL01～08 | css/admin-interaction-standard.css:191 |
| voc-pagination | 分页 | 展示 | LIST/TBL | css/course-analytics.css:71 |
| voc-card | 内容卡片 | 展示 | CMP04/05 | css/ai-practice-editor.css:259 |
| voc-description | 描述列表 | 展示 | TXT/CON02 | css/admin-interaction-standard.css:143 |
| voc-tree | 树与目录 | 展示 | WID11/EDU02 | css/admin-interaction-standard.css:194 |
| voc-steps | 步骤条 | 展示 | WID12/AIC14 | css/admin-interaction-standard.css:106 |
| voc-progress | 进度 | 展示 | VIS04 | css/ai-practice.css:102 |
| voc-timeline | 时间线与审批记录 | 展示 | DATA/OPS | css/centers/administration.css:1103 |
| voc-stat | 指标卡 | 展示 | VIS01/DATA02 | css/admin-interaction-standard.css:39 |
| voc-chart | 统计图与明细 | 展示 | VIS01～06 | css/admin-interaction-standard.css:184 |
| voc-empty | 空状态 | 展示 | TBL07/STATE | css/admin-interaction-standard.css:53 |
| voc-skeleton | 骨架与加载 | 展示 | STATE | css/assessment-authoring.css:4 |
| voc-shell | 应用外壳与导航 | 导航布局 | NAV/LAY | css/admin-interaction-standard.css:13 |
| voc-breadcrumb | 面包屑 | 导航布局 | NAV07/WID12 | css/ai-practice.css:138 |
| voc-tabs | 内容标签页 | 导航布局 | LAY03 | css/admin-interaction-standard.css:512 |
| voc-segmented | 分段控件 | 导航布局 | DESIGN 10.6 | css/login.css:23 |
| voc-toolbar | 筛选与操作栏 | 导航布局 | TPL02/LIST | css/admin-interaction-standard.css:132 |
| voc-menu | 更多菜单 | 反馈浮层 | OVR/WID09 | css/account.css:1 |
| voc-popover | 选择浮层 | 反馈浮层 | OVR/WID10 | css/ai-composer.css:99 |
| voc-tooltip | 悬停与焦点提示 | 反馈浮层 | WID10/ACC | index.html:151 |
| voc-dialog | 弹窗 | 反馈浮层 | OVR01～10 | css/admin-interaction-standard.css:120 |
| voc-confirm | 危险操作确认 | 反馈浮层 | CMP06/OVR | css/admin-interaction-standard.css:122 |
| voc-drawer | 抽屉 | 反馈浮层 | OVR/LAY12 | css/admin-interaction-standard.css:121 |
| voc-alert | 就地反馈与错误 | 反馈浮层 | SYS01/09 | css/admin-interaction-standard.css:42 |
| voc-toast | 轻提示 | 反馈浮层 | SYS01/DESIGN10.16 | css/centers/administration.css:329 |
| voc-course-card | 课程卡片 | 高职教业务 | EDU/TXT05 | css/design-system.css:127 |
| voc-person-picker | 人员选择 | 高职教业务 | FORM11/DATA | css/admin-interaction-standard.css:560 |
| voc-approval | 审核与分发 | 高职教业务 | OPS/AIC12 | css/centers/administration.css:1103 |
| voc-resource | 资源与版本 | 高职教业务 | FILE/TRN | css/management.css:2 |
| voc-task-guide | AI 任务引导 | AI交互 | CHAT15 | css/admin-interaction-standard.css:95 |
| voc-agent | 智能体入口 | AI交互 | DESIGN11.11 | css/admin-interaction-standard.css:5 |
| voc-conversation | 会话列表 | AI交互 | HIST01～10 | css/admin-interaction-standard.css:144 |
| voc-composer | AI 输入区 | AI交互 | AIC05/16 | css/admin-interaction-standard.css:39 |
| voc-message | 用户与 AI 消息 | AI交互 | AIC02/03 | css/course-workflow.css:103 |
| voc-prose | Markdown 与代码 | AI交互 | DESIGN 附录C/AIC02 | js/ai-practice-editor.js:805 |
| voc-process | 处理过程 | AI交互 | AIC06/15 | css/student-job-search.css:189 |
| voc-citation | 引用与来源 | AI交互 | DESIGN11.7/DATA01 | css/ai-practice-editor.css:32 |
| voc-result | 生成内容摘要 | AI交互 | AIC07 | css/admin-interaction-standard.css:564 |
| voc-workspace | 生成内容工作区 | AI交互 | AIC08/12 | css/account.css:1 |
| voc-chat | AI 协作组合 | AI交互 | AI/CHAT/AIC | css/ai-composer.css:65 |
| voc-time-picker | 时间选择 | 录入 | EDU/QUALITY-2.1 | js/teacher-training-arrangement.js:5 |
| voc-tree-select | 树选择 | 录入 | EDU/QUALITY-2.1 | js/centers/administration/views/teaching.js:14 |
| voc-academic-term | 学年学期选择 | 高职教业务 | EDU/QUALITY-2.1 | js/centers/administration/views/teaching.js:14 |
| voc-collapse | 折叠面板 | 展示 | EDU/QUALITY-2.1 | js/teacher-training-materials.js:159 |
| voc-rate | 五级评价 | 录入 | EDU/QUALITY-2.1 | js/centers/administration/views/course-evaluation.js:160 |
| voc-calendar | 事件日历 | 展示 | EDU/QUALITY-2.1 | js/student-training-dashboard.js:96 |
| voc-notification | 通知提醒 | 反馈浮层 | EDU/QUALITY-2.1 | 建议扩展 |
| voc-image-preview | 图片预览 | 展示 | EDU/QUALITY-2.1 | js/teacher-training-materials.js:44 |
| voc-feedback-result | 操作结果反馈 | 反馈浮层 | EDU/QUALITY-2.1 | js/course-hub.js:168 |
| voc-batch-import | 名单导入校验 | 高职教业务 | EDU/QUALITY-2.1 | js/course-hub.js:146 |
| voc-date-picker | 单日期选择 | 录入 | FAMILY/2.2 | 建议扩展 |
| voc-date-range | 日期范围选择 | 录入 | FAMILY/2.2 | 建议扩展 |
| voc-time-range | 时间范围选择 | 录入 | FAMILY/2.2 | 建议扩展 |
| voc-datetime-picker | 日期时间选择 | 录入 | FAMILY/2.2 | 建议扩展 |
| voc-datetime-range | 日期时间范围 | 录入 | FAMILY/2.2 | 建议扩展 |
| voc-year-picker | 年份选择 | 录入 | FAMILY/2.2 | 建议扩展 |
| voc-year-range | 年份范围 | 录入 | FAMILY/2.2 | 建议扩展 |
| voc-month-picker | 月份选择 | 录入 | FAMILY/2.2 | 建议扩展 |
| voc-month-range | 月份范围 | 录入 | FAMILY/2.2 | 建议扩展 |
| voc-quarter-picker | 季度选择 | 录入 | FAMILY/2.2 | 建议扩展 |
| voc-week-picker | 周选择 | 录入 | FAMILY/2.2 | 建议扩展 |
| voc-multi-date | 多日期选择 | 录入 | FAMILY/2.2 | 建议扩展 |
| voc-password | 密码输入 | 录入 | FAMILY/2.2 | 建议扩展 |
| voc-input-group | 组合输入 | 录入 | FAMILY/2.2 | 建议扩展 |
| voc-slider | 滑动输入条 | 录入 | FAMILY/2.2 | 建议扩展 |
| voc-autocomplete | 自动补全 | 录入 | FAMILY/2.2 | 建议扩展 |
| voc-transfer | 穿梭选择 | 录入 | FAMILY/2.2 | 建议扩展 |
| voc-list | 数据列表 | 展示 | FAMILY/2.2 | 建议扩展 |
| voc-anchor | 锚点导航 | 导航布局 | FAMILY/2.2 | 建议扩展 |
| voc-loading | 加载指示 | 反馈浮层 | FAMILY/2.2 | 建议扩展 |
| voc-color-picker | 颜色选择 | 录入 | FAMILY/2.2 | 建议扩展 |
| voc-richtext | 基础富文本编辑 | 录入 | FORM/2.3 | 建议扩展 |
| voc-navigation-menu | 业务导航菜单 | 导航布局 | FAMILY/2.2 | 建议扩展 |
| voc-carousel | 图文轮播 | 展示 | FAMILY/2.2 | 建议扩展 |
| voc-splitter | 可调整分栏 | 导航布局 | FAMILY/2.2 | 建议扩展 |
| voc-backtop | 局部返回顶部 | 导航布局 | FAMILY/2.2 | 建议扩展 |
| voc-teaching-audience | 教学对象选择 | 高职教业务 | FAMILY/2.2 | 建议扩展 |
| voc-curriculum-plan | 教学目录与学时 | 高职教业务 | FAMILY/2.2 | 建议扩展 |
| voc-teaching-task | 教学任务 | 高职教业务 | FAMILY/2.2 | 建议扩展 |
| voc-question-sheet | 题目与作答 | 高职教业务 | FAMILY/2.2 | 建议扩展 |
| voc-submission-review | 提交与批阅 | 高职教业务 | FAMILY/2.2 | 建议扩展 |
| voc-scoring-rubric | 评分量规 | 高职教业务 | FAMILY/2.2 | 建议扩展 |
| voc-class-roster | 班级名册 | 高职教业务 | FAMILY/2.2 | 建议扩展 |
| voc-teaching-assignment | 任教关系 | 高职教业务 | FAMILY/2.2 | 建议扩展 |
| voc-practice-workflow | 实训步骤与验收 | 高职教业务 | FAMILY/2.2 | 建议扩展 |
| voc-learning-progress | 学习进度与续学 | 高职教业务 | FAMILY/2.2 | 建议扩展 |
| voc-resource-version | 资源版本与引用 | 高职教业务 | FAMILY/2.2 | 建议扩展 |
| voc-evaluation-survey | 评价问卷 | 高职教业务 | FAMILY/2.2 | 建议扩展 |
| voc-grade-detail | 成绩明细 | 高职教业务 | FAMILY/2.2 | 建议扩展 |
| voc-career-goal | 成长目标 | 高职教业务 | FAMILY/2.2 | 建议扩展 |
| voc-growth-plan | 成长计划 | 高职教业务 | FAMILY/2.2 | 建议扩展 |
| voc-job-opportunity | 岗位目录 | 高职教业务 | FAMILY/2.2 | 建议扩展 |
| voc-application-tracker | 投递进度 | 高职教业务 | FAMILY/2.2 | 建议扩展 |
| voc-assessment-collection | 评估指标采集 | 高职教业务 | FAMILY/2.2 | 建议扩展 |
| voc-evidence-material | 佐证材料 | 高职教业务 | FAMILY/2.2 | 建议扩展 |
| voc-asset-loan | 设备借还 | 高职教业务 | FAMILY/2.2 | 建议扩展 |
| voc-repair-ticket | 报修工单 | 高职教业务 | FAMILY/2.2 | 建议扩展 |
| voc-admissions-lead | 招生线索 | 高职教业务 | FAMILY/2.2 | 建议扩展 |

每类完整来源片段、适用状态及 API 见 data/components.json，展示站可查看对应来源。

## 覆盖与未覆盖
已建立上述118类的可运行原型实现与15类组合模板。该结论不表示每个旧页面已迁移，或每个状态都已浏览器验收。验收另见 VALIDATION.md。

词法映射中的未判断类名全部列为 review-required；画布/考试/媒体候选列为 specialized-preserve，不把它们勉强塞入基础组件。复合动态模板、业务权限和真实异步数据的逐页覆盖仍待后续整改。
