/* Editable whole-flow configurations. These are illustrative records, not business defaults. */
(() => {
const C=x=>JSON.parse(JSON.stringify(x)),F=VocEducationPlatformFixtures,A=VocEducationFixtures,B=VocEducationNextFixtures,P=(S,key,i=0)=>C(S.filter(x=>x.component===key)[i].props),S1=VocEducationScenarios,S2=VocEducationNextScenarios,S3=VocEducationPlatformScenarios;
const flows=[];
flows.push({id:'teaching',title:'名册、任教与教学任务',description:'更新名册目录，确认教学对象名单，再把学时与任教快照交给草稿任务；发布后的任务保留原快照。',cards:[
 {id:'roster',label:'第二批 · 班级名册',key:'class-roster',props:P(S2,'class-roster')},
 {id:'audience',label:'第一批 · 教学对象',key:'teaching-audience',props:{role:'teacher',nodes:[],students:[],value:{classIds:[],studentIds:[]},now:F.now}},
 {id:'curriculum',label:'第一批 · 教学目录与学时',key:'curriculum-plan',props:P(S1,'curriculum-plan')},
 {id:'assignment',label:'第二批 · 任教关系',key:'teaching-assignment',props:P(S2,'teaching-assignment')},
 {id:'tasks',label:'第一批 · 教学任务',key:'teaching-task',props:{role:'teacher',now:F.now,tasks:[{id:'flow-task',title:'目录与对象联动教学任务',type:'project',status:'draft',description:'核对对象、任教范围与教学目录快照后发布。',requirements:'依据交付清单准备成果。',checklist:[]}]}}
 ],links:[{id:'roster-audience',kind:'roster-to-audience',source:'roster',target:'audience'},{id:'audience-task',kind:'audience-to-task',source:'audience',target:'tasks',options:{taskId:'flow-task'}},{id:'curriculum-task',kind:'curriculum-to-task',source:'curriculum',target:'tasks',options:{taskId:'flow-task'}},{id:'assignment-task',kind:'assignment-to-task',source:'assignment',target:'tasks',options:{taskId:'flow-task',assignmentId:'a1'}}]});
flows.push({id:'growth',title:'目标、学习与成长计划',description:'教学任务和学习资源合并为可关联目录。完成来源任务后仍需登记个人任务依据，成长计划不会自动完成。',cards:[
 {id:'goals',label:'第三批 · 成长目标',key:'career-goal',props:P(S3,'career-goal')},
 {id:'teaching-task',label:'第一批 · 学生教学任务',key:'teaching-task',props:{role:'student',actorId:F.learner,now:F.now,tasks:[{id:'teach-task1',title:'设备巡检实训',type:'practice',status:'in-progress',description:'完成安全检查与巡检记录。',prerequisiteIds:[],checklist:[{id:'check-safe',label:'核对安全防护',required:true,done:false}]}]}},
 {id:'learning',label:'第二批 · 学习进度',key:'learning-progress',props:{...P(S2,'learning-progress'),actorId:F.learner}},
 {id:'plans',label:'第三批 · 成长计划',key:'growth-plan',props:{...P(S3,'growth-plan'),plans:[{...C(F.plans[0]),status:'active',tasks:[{...C(F.plans[0].tasks[0]),status:'in-progress'},{id:'learn-plan-task',title:'完成巡检视频学习',linkedTaskId:'res2',status:'pending',requireEvidence:true,revision:0,history:[]}]}]}}
 ],links:[{id:'goals-plans',kind:'goals-to-plan',source:'goals',target:'plans'},{id:'tasks-plans',kind:'tasks-to-plan',source:'teaching-task',target:'plans',options:{mergeReferences:true}},{id:'learning-plans',kind:'learning-to-plan',source:'learning',target:'plans',options:{mergeReferences:true}}]});
flows.push({id:'employment',title:'岗位与投递快照',description:'创建岗位投递草稿后追加到投递进度，保留简历与岗位版本；后续登记投递、面试和意向各有独立回执。',cards:[
 {id:'jobs',label:'第三批 · 岗位目录',key:'job-opportunity',props:P(S3,'job-opportunity')},
 {id:'applications',label:'第三批 · 投递进度',key:'application-tracker',props:{...P(S3,'application-tracker'),applications:[]}}
 ],links:[{id:'jobs-applications',kind:'jobs-to-applications',source:'jobs',target:'applications'}]});
const resource=P(S2,'resource-version',1),evidence={...P(S3,'evidence-material',1),sources:[],materials:[{...C(F.materials[0]),versions:[{...C(F.materials[0].versions[0]),status:'in-review',sourceId:resource.citations[0].id,sourceSnapshot:{id:resource.citations[0].id,label:resource.citations[0].title,version:resource.citations[0].versionNumber}}]}]};
flows.push({id:'assessment',title:'资源、佐证与评估采集',description:'已确认资源引用成为佐证来源，佐证审核通过后进入指标可选目录。失效或作废会阻止新提交，已提交快照保持原样。',cards:[
 {id:'resources',label:'第二批 · 资源版本与引用',key:'resource-version',props:resource},
 {id:'evidence',label:'第三批 · 佐证材料审核',key:'evidence-material',props:evidence},
 {id:'indicators',label:'第三批 · 指标填报',key:'assessment-collection',props:{...P(S3,'assessment-collection'),indicators:[C(F.indicators[0])],evidence:[]}}
 ],links:[{id:'resource-evidence',kind:'resource-to-evidence',source:'resources',target:'evidence'},{id:'evidence-indicators',kind:'evidence-to-indicators',source:'evidence',target:'indicators'}]});
flows.push({id:'operations',title:'设备借还与报修',description:'设备台账同步到报修目录；未验收工单按配置阻止新分配。归还申报不释放库存，接收损坏设备转维护；关闭工单不自动恢复设备。',cards:[
 {id:'loans',label:'第三批 · 设备借还',key:'asset-loan',props:P(S3,'asset-loan')},
 {id:'repairs',label:'第三批 · 报修工单',key:'repair-ticket',props:P(S3,'repair-ticket')}
 ],links:[{id:'assets-repairs',kind:'assets-to-repairs',source:'loans',target:'repairs'},{id:'repairs-assets',kind:'repairs-to-assets',source:'repairs',target:'loans'}]});
flows.push({id:'paper',title:'教师试卷与学生作答',description:'教师保存结构后更新空白作答卷。学生已有草稿时会提示核对，正式提交后的作答不会被新试卷覆盖。未公布答案会从学生配置移除。',cards:[
 {id:'author',label:'第一批 · 教师试卷结构',key:'question-sheet',props:P(S1,'question-sheet',2)},
 {id:'answer',label:'第一批 · 学生作答',key:'question-sheet',props:P(S1,'question-sheet')}
 ],links:[{id:'paper-answer',kind:'paper-to-answer',source:'author',target:'answer'}]});
flows.push({id:'grading',title:'批阅与成绩草稿',description:'教师确认批阅后，将真实分数放入指定学生成绩项。已有不同分值时需明确核对；成绩公布仍在成绩组件单独确认。',cards:[
 {id:'review',label:'第一批 · 提交批阅与量规',key:'submission-review',props:P(S1,'submission-review',2)},
 {id:'grades',label:'第二批 · 成绩明细',key:'grade-detail',props:{...P(S2,'grade-detail'),rows:[{...C(B.gradeRows[0]),scores:{process:80,practice:null,reflection:10}}]}}
 ],links:[{id:'review-grade',kind:'review-to-grade',source:'review',target:'grades',options:{rowId:'s1',columnId:'practice'}}]});
window.VocEducationIntegrationScenarios=C(flows);
})();
