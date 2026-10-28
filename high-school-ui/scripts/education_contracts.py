"""Six first-batch vocational domain components, source and interaction contracts."""
DATA={
 'teaching-audience':('教学对象选择','classes/students/mixed，单选或多选、组织范围、搜索、复核和确认名单快照。',{'nodes':'{id,label,kind?,disabled?,children?}[]；班级节点kind=class','students':'{id,name,number?,classId,disabled?}[]','mode':'classes/students/mixed','multiple':'默认true','value':'{classIds:[],studentIds:[]}','scopeIds':'允许的组织子树ID','directoryVersion':'本次组织目录版本','allowEmpty':'允许确认空名单','snapshot':'既有已确认名单快照'}),
 'curriculum-plan':('教学目录与学时','理论/实训/理实结合课程，三层单元、增删排序移动、学时校验与教学目标关联。',{'mode':'theory/practice/blended','nodes':'{id,title,theoryHours?,practiceHours?,objectiveIds?,locked?,children?}[]','objectives':'{id,label}[]','totalHours':'可选的目标总学时','step':'学时步长，默认1'}),
 'teaching-task':('教学任务','可配置任务类型、卡片/列表、前置任务与检查项，明确草稿、发布、开始、完成、结束及逾期。',{'tasks':'{id,title,type,status?,description?,requirements?,dueAt?,prerequisiteIds?,checklist?,audienceSnapshot?,locked?}[]','types':'{id,label}[]，默认理论/实训/项目/作业','view':'cards/list','allowLate':'是否允许截止后开始或完成任务，默认false'}),
 'question-sheet':('题目与作答','单选、多选、判断、填空、简答；答题卡、标记、草稿、提交锁定、公布答案和教师试卷结构编辑。',{'questions':'{id,type,title,score,options?,blanks?,answer?,analysis?,maxLength?}[]','mode':'answer/review/author；author需role=teacher','layout':'all/single','value':'{题目ID:答案}；判断题为boolean','marked':'疑问题号ID数组','totalScore':'作者保存时核对总分','released':'业务已授权公布参考答案','submitted':'已有正式提交，作答锁定','allowIncomplete':'允许确认后提交未答完整试卷','endsAt':'作答截止ISO时间'}),
 'submission-review':('提交与批阅','学生成果说明与真实本地附件、版本快照、撤回重交，教师退回与评分确认，历史版本只读。',{'assignmentId':'业务任务ID','value':'{text}初始草稿','draftFiles':'既有附件引用数组','attempts':'{id,version,status,text,files,submittedAt?,grade?,feedback?,released?,rubricValues?}[]','maxScore':'满分，默认100','dueAt':'提交截止ISO时间','allowLate':'允许截止后提交','allowResubmit':'已评分后允许新提交，默认false','allowWithdraw':'截止前允许撤回待批阅提交，默认true','accept':'扩展名或MIME列表','maxFiles':'默认5个','maxFileSize':'默认10MB','requireText':'文字必填','requireFile':'附件必填','rubric':'可选的scoring-rubric配置，满分须一致','allowScoreOverride':'量规之外允许教师调整最终分','releaseFeedback':'教师确认时默认公布反馈'}),
 'scoring-rubric':('评分量规','等级/数值评分，权重与分项计分、作者维度编辑、范围校验、不适用排除和未评分保留。',{'criteria':'{id,title,description?,type?,weight?,max?,levels?,allowNA?}[]','method':'weighted/points','mode':'author/score/readonly','totalScore':'默认100','value':'{维度ID:number|null|"na"}','embedded':'嵌入批阅时隐藏独立确认栏'})
}
def upgrade(catalog,contracts,version):
 import copy
 known={c['key']:c for c in catalog}
 for key,(name,desc,params) in DATA.items():
  if key not in known:
   row=copy.deepcopy(known['list']);row.update(id='voc-'+key,key=key,name=name,category='高职教业务',evidence=[],evidenceMatches=0,evidenceType='domain-composition',sourcePattern='domain-composition');catalog.append(row);known[key]=row
  row=known[key];contracts[key]={**params,'title':'组件标题','description':'说明','role':'student/teacher；与业务授权配合','context':'业务对象上下文，仅作为请求载荷','readonly':'只读','disabled':'禁用编辑','state':'default/dirty/invalid/submitting/success/failed/loading/load-error/empty/forbidden/readonly/disabled','now':'可选ISO当前时间，用于业务时钟或确定性预览'}
  row.update(version=version,name=name,description=desc,implementationFiles=['js/education-controls.js','css/education-controls.css'],states=['default','dirty','invalid','submitting','success','failed','loading','load-error','empty','forbidden','readonly','disabled'],extensions=['2.5高职教第一批业务组件'],alignment={'reference':'当前平台教学、出卷、批阅与评价流程约束','kind':'domain-composition','standardVersion':version})
  row['api']={'render':f'VocUI.render("{key}", props)','mount':f'VocUI.mount(element,"{key}",props)','parameters':contracts[key],'events':['voc:change','voc:submit','voc:action'],'eventContract':'动作、请求编号、确认回执与真实File接口详见EDUCATION.md','parameterPolicy':'仅列实际支持配置；客户端交互不替代服务端权限。'}
  row['usage']={'recommended':desc,'avoid':'不把本地模拟、建议分、未确认提交或未公布数据当成正式业务结果。'}
