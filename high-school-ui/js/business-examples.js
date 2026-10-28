/* Documentation fixtures and mock acknowledgements only. Never a public runtime dependency. */
(() => {
'use strict';
const clone=x=>JSON.parse(JSON.stringify(x)),U=window.VocUI,F=window.VocEducation,N=window.VocEducationNext;
const batches=[{id:'education',name:'教学业务示例',number:1,scenes:window.VocEducationScenarios||[]},{id:'education-next',name:'教学过程示例',number:2,scenes:window.VocEducationNextScenarios||[]},{id:'education-platform',name:'成长与运营示例',number:3,scenes:window.VocEducationPlatformScenarios||[]}];
const guides={
 'teaching-audience':'试选另一个班级或学生，复核名单后点击“确认教学对象”，查看已确认名单快照。',
 'curriculum-plan':'调整末级单元的理论/实训学时，观察总学时校验，再核对并保存目录。',
 'teaching-task':'学生可完成检查项并登记任务完成；切换“教师草稿与发布”可编辑和发布草稿。',
 'question-sheet':'单选、多选、是非、填空和问答均有实际题干；填写后暂存或交卷，也可切换教师出题示例。',
 'submission-review':'已有成果说明可直接修改、暂存和提交；切换教师示例可查看第二版成果并使用量规批阅。',
 'scoring-rubric':'给成果完整性选等级，并填写过程说明分数；观察加权总分、未评分和零分的区别。',
 'class-roster':'查看在读、休学和锁定成员，编辑成员资料或登记转班及原因，核对异动历史。',
 'teaching-assignment':'查看主讲、助教和已结束关系；可编辑草稿、启用任教或登记结束原因。',
 'practice-workflow':'安全步骤已有验收记录；继续检查设备步骤，填写证据、选择本地文件并提交验收。',
 'learning-progress':'选择视频或文档，记录实际位置，再按完成规则确认完成；续学定位不改变完成状态。',
 'resource-version':'查看资源不同版本并比较文本；教师可引用、撤回或发布，已有引用保留版本快照。',
 'evaluation-survey':'填写真实的选择、评分、是非和开放问题；切换结果示例可查看已配置的汇总数据。',
 'grade-detail':'编辑未公布学生的分项成绩，核对总评；零分、缺考、免修和未录入值分别展示。',
 'career-goal':'把“技能证书备考”设为主目标，观察旧主目标转为备选；也可编辑、归档和重新启用。',
 'growth-plan':'选择计划后增改草稿任务、调整顺序并启用；执行中的任务需要来源完成记录和完成依据。',
 'job-opportunity':'查看在招岗位和关闭岗位，收藏或创建投递草稿；切换管理示例可编辑、发布和关闭岗位。',
 'application-tracker':'投递草稿、面试记录已有岗位/简历快照；可编辑草稿、登记投递、添加跟进或撤回。',
 'assessment-collection':'数值0和是非“否”都是实际填报值；补充说明、关联已审核佐证后暂存或提交。',
 'evidence-material':'查看已审核的统计材料与待补充照片；选择材料版本、填写来源或创建下一版本。',
 'asset-loan':'查看已借出、待审批和已预约记录；登记审批、交付、归还与接收，观察容量及维护限制。',
 'repair-ticket':'选择新报修、处理中或待验收工单；可派单、记录处理过程和工时，再登记结果及验收。',
 'admissions-lead':'查看重复线索、撤回授权和逾期预约；登记人工跟进、更新阶段、分配责任人或核对合并。'
};
const fields={
 'teaching-audience':[['nodes','组织'],['students','学生']], 'curriculum-plan':[['nodes','教学单元'],['objectives','教学目标']],
 'teaching-task':[['tasks','教学任务']], 'question-sheet':[['questions','题目']], 'submission-review':[['attempts','历史提交']],
 'scoring-rubric':[['criteria','评分维度']], 'class-roster':[['classes','班级'],['records','成员']],
 'teaching-assignment':[['assignments','任教关系'],['teachers','教师']], 'practice-workflow':[['steps','实训步骤'],['materials','实训材料']],
 'learning-progress':[['chapters','学习章节']], 'resource-version':[['resources','资源'],['citations','引用快照']],
 'evaluation-survey':[['questions','问卷问题'],['responses','答卷']], 'grade-detail':[['rows','学生成绩'],['columns','成绩项']],
 'career-goal':[['goals','成长目标'],['types','目标类型']], 'growth-plan':[['plans','成长计划'],['taskDirectory','可关联任务']],
 'job-opportunity':[['jobs','岗位'],['resumes','简历版本']], 'application-tracker':[['applications','投递记录'],['jobs','岗位']],
 'assessment-collection':[['indicators','采集指标'],['evidence','佐证版本']], 'evidence-material':[['materials','佐证材料'],['sources','引用来源']],
 'asset-loan':[['assets','设备台账'],['loans','借用记录']], 'repair-ticket':[['tickets','报修工单'],['technicians','处理人员']],
 'admissions-lead':[['leads','招生线索'],['programs','意向专业']]
};
const raw=batches.flatMap(b=>b.scenes.map(s=>({...clone(s),batch:b.number}))),keys=[...new Set(raw.map(s=>s.component))];
function prepare(s){const p=clone(s.props),logic=s.batch===1?F.logic:N.logic;return {...clone(s),props:logic.publicConfig(s.component,logic.normalize(s.component,p))}}
function cases(key){return raw.filter(s=>s.component===key).map(prepare)}
function selected(key,id){const list=cases(key);return list.find(s=>s.id===id)||list[0]||null}
function describe(key,p){const entries=(fields[key]||[]).filter(([field])=>Array.isArray(p[field])).map(([field,label])=>({field,label,count:p[field].length}));if(key==='submission-review'&&p.value?.text)entries.push({field:'value.text',label:'成果草稿',count:1});return entries}
function controller(host){return N?.getState(host)?N:F?.getState(host)?F:null}
const bindings=new WeakMap();
function attach(root,{onEvent,shouldFail=()=>false}={}){bindings.get(root)?.abort();const abort=new AbortController();bindings.set(root,abort);for(const node of root.querySelectorAll('[data-edu],[data-en]')){const api=controller(node);if(!api)continue;api.setHandler(node,async(request,{signal})=>{await new Promise((resolve,reject)=>{const timer=setTimeout(resolve,300);signal.addEventListener('abort',()=>{clearTimeout(timer);reject(new DOMException('Cancelled','AbortError'))},{once:true})});return shouldFail()?{ok:false,message:'示例模拟：处理失败，输入已保留，可重试。'}:{ok:true,message:'示例本地回执已确认；未写入真实业务。'}})}if(onEvent)for(const type of ['voc:change','voc:submit','voc:action'])root.addEventListener(type,e=>{if(e.detail&&keys.includes(e.detail.component))onEvent({event:type,...clone(e.detail)})},{signal:abort.signal});return ()=>{abort.abort();bindings.delete(root)}}
function showDataset(host,key,props){let box=host.previousElementSibling?.matches('[data-business-dataset]')?host.previousElementSibling:null;if(!keys.includes(key)){box?.remove();return}const config=controller(host)?.getState(host)?.config||props;if(!box){box=document.createElement('section');box.dataset.businessDataset='true';box.className='business-example-data';host.before(box)}box.innerHTML=`<div class="story-example-counts">${describe(key,config).map(x=>`<span><strong>${x.count}</strong> ${U.escape(x.label)}</span>`).join('')}</div><p>${U.escape(guides[key])}</p><details><summary>查看载入的示例数据（JSON）</summary><pre>${U.escape(JSON.stringify(config,null,2))}</pre></details>`}
window.VocBusinessExamples={keys,cases,selected,describe,controller,attach,showDataset,guides:clone(guides),batches:batches.map(b=>({id:b.id,name:b.name,number:b.number,keys:[...new Set(b.scenes.map(s=>s.component))]}))};
})();
