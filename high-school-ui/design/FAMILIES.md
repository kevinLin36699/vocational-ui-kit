# 全家族组件完整性 · v2.7.1

[全家族交互实验室](../examples/families.html)逐类提供目录与配置，覆盖基础、录入、展示、导航布局、反馈、高职教业务、AI交互。表格/表单/toolbar沿用TABLE_FORM.md。组件总数为118项，表格/表单/toolbar之外共115项；第一批业务组件另见EDUCATION.md，第二批见EDUCATION_NEXT.md；新增导航菜单、图文轮播、可调整分栏与局部返回顶部。

## 本轮补齐

- 基础与内容：单实例可配置按钮、链接、可选标签、计数/圆点徽标、头像组展开与失败回退、三列描述与复制、可折叠卡片、精度指标、横纵时间线、环形/仪表/分段/不确定进度、静态/动画骨架和局部遮罩。
- 导航：可关闭/新增请求/未保存保护页签、嵌套横纵导航、同层面包屑、完整/简洁分页、手风琴键盘操作、滚动锚点跟随、分栏键盘及拖动、局部返回顶部。
- 反馈：普通/复选/单选/子菜单，焦点与悬停提示、说明浮层、四向抽屉、可控弹窗、危险确认、异步防重和失败保留、可关闭提示与多动作结果反馈。
- 数据内容：列表/网格、搜索排序与逐批显示，异步追加失败保留；日历月/周/日/日程、边界和禁选、键盘选日；图片组切换、缩放旋转、重置、重试；通知筛选、单项/批量已读及禁用项保护。
- 业务与AI：课程卡片、助手目录、任务预填、消息正文/附件/反馈、Markdown、来源、成果摘要、审核状态和平台外壳均接受业务配置。没有把固定课程名称或固定问题放进通用控制器。自定义公开处理阶段可通过process.stages传入。
- 既有录入：只读单选/多选/树选择/人员选择锁定入口和移除；树禁用父项继承；保留禁用已选人员；中文组合输入完成后才提交值或搜索。

## 参数、状态与使用约定

依次加载data/library.json内styles与runtime，最后的family-controls.js注册本轮公共渲染器。使用VocUI.mount(host,key,props)，切换和移除前调用destroy；不直接运行预览控制器。

参数详见API.md和data/control-contracts.json。项目ID唯一；tabs/segmented使用value作为ID，其余集合使用id。层级目录ID在整棵树内唯一。文本与Markdown均转义；只允许已定义的安全链接和图片地址。

- loading/empty/failed/forbidden是本轮数据组件的内容状态，遮蔽正文。forbidden不会把数据仅仅藏进折叠区。静态分隔线、骨架、加载指示和结果页不套用不适用的状态。
- disabled锁定动作；readonly用于保留当前值、禁止数据修改，仍可查看允许浏览的内容。树可以在只读时展开目录，但不可改变选中项。
- 旧录入组件的空态由options/items/nodes等空集合提供，无匹配由实际搜索产生；focus/hover为真实浏览器状态，不使用state字符串伪造。
- 示例“下一次模拟失败”仅绑定本地演示处理器；确认成功文案明确注明未写入真实业务。无处理器只发出动作，不自动改变审核状态或声称已保存。

## 本轮实例接口

```javascript
VocUI.mount(host,'notification',{items:[{id:'n1',title:'资料待复核',read:false}]});
VocFamilies.getState(host); // 当前值、项目、请求编号、挂起状态等快照
VocFamilies.setState(host,'failed','读取失败，可重试');
VocFamilies.setLoader(host, async(params,{signal,requestId}) => {
  return {items: await businessRead({signal})};
});
```

- getValue/getState：读取当前值/快照；VocUI.getValue也识别本轮组件。
- setItems(host,items)：替换列表、通知、导航、页签、图片组等集合，保留仍有效的选中ID；无效页签回退首个可用项。替换会中断旧请求。
- setState(host,state,message?)：切换适用内容状态；不会自动执行真实读取。retry通过loader或load-request动作接续。
- setHandler(host, async(request,{signal,requestId})=>({ok,message?}))：按钮、弹窗、确认、消息重试、审核动作处理器。request含action与value。挂起时防重复；取消、卸载、替换请求将使迟到响应失效。
- setLoader(host, async({query,cursor},{signal,requestId})=>({items,cursor?,hasMore?}),{immediate?:true})；load(host,{append?:false})。list追加失败保留原记录与游标，重复ID明确报错，不悄悄覆盖。
- cancel(host)：取消本地等待并AbortSignal；服务端是否实际中断或回滚由业务决定。
- setPagination(host,{total?,page?,pageSize?})：总数变化后裁剪页码；setProgress(host,value,{status?})更新进度。
- setApproval(host,value)：应用业务确认状态。默认动作转换为draft→review→approved→distributed；review可退回rejected，填原因后才能退回；rejected可重新提交review。没有处理器时发出approval-request，由业务接续。

所有事件通过voc:action或voc:change冒泡，detail包含component/action/value。常用action：tab/tab-add-request/tab-remove、navigate、pagination、list-search/list-sort/list-action、calendar-select/calendar-view/calendar-event、notice-open/read-all、menu、confirm/close、agent-select/task-prepare、message-feedback、citation-open/result-open、approval-request/approval-state、shell-navigate。

需要主站路由、实际跳转或新增页签时，由业务收到请求后调用setItems或自身路由；本轮不会为用户自动创建业务对象、发送消息、发布成果或执行模型任务。

自动轮播默认关闭；鼠标悬停、焦点在组件内、页面隐藏时暂停；减少动画偏好下不自动滚动。工具提示支持上下左右与边缘翻转。浮层优先置于所属dialog顶层，退出恢复焦点；drawer提供left/right/top/bottom。异步操作结束前关闭弹层会中断本地等待。

## 逐项复查与证据

目录挂载/状态结构/320px通过只代表这些范围；定向交互结果应看具体断言。没有给只测挂载的组件标记“全部行为验收”。本轮浏览器检查入口examples/family-checks.html，既有回归examples/completeness-checks.html、examples/common-checks.html。

| 组件 | 本轮处理 | 类型 / 状态记录 |
| --- | --- | --- |
| 按钮 `button` | 参数化升级 | primary; soft; outline; ghost; destructive; sm/default/lg; default; disabled; loading; empty; failed; forbidden |
| 图标与图标按钮 `icon` | 参数化升级 | default; disabled; loading; empty; failed; forbidden |
| 链接 `link` | 参数化升级 | default; disabled |
| 标签与可移除项 `tag` | 参数化升级 | semantic; checkable; closable; default; disabled; loading; empty; failed; forbidden |
| 状态徽标 `badge` | 参数化升级 | status; count; dot; default; loading; empty; failed; forbidden |
| 头像 `avatar` | 参数化升级 | image/text; circle/square; group; default; loading; empty; failed; forbidden |
| 分割线 `separator` | 参数化升级 | default |
| 文本输入 `input` | 交互补强 | default; hover; focus; disabled; readonly; invalid |
| 多行输入 `textarea` | 交互补强 | default; focus; disabled; readonly; invalid |
| 数字与单位 `number` | 复查并沿用 | default; focus; invalid; disabled; readonly |
| 下拉选择 `select` | 交互补强 | default; open; selected; disabled; empty; readonly |
| 复选框 `checkbox` | 复查并沿用 | default; selected; disabled; readonly; partial |
| 单选组 `radio` | 复查并沿用 | default; selected; disabled; readonly |
| 开关 `switch` | 复查并沿用 | default; selected; disabled; readonly |
| 日期与范围 `date` | 复查并沿用 | default; focus; selected; partial; invalid; disabled; readonly |
| 多选标签 `multiselect` | 交互补强 | empty; selected; open; disabled; readonly |
| 院系专业级联 `cascade` | 交互补强 | empty; selected; dependent; invalid; disabled; readonly |
| 文件上传 `upload` | 复查并沿用 | empty; selected; invalid; removed; disabled; readonly |
| 搜索 `search` | 交互补强 | default; composing; searching; empty |
| 分页 `pagination` | 参数化升级 | full; simple; default; disabled; loading; empty; failed; forbidden |
| 内容卡片 `card` | 参数化升级 | default; disabled; loading; empty; failed; forbidden |
| 描述列表 `description` | 参数化升级 | 1/2/3 columns; bordered; copyable; default; loading; empty; failed; forbidden |
| 树与目录 `tree` | 复查并沿用 | collapsed; expanded; selected; disabled; readonly |
| 步骤条 `steps` | 交互补强 | pending; active; completed; disabled; readonly |
| 进度 `progress` | 参数化升级 | line; circle; dashboard; steps; indeterminate; default; loading; empty; failed; forbidden |
| 时间线与审批记录 `timeline` | 参数化升级 | vertical; horizontal; alternate; pending; default; loading; empty; failed; forbidden |
| 指标卡 `stat` | 参数化升级 | default; loading; empty; failed; forbidden |
| 统计图与明细 `chart` | 复查并沿用 | bar; line; donut; empty |
| 空状态 `empty` | 参数化升级 | empty; no-match; failed; forbidden |
| 骨架与加载 `skeleton` | 参数化升级 | default |
| 应用外壳与导航 `shell` | 参数化升级 | default; disabled; loading; empty; failed; forbidden |
| 面包屑 `breadcrumb` | 参数化升级 | default; disabled; loading; empty; failed; forbidden |
| 内容标签页 `tabs` | 参数化升级 | line; card; vertical; closable; dynamic; default; disabled; loading; empty; failed; forbidden |
| 分段控件 `segmented` | 参数化升级 | default; disabled; loading; empty; failed; forbidden |
| 更多菜单 `menu` | 参数化升级 | action; checkbox; radio; separator; submenu; default; disabled; loading; empty; failed; forbidden |
| 选择浮层 `popover` | 参数化升级 | default; disabled; loading; empty; failed; forbidden |
| 悬停与焦点提示 `tooltip` | 参数化升级 | default; disabled; loading; empty; failed; forbidden |
| 弹窗 `dialog` | 参数化升级 | default; disabled; loading; empty; failed; forbidden |
| 危险操作确认 `confirm` | 参数化升级 | default; disabled; loading; empty; failed; forbidden |
| 抽屉 `drawer` | 参数化升级 | left; right; top; bottom; default; disabled; loading; empty; failed; forbidden |
| 就地反馈与错误 `alert` | 参数化升级 | default; disabled; loading; empty; failed; forbidden |
| 轻提示 `toast` | 参数化升级 | default; disabled; loading; empty; failed; forbidden |
| 课程卡片 `course-card` | 参数化升级 | required/elective labels; cover/placeholder; local favorite; default; disabled; loading; empty; failed; forbidden |
| 人员选择 `person-picker` | 交互补强 | empty; selected; searched; disabled; readonly |
| 审核与分发 `approval` | 参数化升级 | draft; review; approved; rejected; distributed; default; disabled; loading; empty; failed; forbidden |
| 资源与版本 `resource` | 复查并沿用 | default; versioned; downloaded |
| AI 任务引导 `task-guide` | 参数化升级 | default; disabled; loading; empty; failed; forbidden |
| 智能体入口 `agent` | 参数化升级 | default; disabled; loading; empty; failed; forbidden |
| 会话列表 `conversation` | 复查并沿用 | empty; selected; renamed; pinned |
| AI 输入区 `composer` | 复查并沿用 | empty; draft; attached; running; disabled; resource-open; resource-no-match; resource-selected; resource-unavailable; agents-selected; agents-locked |
| 用户与 AI 消息 `message` | 参数化升级 | user; assistant; completed/streaming/failed/stopped; default; disabled; loading; empty; failed; forbidden |
| Markdown 与代码 `prose` | 参数化升级 | default; disabled; loading; empty; failed; forbidden |
| 处理过程 `process` | 交互补强 | waiting; running; completed; stopped; failed |
| 引用与来源 `citation` | 参数化升级 | default; disabled; loading; empty; failed; forbidden |
| 生成内容摘要 `result` | 参数化升级 | default; disabled; loading; empty; failed; forbidden |
| 生成内容工作区 `workspace` | 复查并沿用 | empty; loading; ready; error; collapsed |
| AI 协作组合 `chat` | 复查并沿用 | idle; running; stopped; failed; completed |
| 时间选择 `time-picker` | 复查并沿用 | default; focus; disabled; readonly; invalid |
| 树选择 `tree-select` | 交互补强 | default; selected; disabled; empty; no-match; readonly |
| 学年学期选择 `academic-term` | 交互补强 | default; selected; disabled; empty; readonly |
| 折叠面板 `collapse` | 参数化升级 | default; disabled; loading; empty; failed; forbidden |
| 五级评价 `rate` | 复查并沿用 | default; selected; disabled; readonly |
| 事件日历 `calendar` | 参数化升级 | month; week; day; agenda; default; disabled; loading; empty; failed; forbidden; readonly |
| 通知提醒 `notification` | 参数化升级 | default; disabled; loading; empty; failed; forbidden; readonly |
| 图片预览 `image-preview` | 参数化升级 | single; gallery; default; disabled; loading; empty; failed; forbidden |
| 操作结果反馈 `feedback-result` | 参数化升级 | success; error; forbidden; notfound; warning; info |
| 名单导入校验 `batch-import` | 复查并沿用 | draft; invalid; valid; confirmed; failed |
| 单日期选择 `date-picker` | 复查并沿用 | default; selected; disabled; readonly; invalid |
| 日期范围选择 `date-range` | 复查并沿用 | default; selected; disabled; readonly; invalid |
| 时间范围选择 `time-range` | 复查并沿用 | default; selected; disabled; readonly; invalid |
| 日期时间选择 `datetime-picker` | 复查并沿用 | default; selected; disabled; readonly; invalid |
| 日期时间范围 `datetime-range` | 复查并沿用 | default; selected; disabled; readonly; invalid |
| 年份选择 `year-picker` | 复查并沿用 | default; selected; disabled; readonly; invalid |
| 年份范围 `year-range` | 复查并沿用 | default; selected; disabled; readonly; invalid |
| 月份选择 `month-picker` | 复查并沿用 | default; selected; disabled; readonly; invalid |
| 月份范围 `month-range` | 复查并沿用 | default; selected; disabled; readonly; invalid |
| 季度选择 `quarter-picker` | 复查并沿用 | default; selected; disabled; readonly; invalid |
| 周选择 `week-picker` | 复查并沿用 | default; selected; disabled; readonly; invalid |
| 多日期选择 `multi-date` | 复查并沿用 | default; selected; disabled; readonly; invalid |
| 密码输入 `password` | 交互补强 | default; selected; disabled; readonly; invalid |
| 组合输入 `input-group` | 复查并沿用 | default; selected; disabled; readonly; invalid |
| 滑动输入条 `slider` | 复查并沿用 | default; selected; disabled; readonly |
| 自动补全 `autocomplete` | 交互补强 | default; selected; empty; no-match; disabled; readonly |
| 穿梭选择 `transfer` | 复查并沿用 | default; selected; empty; no-match; disabled; readonly |
| 数据列表 `list` | 参数化升级 | list; grid; search/sort; incremental; remote append; default; disabled; loading; empty; failed; forbidden; readonly |
| 锚点导航 `anchor` | 交互补强 | default |
| 加载指示 `loading` | 参数化升级 | default |
| 颜色选择 `color-picker` | 复查并沿用 | default; selected; disabled; readonly |
| 基础富文本编辑 `richtext` | 复查并沿用 | default; focus; invalid; disabled; readonly |
| 业务导航菜单 `navigation-menu` | 参数化升级 | horizontal; vertical; nested; collapsed; default; disabled; loading; empty; failed; forbidden |
| 图文轮播 `carousel` | 参数化升级 | text/image; bounded/loop; manual/automatic; default; disabled; loading; empty; failed; forbidden |
| 可调整分栏 `splitter` | 参数化升级 | horizontal; vertical; default; disabled; loading; empty; failed; forbidden |
| 局部返回顶部 `backtop` | 参数化升级 | default; disabled; loading; empty; failed; forbidden |
| 教学对象选择 `teaching-audience` | 复查并沿用 | default; dirty; invalid; submitting; success; failed; loading; load-error; empty; forbidden; readonly; disabled |
| 教学目录与学时 `curriculum-plan` | 复查并沿用 | default; dirty; invalid; submitting; success; failed; loading; load-error; empty; forbidden; readonly; disabled |
| 教学任务 `teaching-task` | 复查并沿用 | default; dirty; invalid; submitting; success; failed; loading; load-error; empty; forbidden; readonly; disabled |
| 题目与作答 `question-sheet` | 复查并沿用 | default; dirty; invalid; submitting; success; failed; loading; load-error; empty; forbidden; readonly; disabled |
| 提交与批阅 `submission-review` | 复查并沿用 | default; dirty; invalid; submitting; success; failed; loading; load-error; empty; forbidden; readonly; disabled |
| 评分量规 `scoring-rubric` | 复查并沿用 | default; dirty; invalid; submitting; success; failed; loading; load-error; empty; forbidden; readonly; disabled |
| 班级名册 `class-roster` | 复查并沿用 | default; dirty; invalid; submitting; success; failed; loading; load-error; empty; forbidden; readonly; disabled |
| 任教关系 `teaching-assignment` | 复查并沿用 | default; dirty; invalid; submitting; success; failed; loading; load-error; empty; forbidden; readonly; disabled |
| 实训步骤与验收 `practice-workflow` | 复查并沿用 | default; dirty; invalid; submitting; success; failed; loading; load-error; empty; forbidden; readonly; disabled |
| 学习进度与续学 `learning-progress` | 复查并沿用 | default; dirty; invalid; submitting; success; failed; loading; load-error; empty; forbidden; readonly; disabled |
| 资源版本与引用 `resource-version` | 复查并沿用 | default; dirty; invalid; submitting; success; failed; loading; load-error; empty; forbidden; readonly; disabled |
| 评价问卷 `evaluation-survey` | 复查并沿用 | default; dirty; invalid; submitting; success; failed; loading; load-error; empty; forbidden; readonly; disabled |
| 成绩明细 `grade-detail` | 复查并沿用 | default; dirty; invalid; submitting; success; failed; loading; load-error; empty; forbidden; readonly; disabled |
| 成长目标 `career-goal` | 复查并沿用 | default; dirty; invalid; submitting; success; failed; loading; load-error; empty; forbidden; readonly; disabled |
| 成长计划 `growth-plan` | 复查并沿用 | default; dirty; invalid; submitting; success; failed; loading; load-error; empty; forbidden; readonly; disabled |
| 岗位目录 `job-opportunity` | 复查并沿用 | default; dirty; invalid; submitting; success; failed; loading; load-error; empty; forbidden; readonly; disabled |
| 投递进度 `application-tracker` | 复查并沿用 | default; dirty; invalid; submitting; success; failed; loading; load-error; empty; forbidden; readonly; disabled |
| 评估指标采集 `assessment-collection` | 复查并沿用 | default; dirty; invalid; submitting; success; failed; loading; load-error; empty; forbidden; readonly; disabled |
| 佐证材料 `evidence-material` | 复查并沿用 | default; dirty; invalid; submitting; success; failed; loading; load-error; empty; forbidden; readonly; disabled |
| 设备借还 `asset-loan` | 复查并沿用 | default; dirty; invalid; submitting; success; failed; loading; load-error; empty; forbidden; readonly; disabled |
| 报修工单 `repair-ticket` | 复查并沿用 | default; dirty; invalid; submitting; success; failed; loading; load-error; empty; forbidden; readonly; disabled |
| 招生线索 `admissions-lead` | 复查并沿用 | default; dirty; invalid; submitting; success; failed; loading; load-error; empty; forbidden; readonly; disabled |

## 验证报告

- families：53通过 / 0失败，data/families-2.4/family-browser.json
- catalogRegression：36通过 / 0失败，data/families-2.4/catalog-regression.json
- tableFormRegression：53通过 / 0失败，data/families-2.4/table-form-regression.json
- unit：6通过 / 0失败，data/families-2.4/unit.json

静态检查仍保留原工程与历史来源快照差异的既有失败；本轮未改原业务工程，不重置历史快照。

## 明确边界

- 日历为本地事件查看，不提供自动排课、拖拽改期、时区转换或冲突服务
- 图片以预览为主，不提供裁剪/批注/媒体编辑；轮播不含视频播放器
- HTML原型组件，没有React/Vue框架包和可视化页面搭建器
- 交互权限仅为客户端约束，真实上传、消息投递、审批、分发、Agent/模型执行需业务回执
- 全浏览器、触摸设备、屏幕阅读器与全量视觉状态验收尚未覆盖
