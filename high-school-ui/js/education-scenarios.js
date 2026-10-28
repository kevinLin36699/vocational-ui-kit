(()=>{
const nodes=[{id:'college-a',label:'信息工程学院',children:[{id:'major-a',label:'软件技术专业',children:[{id:'class-a',label:'软件2601班',kind:'class'},{id:'class-b',label:'软件2602班',kind:'class'}]}]},{id:'college-b',label:'智能制造学院',children:[{id:'class-c',label:'机电2601班',kind:'class'}]}];
const students=[{id:'s1',number:'260101',name:'林同学',classId:'class-a'},{id:'s2',number:'260102',name:'周同学',classId:'class-a'},{id:'s3',number:'260201',name:'陈同学',classId:'class-b'},{id:'s4',number:'260202',name:'张同学',classId:'class-b',disabled:true},{id:'s5',number:'260301',name:'李同学',classId:'class-c'}];
const questions=[{id:'q1',type:'single',title:'下面哪项适合作为程序中的唯一标识？',score:10,options:[{id:'a',label:'稳定且唯一的编号'},{id:'b',label:'可能重复的显示名称'}],answer:'a',analysis:'显示名称可能重复，关联数据应使用稳定标识。'},{id:'q2',type:'multiple',title:'提交成果之前，应检查哪些内容？',score:20,options:[{id:'a',label:'任务要求'},{id:'b',label:'附件版本'},{id:'c',label:'忽略评分标准'}],answer:['a','b']},{id:'q3',type:'boolean',title:'暂存草稿等同于正式提交。',score:10,answer:false,analysis:'正式提交应经过明确确认并保留快照。'},{id:'q4',type:'fill',title:'请补全：学习记录应关联稳定的____，未评分应保留为____。',score:20,blanks:['关联标识','未评分值'],answer:[['ID','标识'],['null','空值']]},{id:'q5',type:'text',title:'说明如何核对任务要求与交付成果。',score:40,answer:'可说明交付清单、版本核对与评分标准。',maxLength:2000}];
const criteria=[{id:'quality',title:'成果完整性',description:'对照任务要求核对交付内容。',type:'level',max:100,weight:60,levels:[{id:'excellent',label:'完整且可核验',score:100,description:'交付项齐全并有证据。'},{id:'partial',label:'部分完成',score:60,description:'存在缺项或依据不足。'},{id:'missing',label:'未体现',score:0,description:'没有对应成果。'}]},{id:'reflection',title:'过程说明与反思',type:'number',max:20,weight:40,allowNA:true}];
const attempts=[{id:'attempt-v1',version:1,status:'returned',text:'首次成果说明，尚缺少测试记录。',files:[],feedback:'请补充测试依据。',grade:null,released:true,submittedAt:'2026-10-26T10:00:00+08:00'},{id:'attempt-v2',version:2,status:'submitted',text:'补充了测试记录与成果说明，请复核。',files:[{id:'evidence',name:'测试记录.txt',size:128}],submittedAt:'2026-10-27T14:00:00+08:00'}];
const curriculum=[{id:'unit-a',title:'项目准备',children:[{id:'lesson-a',title:'任务理解',theoryHours:4,practiceHours:0,objectiveIds:['obj-a']},{id:'lesson-b',title:'工具与方案',theoryHours:4,practiceHours:4,objectiveIds:['obj-b']}]},{id:'unit-b',title:'项目实施与复盘',theoryHours:0,practiceHours:4,objectiveIds:['obj-b']}];
const tasks=[{id:'task-a',title:'阅读任务要求',type:'theory',status:'completed',description:'核对任务背景与交付范围。',checklist:[]},{id:'task-b',title:'完成项目成果',type:'practice',status:'in-progress',description:'提交可核对的成果与过程说明。',requirements:'交付成果、测试记录与反思说明。',dueAt:'2026-10-30T17:00',prerequisiteIds:['task-a'],checklist:[{id:'c1',label:'检查成果文件',required:true,done:false},{id:'c2',label:'补充测试与反思',required:true,done:false}]},{id:'task-c',title:'整理学习反思',type:'assignment',status:'published',description:'说明本次学习的收获与待改进项。',dueAt:'2026-10-27T18:00',checklist:[]}];
const now='2026-10-28T09:00:00+08:00',scenes=[
['teaching-audience','混合选择与名单快照',{nodes,students,value:{classIds:['class-a'],studentIds:[]},mode:'mixed',directoryVersion:'2026-fall-v1'}],
['teaching-audience','单选班级与组织范围',{nodes,students,scopeIds:['college-a'],mode:'classes',multiple:false}],
['teaching-audience','学生单选与禁用项',{nodes,students,mode:'students',multiple:false}],
['curriculum-plan','理实结合与目标关联',{mode:'blended',totalHours:16,step:1,nodes:curriculum,objectives:[{id:'obj-a',label:'理解项目要求'},{id:'obj-b',label:'完成实施与验收'}]}],
['curriculum-plan','理论课与半学时',{mode:'theory',totalHours:6,step:.5,nodes:[{id:'u1',title:'基础概念',theoryHours:2.5,practiceHours:0},{id:'u2',title:'案例分析',theoryHours:3.5,practiceHours:0}]}],
['curriculum-plan','实训课与锁定单元',{mode:'practice',totalHours:8,nodes:[{id:'u1',title:'安全与准备',practiceHours:2,locked:true},{id:'u2',title:'项目实训',practiceHours:6}]}],
['teaching-task','学生任务与前置检查',{role:'student',tasks,now}],
['teaching-task','教师草稿与发布',{role:'teacher',now,tasks:[{id:'draft-a',title:'项目验收任务',type:'project',description:'核对成果、测试和说明。',requirements:'按交付清单准备成果。',status:'draft',dueAt:'2026-11-01T17:00',checklist:[]},...tasks]}],
['teaching-task','列表与逾期状态',{role:'student',view:'list',tasks,now}],
['question-sheet','五类题型与答题卡',{questions,role:'student',layout:'all',totalScore:100,now,paperId:'paper-a'}],
['question-sheet','逐题作答与未答确认',{questions,role:'student',layout:'single',allowIncomplete:true,now}],
['question-sheet','教师出题与结构编辑',{questions,role:'teacher',mode:'author',totalScore:100}],
['question-sheet','公布后只读复核',{questions,role:'student',mode:'review',released:true,value:{q1:'a',q2:['a','b'],q3:false,q4:['ID','null'],q5:'先对照要求，再核对版本和证据。'}}],
['question-sheet','截止锁定与草稿保留',{questions,role:'student',endsAt:'2026-10-27T17:00:00+08:00',value:{q1:'a',q3:false},now}],
['submission-review','学生成果与本地附件',{assignmentId:'assignment-a',role:'student',maxScore:100,dueAt:'2026-11-01T17:00',accept:'.txt,.md,.pdf',requireText:true,maxFiles:3,now,value:{text:'这是本次项目的成果说明。'}}],
['submission-review','退回后重交版本',{assignmentId:'assignment-a',role:'student',maxScore:100,attempts:attempts.slice(0,1),dueAt:'2026-11-01T17:00',now}],
['submission-review','教师批阅与量规联动',{assignmentId:'assignment-a',role:'teacher',maxScore:100,attempts,releaseFeedback:true,rubric:{criteria,method:'weighted',totalScore:100},now}],
['submission-review','历史评分与零分保留',{role:'student',maxScore:100,attempts:[{id:'graded-a',version:1,status:'graded',text:'已确认的提交快照',files:[],grade:0,feedback:'本次成果未达到评分项要求。',released:true}],now}],
['scoring-rubric','等级与数值加权评分',{criteria,method:'weighted',mode:'score',totalScore:100}],
['scoring-rubric','评分标准作者编辑',{criteria,method:'weighted',mode:'author',totalScore:100,role:'teacher'}],
['scoring-rubric','分项计分与不适用',{method:'points',mode:'score',totalScore:100,criteria:[{id:'content',title:'内容质量',type:'number',max:70,weight:0},{id:'format',title:'呈现规范',type:'number',max:30,weight:0,allowNA:true}]}],
['scoring-rubric','只读评分复核',{criteria,method:'weighted',mode:'readonly',value:{quality:60,reflection:0},totalScore:100}]
];window.VocEducationScenarios=scenes.map(([component,title,props],i)=>({id:'edu-case-'+i,component,title,props}));window.VocEducationFixtures={nodes,students,questions,criteria,attempts,curriculum,tasks,now};
})();
