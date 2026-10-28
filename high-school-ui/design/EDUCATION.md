# 高职教第一批业务组件 · v2.5.0

[业务实验室](../examples/education.html)直接挂载公共组件，提供六类、22组配置。可从空数据开始，可替换真实业务字段与ID；教师出题和量规编辑提供普通表单，不要求教师编写JSON。实验室的JSON编辑器面向组件接入和评审。

## 六类组件与支持范围

| 组件 | 类型 | 业务状态与交互 |
| --- | --- | --- |
| teaching-audience 教学对象 | 班级 / 学生 / 混合，单选 / 多选 | 组织子树范围、搜索、禁用项保护、已选复核、去重、确认快照；目录更新不改旧快照，失效对象阻止确认 |
| curriculum-plan 教学目录与学时 | 理论 / 实训 / 理实结合；最多三层 | 单元增删排序与换上级、理论/实训学时、步长/总数核对、教学目标关联、锁定继承、删除确认、草稿恢复 |
| teaching-task 教学任务 | 可配置类型目录；卡片 / 列表 | 草稿编辑保存、发布、开始、完成、结束、重开、截止调整；前置任务与检查项；逾期单独标记，不自动完成 |
| question-sheet 题目与作答 | 单选 / 多选 / 判断 / 填空 / 简答；整卷 / 逐题 | 教师出题、修改类型与选项、重排删除和总分校验；学生答题卡、标记、草稿、未答校验、部分交卷确认、提交锁定、公布后复核 |
| submission-review 提交与批阅 | 学生成果提交 / 教师批阅 / 历史只读 | 本地真实File校验、暂存、提交新版本、截止前撤回、退回重交；教师原因/分值校验、量规联动、公布反馈；旧版本不能覆盖当前批阅 |
| scoring-rubric 评分量规 | 等级 / 数值；权重 / 分项计分；作者 / 评分 / 只读 | 作者维护维度与等级、权重与满分校验；评分范围、不适用排除、未评分保留、确认与取消恢复 |

参数矩阵见API.md或data/control-contracts.json，场景配置独立放在js/education-scenarios.js；公共控制器不写死学校、课程、班级、题干或评分结果。

## 数据与规则

项目使用稳定的字符串ID，支持字母、数字、下划线与短横线；同一目录整棵树内唯一。重复、缺失和原型链保留名明确拒绝。不得使用姓名或显示标题代替身份ID。所有文本转义，不运行配置中的HTML或脚本。

- 教学对象nodes中班级kind为class，students用classId关联；scopeIds限制可用组织子树。disabled学生不能新选入班级快照，已有显式锁定选择保留。名单确认载荷包括classIds、studentIds、去重members、directoryVersion、confirmedAt。学期/班级关联属于教学任务或任教关系，不写进课程基础对象。
- 教学目录只累加末级单元。父级不能同时拥有直接学时和下级。末级学时需为非负、符合step且合计大于0；理论课不带实训学时，实训课不带理论学时。配置totalHours后，保存必须完全匹配。新增下级前先明确处理原单元学时，不悄悄清空。
- 任务的prerequisiteIds禁止无效关联和循环。checklist使用{id,label,required?,done?}。学生只能操作published/in-progress任务，教师处理草稿及发布/结束。状态改变需回执；截止不会自动提交或完成。allowLate默认false。
- 试题使用type=single/multiple/boolean/fill/text。选择题options为{id,label}[]，填空用blanks文本数组。value按题目ID存答案：字符串、ID数组、boolean、字符串数组、字符串。false是有效判断答案，空字符串不算完成。参考答案只用于公布后的展示，不提供自动判分服务。
- 学生未公布的试卷配置会移除answer/analysis；未公布的提交评分会移除grade/feedback/rubricValues。页面不把答案仅放进隐藏面板。生产服务仍必须按身份过滤返回数据，客户端配置不是鉴权机制。
- 提交版本为唯一正整数。新版本不改旧快照；教师只批阅最新待批阅版本。无提交不能凭空录分。未评分为null，与0分不同；退回需原因。正式提交后，默认需退回或撤回才能再次编辑；已评分后重交需allowResubmit。
- 量规weighted要求weight合计100；各维度评分按value/max加权，再折算totalScore。points要求各维度max合计等于总分。不适用“na”从分母排除并重新折算；未评分保持总分null，不当作0。所有适用项完成且配置有效才允许确认；全部不适用不会制造0分。等级分值在维度内唯一。

## 接入与确认回执

依照data/library.json顺序加载styles/runtime。新增education-controls.js及education-controls.css，其他基础样式仍沿用现有蓝白令牌。

```javascript
VocUI.mount(host, 'curriculum-plan', {
  mode: 'blended', totalHours: 8, step: 1,
  nodes: [{id:'unit-01', title:'项目入门', theoryHours:4, practiceHours:4}],
  context: {courseId:'current-course'}
});
VocEducation.setHandler(host, async (request, {signal, requestId, files}) => {
  // 在这里接入本业务；request含action/value/context。
  // files是当前草稿的真实File数组；JSON载荷只包含附件元数据与既有引用。
  return businessSave(request, {signal, requestId, files});
});
```

处理器返回{ok:true,message?}才应用正式变化，{ok:false,message?,fieldErrors?}保留草稿及已有记录。抛错也显示失败。挂起时锁定业务编辑、防重复，仍可取消等待。取消、卸载、更换配置、切换内容状态使旧请求失效并发出AbortSignal；服务端是否实际中断或回滚由业务实现。

没有绑定处理器时，voc:submit发出后保持等待，不自动成功。业务收到detail.requestId后调用：

```javascript
VocEducation.resolve(host, requestId, {ok:true, message:'业务已确认'});
```

只接受当前请求编号，过期回执返回false。成功后建立新的重置基线。界面“恢复上次确认”在有修改时先确认；关闭编辑弹窗不应用其中修改。

提交新版本的成功回执可带attempt:{id,submittedAt}指定业务记录标识与时间。批阅请求含attemptId/version/score/feedback/rubricValues/released，必须由服务端再次核对当前版本与权限。实验室绑定的处理器明确标注为本地模拟。

## 公共实例方法

- VocUI.mount / hydrate / destroy：挂载、初始化与卸载；VocUI.getValue识别六类业务组件。
- VocEducation.getValue(host)：当前业务值快照。对象={classIds,studentIds}；目录={nodes}；任务={tasks}；试题={answers,marked}；提交={text,attempts}；量规={scores,criteria?}。
- getState(host)：状态、dirty、errors、pending、requestId、snapshot、submitted、文件元数据及当前配置。getScore(host)只用于量规，返回score/completed/applicable/complete/errors。
- setData(host,props)：校验并替换完整配置，中断旧请求、建立新基线；不是业务保存。调用前由业务确认是否放弃未确认草稿。
- setDirectory(host,{nodes?,students?,scopeIds?,directoryVersion?})：仅更新对象目录，保留当前选择和已确认快照；失效或超范围选择需核对或清除。
- setState(host,state,message?)：设置default/readonly/disabled/loading/load-error/empty/forbidden/failed等状态。readonly/disabled保留值、禁止修改；failed保留正文，load-error提供读取重试，forbidden移除可见业务正文。
- setHandler / resolve / cancel：提交、确认回执与取消等待。
- setLoader(host,async({context},{signal,requestId})=>({props}),{immediate?:true}) / load(host)：业务数据读取。失败不清空旧草稿，重试重新读取；过期结果忽略。
- resolveLoad(host,requestId,{props?,error?,forbidden?})：事件模式load-request的读取回执。
- getFiles(host,attemptId?)：当前草稿或当前页面内指定版本的真实File引用；没有实际文件时返回空数组，不能从文件名伪造File。
- setNow(host,ISO时间)：应用业务时钟或演示时钟。未配置now的考试截止由实际时钟检查；截止只锁定新答案，不自动交卷。

## 主要事件

所有事件冒泡，detail含component/action/value/requestId/context。

- voc:change：audience-draft/directory-change、curriculum-edit/curriculum-objective、task-edit/task-checklist、answer-change/answer-mark、submission-files/review-draft、rubric-score/rubric-edit。
- voc:submit：audience-confirm、curriculum-save、task-save/task-delete/task-publish/task-start/task-complete/task-close/task-reopen/task-extend、paper-save/answer-draft/answer-submit、submission-draft/submission-submit/submission-withdraw/submission-return/submission-grade、rubric-save/rubric-score。
- 处理器确认后发出相应action-confirmed变更，confirmed=true；仅此时将正式操作应用到组件状态。
- voc:action：cancel、load-request、answer-expired。

## 验证与范围

定向浏览器入口examples/education-checks.html，纯业务规则scripts/test_education.mjs，证据位于data/education-2.5/。同时回归既有目录、通用家族、表格和表单。

第一批没有新增后端、真实上传/持久化/成绩发布服务、多人实时协作或自动排课；没有提供自动阅卷或根据评分自动作出学籍/就业决定。文件只校验本地格式、数量和大小，不声称完成内容解析、病毒扫描或上传。真实服务需核对身份、组织范围、业务版本与提交幂等。

目录支持三层；试题覆盖本平台已有五类，不扩展编程、公式证明、拖拽等专用题型；富媒体编辑、试题随机化、跨设备草稿同步和完整浏览器/WCAG认证不在本轮范围。

## 本轮验证记录

- browser：39项通过 / 0项失败；data/education-2.5/browser.json
- catalogRegression：36项通过 / 0项失败；data/education-2.5/catalog-regression.json
- commonRegression：53项通过 / 0项失败；data/education-2.5/common-regression.json
- familyRegression：53项通过 / 0项失败；data/education-2.5/family-regression.json
- unit：12项通过 / 0项失败；data/education-2.5/unit.json
- static：63项通过 / 1项失败；data/education-2.5/static.json

静态检查中的原工程历史快照差异保留为失败，不修改原工程或重置历史来源。检查通过不等于生产服务、全设备和全部视觉状态均已验收。
