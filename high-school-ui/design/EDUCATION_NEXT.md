# 高职教第二批业务组件 · v2.6.0

[第二批交互实验室](../examples/education-next.html)挂载七类公共业务组件，提供28组独立配置。目录总数109。第一批六类保留，见[EDUCATION.md](EDUCATION.md)。这一批覆盖前轮分类建议中的教学组织、实训、学习过程、资源版本和评价；成长就业、办学评估和学校运营尚未在本批实现。

公共实现为js/education-next.js、css/education-next.css；示例业务数据只在js/education-next-scenarios.js，不写入公共控制器。复用既有蓝白令牌、按钮、表单控件、对话框与业务容器。无构建、无CDN、无后端。普通使用者通过表单实际操作；实验室的JSON配置编辑器面向接入与评审。

## 类型、流程与规则

| 公共组件 | 类型 | 实际操作与业务状态 |
| --- | --- | --- |
| class-roster 班级名册 | 列表 / 卡片；班级 / 个人；授权范围 | 名称学号搜索、班级与在读/休学/退出筛选、当前名单CSV导出；添加、状态备注更新、转班及原因；异动历史、失效关联提示和锁定成员保护 |
| teaching-assignment 任教关系 | 主讲 / 助教；单班 / 多班 | 草稿新增编辑删除、启用、填写原因后结束；课程/教师/班级/学期独立关联，目录停用、重复任教和同班同学期主讲冲突校验 |
| practice-workflow 实训步骤与验收 | 安全 / 操作 / 检查 / 验收；顺序 / 依赖；设计 / 执行 | 设计步骤、检查项、材料与前置关系；学生开始、核对、真实File证据、暂存、提交；教师验收或填原因退回；未开始/进行中/待验收/已退回/已验收及历史快照 |
| learning-progress 学习进度与续学 | 文档 / 视频 / 任务；阈值 / 手动完成 | 章节定位、前置限制、续学事件、本次位置记录、明确确认完成和可选重置；未学/学习中/已完成；进度不当作学习掌握度，不自动完成 |
| resource-version 资源版本与引用 | 文本 / 文档引用 / 链接 | 新资源、草稿版本新增编辑、发布锁定、理由停用；草稿/可用/过期/不可用；版本切换、按文本行对照、确认引用、移除引用和源版本失效提示 |
| evaluation-survey 评价问卷 | 单选 / 多选 / 量表 / 是非 / 文本；作者 / 作答 / 汇总 | 题目与选项、必答、最多选择数、量表刻度、排序删除；保存结构、开放、关闭与配置允许的重开；暂存、提交、答卷修订、原始答卷过滤与独立汇总公布 |
| grade-detail 成绩明细 | 权重 / 分项计分；分数 / 未评 / 缺考 / 免修；规则作者 / 录分 / 只读 | 成绩项编辑、分项录入、反馈、个人草稿、所选成绩批量公布、原因撤回、历史快照与当前CSV导出；学生只见自身已公布数据 |

- 所有项目使用稳定唯一ID，沿用字母、数字、下划线、短横线格式，拒绝重复和原型链保留名。姓名、课程标题和学号显示字段不作为对象ID。
- 课程基础目录只包含课程身份；任教关系单独携带termId/classIds/teacherId/courseId，不把学期或班级塞入课程基础对象。主讲冲突范围为同课程、同学期、交集班级；助教可并行，完全相同教师关系不能重复启用。
- 名册转班修改当前班级，保留fromClassId/toClassId、原因和时间。目录更新不回写既有人员历史；失效目录明确提示，不能据此保存新关联。已锁定人员与班级范围受保护。退出采用状态，不物理删除历史人员。
- 实训顺序模式要求之前必需步骤验收；安全步骤始终是后续步骤的前置。显式prerequisiteIds在两种模式下均生效，拒绝循环。材料和检查项可以配置必需/可选，默认必需。所有提交快照保留当时证据与附件元数据；退回不会改写旧快照。开始过的流程锁定设计结构。
- 文档位置按页、视频按秒、任务按项，整数0—total。定位续学只发出定位事件，不伪造访问、播放或进度。进度经回执确认后仍为学习中；确认完成需达到配置阈值，或采用manual规则。完成后锁定位置，明确重置后才可重学。
- 资源发布后正文不可原地编辑，新内容创建递增正整数版本。引用包含资源ID、版本ID、版本号、名称、正文/链接与引用时间，后续发布不改旧快照。不可用或过期版本不能新引用；旧引用保留并提示来源状态。文本对照按对应行比较，不声称完成PDF/Word二进制差异分析。
- 问卷false与量表0在允许刻度内是有效值。多选数量、选项ID、必答、时间窗和提交锁定均参与校验。开放后锁定结构；修订保留版本编号，新的正式提交才增加revision。汇总来自已授权的有效答卷，没有答卷时均值为null，显示“—”，不填0。
- 成绩null/空值是未评，0是已评零分；absent默认待处理，仅absentAsZero=true才记0；exempt需成绩项allowExempt=true，排除分母后折算。全部免修或尚未完成时总分null。weighted权重合计100%；points分项满分合计等于totalScore。公布使用当前实际计算值，并保留分项、反馈、总分与版本快照；已公布不可直接改分，先填原因撤回。

## 挂载与数据配置

按data/library.json的styles与runtime顺序加载，使用公共渲染器，不运行实验室控制器。

```javascript
VocUI.mount(host, 'learning-progress', {
  title: '设备维护学习计划', role: 'student',
  completion: 'threshold', threshold: 100, allowReset: true,
  chapters: [{id:'ch-01', title:'安全准备', resources:[
    {id:'manual-01', title:'安全手册', type:'document', total:12,
     prerequisiteIds:[], locator:{documentId:'current-manual'}}
  ]}], records: {}, context: {courseId:'current-course'}
});
host.addEventListener('voc:action', event => {
  if (event.detail.action === 'learning-locate') {
    // 接入当前业务的文档、视频或任务定位；组件不会伪造资源已打开。
    openBusinessResource(event.detail.value);
  }
});
```

七类参数完整矩阵见[API.md](API.md)与data/control-contracts.json。常用数据结构如下：

| 组件 | 主要配置 |
| --- | --- |
| class-roster | classes:{id,label,active?,disabled?}[]；records:{id,name,number,classId,status?,note?,locked?,history?}[]；classId；view:list/cards；scopeClassIds；studentId；directoryVersion |
| teaching-assignment | teachers/courses/classes/terms均为{id,label,active?,disabled?}[]；assignments:{id,teacherId,courseId,classIds,termId,hours,duty:primary/assistant,status:draft/active/ended,locked?}[]；scopeClassIds；directoryVersion |
| practice-workflow | steps:{id,title,type,description?,prerequisiteIds?,materialIds?,checks:{id,label,required?}[],required?,requireEvidence?,requireFile?,locked?}[]；materials:{id,label,quantity?,unit?,required?}[]；value:{步骤ID:{status,checks,materialChecks,evidence,files,history}}；mode:run/author；sequential；dueAt/allowLate；accept/maxFiles/maxFileSize |
| learning-progress | chapters:{id,title,resources:{id,title,type:document/video/task,total,prerequisiteIds?,locator?,disabled?,locked?}[]}[]；records:{资源ID:{position,status,lastVisitedAt?,history?}}；completion:threshold/manual；threshold；allowReset |
| resource-version | resources:{id,title,type:text/document/link,locked?,versions:{id,number,status,content?,url?,note?,createdAt?,expiresAt?,reason?}[]}[]；citations:{id,resourceId,versionId,versionNumber,title,content?,url?,referencedAt}[] |
| evaluation-survey | questions:{id,title,type,required?,options?,maxChoices?,min?,max?,scaleLabels?,maxLength?}[]；mode:respond/author/results；status:draft/open/closed；answers；responses:{id,answers}[]；surveyId/studentId；anonymous；startsAt/endsAt；submitted/revision；allowRevise/allowReopen；released/aggregate |
| grade-detail | columns:{id,label,max,weight?,allowExempt?}[]；rows:{id,name,number?,classId?,scores,status:draft/published,feedback?,version?,history?,locked?}[]；method:weighted/points；totalScore；mode:score/author/readonly；studentId；scopeClassIds；absentAsZero |

所有组件支持title、description、context、role:student/teacher/admin、state、readonly、disabled和可选ISO业务时钟now。指定now时由业务调用setNow推动时钟；未指定时，问卷截止、实训截止与资源到期通过页面实际时钟刷新，不自动提交任何业务。

## 状态、草稿与确认回执

统一状态：default、dirty、invalid、submitting、success、failed、loading、load-error、empty、forbidden、readonly、disabled。

- 正常交互由真实操作产生dirty/invalid/submitting/success/failed；loading/load-error用于读取，失败保留草稿并提供重试。
- readonly/disabled禁止业务改动，保留已授权内容的筛选、查看、定位或导出。forbidden移除可见业务正文。空态由空数据或state=empty提供，不回退固定示例。
- 弹窗校验失败保留输入；未确认输入关闭前提示放弃，继续编辑不会清空。输入法组字期间不提交旧值，不重绘正在组字的输入。
- 正式业务操作需显式回执，等待时锁定重复操作。无处理器不会自动成功。保存失败保留当前草稿，目录异动、验收、引用、成绩公布不会提前写入正式记录。

```javascript
const V = VocEducationNext;
V.setHandler(host, async (request, {signal, requestId, files}) => {
  // request = {component, action, value, context, requestId}
  // files包含当前页面所有步骤真实File；可通过getFiles(host,stepId)精确读取。
  const result = await saveToBusiness(request, {signal, requestId, files});
  return {ok: result.ok, message: result.message, fieldErrors: result.fieldErrors};
});
```

只有{ok:true}才应用正式转换；{ok:false,message?,fieldErrors?}或抛错显示失败。回执不接受任意覆盖分数、资源版本或学生身份；业务如需刷新正式数据，另行setData。事件模式收到voc:submit的requestId后调用：

```javascript
VocEducationNext.resolve(host, requestId, {ok:true, message:'业务已确认'});
```

取消、关闭已确认放弃的弹窗、切换内容状态、setData、目录更新或destroy中断本地等待并发送AbortSignal。迟到请求编号不再生效。服务端的幂等、并发冲突、版本核对、取消与回滚需要自行实现，前端取消不代表后端撤销成功。

## 公共实例接口

- VocUI.mount/render/hydrate/destroy：公共组件生命周期；VocUI.getValue识别七类当前业务值。
- VocEducationNext.getValue(host)：值副本。名册={records}；任教={assignments}；实训={steps}；学习={records}；资源={resources,citations}；问卷={questions,answers,status,submitted,revision,responses}；成绩={rows}。
- getState(host)：component、config、value、status、errors、dirty、drafts、pending、loading、requestId与真实文件元数据。学习尚未确认的位置放在drafts，不伪装成已确认记录。
- setData(host,props)：校验并替换完整业务配置，中断旧请求并建立新基线。调用前由业务明确处理放弃当前草稿。
- setState(host,state,message?)：切换适用状态，取消旧等待，关闭所属编辑弹窗。
- setHandler(host,fn|null)、resolve(host,requestId,result)、cancel(host)：正式变更的处理器、编号回执与本地取消。
- setLoader(host,fn,{immediate?:true})、load(host)：fn({context},{signal,requestId})返回{props}；失败保留草稿，过期结果忽略。
- resolveLoad(host,requestId,{props?,error?,forbidden?})：事件模式读取回执。读取发出voc:action/action=load-request。
- setDirectory(host,patch)：仅名册/任教。接受classes、scopeClassIds、directoryVersion；任教另接受teachers/courses/terms。保留当前业务记录、人员历史和重置基线里的正式记录，失效关联需业务复核。
- setNow(host,ISO时间)：推进配置业务时钟；只刷新时间限制，不制造自动提交。
- getFiles(host,stepId?)：当前页面真实File对象数组；既有文件名与引用元数据不会伪造成File，也不代表文件上传完成。
- getScore(host,rowId)：成绩结果{score,complete,completed,applicable,errors}，未完成为null。

常用voc:submit动作：roster-add/update/transfer；assignment-save/activate/end/delete；practice-design/up/down/delete/start/save/submit/accept/return；learning-record/complete/reset；version-save/publish/withdraw、resource-cite/citation-remove；survey-save/open/close/draft/submit/revise/release；grade-save/publish/withdraw/rules-save。

voc:change用于草稿变化和确认后的action-confirmed，后者带confirmed=true；voc:action用于learning-locate、resource-open、file-open/file-unavailable、export、load-request、cancel、time-boundary。所有事件冒泡，detail含component/action/value/context/requestId。页面路由、文档打开和文件服务由业务接续；“请求打开”不会冒称外部资源已加载。

## 数据可见性与交付边界

学生成绩配置只保留studentId对应行；未公布时移除分值、反馈、历史与已公布总分。学生资源配置移除草稿和不可用/到期正文链接；问卷移除原始答卷，仅公布后提供统计。序列化配置在初始化后从DOM移除。这些是前端数据约束，正式服务必须按身份、组织与对象范围过滤数据，客户端role不是鉴权机制。

匿名问卷只表示组件提交载荷省略respondentId；后端日志、context、重复提交与匿名化策略需业务设计，不承诺不可追溯。问卷和成绩不会自动作出学籍、就业或其他高影响决定。

本轮交付可配置HTML交互组件，没有接入真实权限、数据库、文件上传、跨端同步、成绩发布或通知服务。实训不控制真实设备；学习组件不播放真实视频、不解析文档、不推断学习掌握度；资源对照只比较提供的文本。文件仅在当前页面内存，刷新后真实File引用丢失。示例回执明确标为本地模拟。没有完整浏览器、触摸设备、屏幕阅读器或全量视觉认证。

## 本轮验证记录

- browser：49项通过 / 0项失败；data/education-2.6/browser.json
- firstBatchRegression：39项通过 / 0项失败；data/education-2.6/first-batch-regression.json
- catalogRegression：36项通过 / 0项失败；data/education-2.6/catalog-regression.json
- commonRegression：53项通过 / 0项失败；data/education-2.6/common-regression.json
- familyRegression：53项通过 / 0项失败；data/education-2.6/family-regression.json
- unit：19项通过 / 0项失败；data/education-2.6/unit.json
- static：67项通过 / 1项失败；data/education-2.6/static.json

静态检查中的原工程历史扫描快照差异保留为失败；本轮仅修改组件库，不修改原工程或重置来源快照。检查通过范围以报告断言为准，不等于生产服务、全设备或全状态视觉认证。
