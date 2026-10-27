/* Templates reuse VocUI renderers; all data is fictitious and local to this page. */
(() => {
const U=window.VocUI,R=U.render,B=U.button,I=U.icon;
const patterns=[
['home','平台首页','TPL01','角色问候、常用入口、最近协作和输入；教师示例不加无依据的指标。',['agent','composer','card']],
['list','管理列表页','TPL02','标题、筛选、列表和分页同轴；查询、排序、选择、增改查删与导出贯通。',['toolbar','table','pagination','form','confirm']],
['detail','普通详情页','TPL03','单一对象标题、内容导航、来源返回及按需收放的 AI 助手。',['breadcrumb','tabs','description','chat']],
['edit','新建与编辑页','TPL04','字段分区、校验、依赖和保存；不把协作草稿当作业务数据。',['form','select','input','date']],
['selection','选择与关联页','CON/FORM11','稳定 ID、多选及级联；更换上级时清除失效值。',['person-picker','multiselect','cascade']],
['analytics','分析与仪表盘','TPL05','统计、图形和明细共用数据口径；不生成无依据的掌握率或排名。',['stat','chart','description']],
['history','协作记录','HIST01～10','会话搜索、重命名、置顶、删除与草稿隔离。',['conversation','menu','confirm']],
['chat','主平台 AI 协作','TPL06/CHAT','输入、过程、停止、失败、重试、引用和生成内容工作区。',['chat','process','result','workspace']],
['assistant','业务内嵌 AI 助手','LAY12/CHAT14','主体与助手分栏；收起完全释放空间，未发送输入仍保留。',['description','chat','button']],
['workspace','生成内容容器','AIC08～14','预留业务内容插槽，通用层只管理布局、收放与滚动。',['workspace','steps','resource']],
['learning','学习与作答','EDU/CON','学生作业期间限制当前助手，提交后恢复；此为组件组合示例。',['tabs','radio','alert','composer']],
['approval','审核与分发','OPS/AIC12','展示对象、状态和操作后果；演示流程不等同真实权限实现。',['approval','description','timeline']],
['files','资源与文件','FILE/TRN','选取和移除、大小类型校验、来源、版本及真实文本下载。',['upload','resource','alert']],
['settings','个人设置与配置','FORM/CON','配置只改本次页面草稿，保存和取消有明确含义。',['input','switch','avatar']]
].map(([id,name,rule,description,components])=>({id,name,rule,description,components,version:U.version,status:'implemented-template',maturity:'交互原型模板；不含真实权限、后台或模型服务'}));
const head=(title,desc,actions='')=>`<div class="pattern-page-head"><div><h1>${title}</h1><p>${desc}</p></div><div class="v-row">${actions}</div></div>`;
function page(id){switch(id){
case 'home':return `<section class="v-home"><header><p class="v-home-eyebrow">高职教 · 教学工作台</p><h1>你好，林老师</h1><p class="v-muted">从一个教学任务开始，组织课程、内容与课堂活动。</p></header>${R('composer')}<div class="v-grid">${[['智能备课','请整理人工智能基础教学大纲'],['创建课程','请准备课程基本信息'],['创建实训','请准备独立实训任务'],['AI 出卷','请准备课程考试要求']].map(([n,p])=>`<button class="v-card v-card-interactive v-ai-entry-card" data-pattern-prefill="${p}" type="button"><h3>${I('spark',17)} ${n}</h3><p>预填需求，确认后再发送</p></button>`).join('')}</div>${U.note('最近协作为空；开始协作后再显示实际记录，不填造历史数量。')}</section>`;
case 'list':return head('课程管理','统一管理普通课程。当前展示虚构示例数据，课程与实训分离。',B('导出当前筛选','table-export','outline','download')+B('创建课程','table-add','primary','plus'))+R('table');
case 'detail':return R('breadcrumb')+`<div style="margin-top:24px">${head('人工智能基础','课程 C001 · 信息工程学院',B('展开 AI 助手','pattern-assistant-toggle','soft','spark'))}</div>`+R('tabs')+R('description')+`<div data-pattern-detail-ai hidden style="margin-top:24px">${R('chat',{history:false})}</div>`;
case 'edit':return head('创建课程','填写课程基本信息；课程不绑定学期，不混入独立实训。')+R('form');
case 'selection':return head('关联教学对象','先确认人员和专业范围，再将选择应用到本次草稿。')+`<div class="v-stack">${R('person-picker')}${R('cascade')}${R('multiselect')}<div>${B('确认关联','pattern-selection-save','primary')}</div><div data-pattern-selection-feedback aria-live="polite"></div></div>`;
case 'analytics':return head('课程结构分析','范围：当前示例的 17 门课程；学院图形与明细同源。')+R('stat')+`<div class="v-card" style="margin-top:24px">${R('chart')}</div>`;
case 'history':return head('教学协作记录','切换会话恢复各自草稿；页面刷新后示例重置。')+R('conversation');
case 'chat':return head('教学 AI 协作','演示完整本地流程；通过会话标题栏“演示控制”选择下一轮失败场景。')+R('chat');
case 'assistant':return head('课程详情与学习助手','收放助手只改变布局，不清空正在编辑的内容。',B('收放助手','pattern-split-toggle','soft','spark'))+`<div class="pattern-split" data-pattern-split><section><h2>课程基本信息</h2>${R('description')}<hr class="v-separator"><label class="v-field">当前备注<textarea class="v-textarea" placeholder="收起助手后，这里保留输入"></textarea></label></section><aside data-pattern-side><h3>课程 AI 助手</h3>${R('chat',{history:false})}</aside></div>`;
case 'workspace':return head('生成内容工作区','预留内容区与可选操作栏，具体预览、编辑、版本及业务操作由页面接入。')+R('workspace');
case 'learning':return head('人工智能基础 · 课堂作业','此模板演示当前作业的助手限制，不模拟正式考试计分和离开规则。')+`<div data-pattern-learning><div class="v-alert" data-learning-guide><div class="v-grow">是否确认已经学完，开始写作业？</div>${B('确认开始作业','learning-start','primary')}</div><form data-learning-form hidden style="margin-top:24px"><fieldset style="padding:20px;border:1px solid var(--v-border);border-radius:var(--v-radius-card)"><legend>单项选择 · 每题 100 分（演示）</legend><p>以下哪项用于描述模型处理前的信息输入？</p>${['数据','界面颜色','按钮圆角'].map((n,i)=>`<label class="v-choice" style="display:flex;margin:10px 0"><input type="radio" name="answer" value="${i}" required>${n}</label>`).join('')}<p class="v-error" data-learning-error></p>${B('提交作业','learning-submit','primary')}</fieldset></form><div data-learning-result style="margin-top:20px" aria-live="polite"></div><div data-learning-ai style="margin-top:24px">${R('composer',{agentOptions:[]})}</div></div>`;
case 'approval':return head('教学内容审核','示例角色流程；正式系统需接入真实权限与状态校验。')+R('description')+'<hr class="v-separator">'+R('approval');
case 'files':return head('教学资源','示例上传限制仅作用于此组件展示，不覆盖三端真实业务限制。')+R('upload')+`<div style="margin-top:24px">${R('resource')}</div>`;
case 'settings':return head('个人设置','以下配置仅保留在当前页面，取消将恢复初始值。')+`<form data-pattern-settings><div class="v-stack">${R('avatar')}${U.input('显示名称',{value:'林老师',name:'displayName'})}${R('switch')}<div class="v-row">${B('取消修改','settings-reset','outline')}${B('保存设置','settings-save','primary')}</div><div data-settings-feedback aria-live="polite"></div></div></form>`;
default:throw Error('未知页面模式：'+id)}}
function mount(el,id){if(typeof el==='string')el=document.querySelector(el);U.destroy(el);el.innerHTML=page(id);el.dataset.pattern=id;U.hydrate(el)}
document.addEventListener('click',e=>{const b=e.target.closest('[data-v-action],[data-pattern-prefill]');if(!b)return;const root=b.closest('[data-pattern]');if(!root)return;if(b.dataset.patternPrefill){const input=root.querySelector('textarea');if(input.value.trim()&&!confirm('替换尚未发送的需求？'))return;input.value=b.dataset.patternPrefill;input.dispatchEvent(new Event('input',{bubbles:true}));input.focus();return}const a=b.dataset.vAction;
if((a==='table-export'||a==='table-add')&&!b.closest('[data-v-table]')){const target=root.querySelector('[data-v-table]'),clone=b.cloneNode(true);clone.hidden=true;target.append(clone);clone.click();clone.remove()}
if(a==='pattern-assistant-toggle'){const side=root.querySelector('[data-pattern-detail-ai]');side.hidden=!side.hidden;b.textContent=side.hidden?'展开 AI 助手':'收起 AI 助手';b.setAttribute('aria-expanded',!side.hidden)}
if(a==='pattern-split-toggle'){const area=root.querySelector('[data-pattern-split]'),side=root.querySelector('[data-pattern-side]');side.hidden=!side.hidden;area.style.gridTemplateColumns=side.hidden?'minmax(0,1fr)':'';b.setAttribute('aria-expanded',!side.hidden)}
if(a==='pattern-selection-save'){const selected=[...root.querySelectorAll('input[type=hidden]')].map(x=>[x.name,x.value]).filter(x=>x[1]);root.querySelector('[data-pattern-selection-feedback]').innerHTML=selected.length?U.note('已关联到本次草稿：'+selected.map(x=>x[0]+' = '+x[1]).join('；'),'success'):U.note('请先选择至少一个关联对象。','warning')}
if(a==='learning-start'){root.querySelector('[data-learning-guide]').hidden=true;root.querySelector('[data-learning-form]').hidden=false;root.querySelector('[data-learning-ai]').innerHTML=U.render('composer',{disabled:true,agentOptions:[]});root.querySelector('[data-learning-ai]').insertAdjacentHTML('afterbegin',U.note('作业期间当前助手暂停提问，提交后恢复。','warning'));U.hydrate(root)}
if(a==='learning-submit'){const f=root.querySelector('[data-learning-form]'),answer=f.querySelector('[name=answer]:checked');if(!answer){f.querySelector('[data-learning-error]').textContent='请选择一个选项后提交。';return}f.hidden=true;root.querySelector('[data-learning-result]').innerHTML=U.note(answer.value==='0'?'本次得分：100 分。':'本次得分：0 分；关注知识点：数据与模型输入。','success');root.querySelector('[data-learning-ai]').innerHTML=U.render('composer',{agentOptions:[]});U.hydrate(root)}
if(a==='settings-reset'){const f=root.querySelector('form');f.reset();const sw=f.querySelector('[role=switch]');sw.setAttribute('aria-checked',false);sw.nextElementSibling.textContent='关闭 · 保存后生效';f.querySelector('[data-settings-feedback]').innerHTML=U.note('已恢复示例初始设置。')}
if(a==='settings-save'){const f=root.querySelector('form'),name=f.querySelector('[name=displayName]').value.trim();f.querySelector('[data-settings-feedback]').innerHTML=U.note(name?'已保留本次页面设置：'+name:'显示名称不能为空。',name?'success':'danger')}
});
window.VocPatterns={version:U.version,list:patterns,render:page,mount};
})();
