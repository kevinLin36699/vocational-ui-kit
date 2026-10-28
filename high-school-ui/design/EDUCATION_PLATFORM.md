# 第三批业务组件与三批联动 · 2.7.0

第三批新增九类公共组件、36组可替换配置。三批合计22类业务组件、86组配置，组件库总目录118项。公共实现不依赖实验数据；默认目录可以为空，记录、类型、身份、时钟和授权范围由调用方提供。

- 第三批实验室：[education-platform.html](../examples/education-platform.html)。每类四组配置，可替换JSON、切换界面状态、模拟失败、取消等待、手动确认回执。
- 三批联动实验室：[education-integration.html](../examples/education-integration.html)。七条完整链路，可编辑整条链路的卡片配置、关联类型和记录ID，逐项执行普通表单操作。
- 公开参数：data/control-contracts.json；目录与证据：data/education-platform-components.json、data/education-2.7/。

## 九类公共能力

| key | 类型与配置 | 业务操作及状态边界 |
| --- | --- | --- |
| career-goal | 就业、证书、竞赛、升学及自定义types | 新增编辑、主备切换、原因归档和恢复；同一时刻只允许一个有效主目标，切换须回执成功后原子生效 |
| growth-plan | 自定义kinds、目标目录、教学/学习任务目录 | 草稿任务增删排序、启用、暂停、恢复、原因调整、依据登记、任务和计划显式完成；关联失效不删除计划，来源完成也不自动完成个人计划；requireLinkedCompletion默认true，可在任务配置/表单中调整 |
| job-opportunity | 正式、实习、学徒及自定义kinds；薪资、名额、截止时间 | 列表/卡片、搜索收藏、编辑发布关闭重开；学生投递操作创建固定岗位/简历版本的本地草稿；零名额和未知薪资分别保留 |
| application-tracker | 岗位和简历目录、当前人的投递记录 | 草稿、登记投递、筛选、面试、意向、接受记录、拒绝、撤回；阶段依据、面试时间、个人备注；提交前重新核对岗位和简历版本 |
| assessment-collection | 数值、文本、是非指标；周期、单位、责任人和佐证 | 设计分配、草稿暂存、提交、退回重提、审核；0和false有效，每次提交保留版本；过期、跨周期、来源缺失和本人审核默认拦截 |
| evidence-material | 文档、图片、链接、数据；来源目录、有效期、本地附件 | 新建、草稿、提交、退回、审核、新版本和作废；旧版本只读；真正File对象只在页面内存中保留，历史元数据不会伪装成文件 |
| asset-loan | 设备、工具、实训场地；容量、状态、时段、借用人、报修阻断目录 | 台账维护、申请、审批、驳回、取消、交付、申报归还、接收；按重叠时段峰值占用计算，逾期未接收仍占用；损坏接收同时转维护 |
| repair-ticket | 硬件、软件、网络、安全及自定义categories；设备、处理人 | 报修附件、派单、改派原因、开始、工时记录、待材料、恢复、处理结果、报告人验收/重开、取消；处理完成仍需验收，工单关闭不自动恢复设备 |
| admissions-lead | 自定义来源、专业和责任人目录；联系授权 | 新增编辑、人工跟进、预约、阶段流转、流失恢复、责任分配、重复核对合并；授权未知/撤回时拦截电话和消息记录，保留内部备注；默认禁止跳阶段 |

界面状态包含default/dirty/invalid/submitting/success/failed/loading/load-error/empty/forbidden/readonly/disabled。业务状态与界面状态分开，例如投递的interview与请求的submitting。只读、禁用、无权限以及等待回执时禁止变更；加载失败保留原草稿。周期、岗位截止、材料有效期、借用和预约支持业务时钟或当前时间。

## 配置和接入

按data/library.json的styles/runtime顺序加载。第三批运行于共享VocEducationNext生命周期，并由VocEducationPlatform提供同等公共入口：

```js
VocUI.mount(host, 'career-goal', {
  role: 'student', actorId: 'current-learner',
  types: [{id: 'project', label: '项目成长'}],
  goals: [], context: {spaceId: 'current-space'}
});
VocEducationPlatform.setHandler(host, async (request, {signal, files}) => {
  // 接入方校验真实权限、版本与业务规则，再返回明确回执。
  const result = await businessAdapter(request, {signal, files});
  return result; // {ok:true} 或 {ok:false,message,fieldErrors?}
});
```

正式动作回传voc:submit，包含component/action/value/context/requestId。未配置处理器时保持等待，不制造成功。也可监听请求后以resolve(host,requestId,{ok:true})确认。cancel、替换配置、关联目录变化和destroy使旧请求失效，过期回执不会改写新数据。expectedRevision供服务端做并发校验；客户端请求号不等于服务端事务或幂等键。

getValue/getState返回副本；getFiles保留实际File引用，上传由业务适配。setData整体替换配置并清除本地草稿、文件和请求；适用于明确切换记录。updateDirectory只更新该组件声明的关联目录，保留业务值、附件、弹窗输入和历史快照，取消旧请求并在下一次提交重新校验。禁止通过目录更新替换身份和业务记录。importRecords按稳定ID追加，重复ID内容不同时报错，不覆盖已有草稿。

role/actorId/scopeOwnerIds用于界面分工，实际数据必须由服务端按权限裁剪。scopeOwnerIds省略表示接入方提供的授权记录，空数组表示没有范围。个人成长数据由调用方提供当前人的集合；指导端修改个人目标或计划须显式managePersonal:true。学生视图剔除岗位草稿、他人的投递和联系方式、未公布成绩与其他私有记录；设备冲突仅保留不含借用人信息的占用切片。

支持setLoader/load/resolveLoad；加载成功返回{props}，失败返回{error}，无权限返回{forbidden:true}。多次加载、切换身份和卸载均按请求代次处理。now是可选ISO业务时钟，演示配置使用固定时间以便复核边界；真实页面可省略。

## 显式的跨组件关联

VocBusinessBridge不会按全局ID自动寻找组件。只对已挂载的指定host建立关系：

```js
const bridge = VocBusinessBridge.create([
  {id:'goal-plan', kind:'goals-to-plan', source:goalHost, target:planHost},
  {id:'task-plan', kind:'tasks-to-plan', source:taskHost, target:planHost,
    options:{mergeReferences:true}}
], {onUpdate: item => renderLinkStatus(item)});
bridge.syncAll();
// 用户核对冲突后才按需 sync(id,{force:true})。
// 页面卸载前 bridge.disconnect(); VocUI.destroy(host);
```

| 链路 | 支持的kind及关键配置 | 传播与保护 |
| --- | --- | --- |
| 名册→对象→任务 | roster-to-audience、audience-to-task（taskId） | 只将授权班级中的在读学生加入可选目录；确认名单才传到草稿任务；转班不会重写已确认/已发布名单 |
| 目录、任教→任务 | curriculum-to-task（taskId）、assignment-to-task（assignmentId/taskId） | 校验学时；保留课程基础对象独立；发布检查任教状态及班级覆盖，单独选择的学生也纳入范围校验；确认弹窗期间更新也重新检查 |
| 目标、教学、学习→成长计划 | goals-to-plan、tasks-to-plan、learning-to-plan | 个人身份匹配；后两者可mergeReferences合并目录；重复ID不同内容阻断并回滚本次贡献，不污染健康来源 |
| 岗位→投递 | jobs-to-applications | 同步当前岗位可用性，只追加当前人的新草稿；固定简历/岗位版本快照保留，岗位关闭后阻止新提交 |
| 资源→佐证→指标 | resource-to-evidence、evidence-to-indicators | 已确认引用构成来源目录，实际审核版本构成佐证目录；来源撤回、材料作废/过期阻断新提交和审核，旧提交快照保留，审核核对提交时的佐证版本 |
| 借还↔报修 | assets-to-repairs、repairs-to-assets | 同步当前台账和未验收阻断，带循环保护；归还申报不释放库存，报修关闭不自动使设备可借 |
| 教师卷→作答卷 | paper-to-answer | 教师结构确认后传到空白作答；未提交草稿冲突需明确核对；已交卷、只读、禁用和组字中不覆盖；未公布答案剔除 |
| 批阅→成绩 | review-to-grade（attemptId可选、rowId/columnId必填） | 只取已确认批阅；null不当0，0保留；不同草稿值需核对；满分不同须显式scaleToColumn:true；只写成绩草稿，公布独立确认并记录分数来源版本 |

共14种显式关联。源组件未确认/等待、加载失败、无权限或正在中文组字时暂停传播。接收方保留输入，失效关联可见并在实际操作前重新校验。已发布记录受保护；force不能突破已交卷、已公布或权限限制。getPending/getLog用于展示待核对原因，日志不包含全部个人记录。指纹去重与循环保护防止同一确认无限传播。

七条演示链路可分别整体替换cards/links和稳定记录ID。联动实验室内置处理器明确标为本地模拟；可关闭模拟后手动回执，或模拟下一次失败。未在实验室中的组件仍通过公共参数及控制器复用，不能把示例ID当后台目录。

## 验证与交付范围

定向入口：examples/education-platform-checks.html、examples/education-integration-checks.html。前者覆盖九类/36配置、320px结构状态及普通增改流转；后者覆盖七条可配置链路、目录合并、快照、权限、异常、失败回执、取消、过期请求、实际File保留、中文输入、确认中目录变化及销毁。

源码为可配置HTML/CSS/JS交互组件。真实存储、上传、审核权限、投递发送、联系动作、录取、合同、设备控制和服务端并发事务需业务接入。本轮未对全部浏览器、触摸设备或完整无障碍认证作出验收结论。原业务工程的历史扫描快照差异保留记录，不修改原工程或重置来源快照。

## 本轮验证记录

- browser：45项通过 / 0项失败；data/education-2.7/browser.json
- integration：40项通过 / 0项失败；data/education-2.7/integration.json
- first-batch-regression：39项通过 / 0项失败；data/education-2.7/first-batch-regression.json
- second-batch-regression：49项通过 / 0项失败；data/education-2.7/second-batch-regression.json
- catalog-regression：36项通过 / 0项失败；data/education-2.7/catalog-regression.json
- common-regression：53项通过 / 0项失败；data/education-2.7/common-regression.json
- family-regression：53项通过 / 0项失败；data/education-2.7/family-regression.json
- unit：18项通过 / 0项失败；data/education-2.7/unit.json
- unit-regressions：70项通过 / 0项失败；data/education-2.7/unit-regressions.json
- static：75项通过 / 1项失败；data/education-2.7/static.json
