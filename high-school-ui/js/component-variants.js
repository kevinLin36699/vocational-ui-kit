/* Every example mounts the same public renderer used by authored pages. */
(() => {
const item=(title,key,props={},note='')=>({title,key,props,note});
const temporal=[
 item('单个日期','date-picker',{label:'会议日期',value:'2026-10-27'}),
 item('日期范围','date-range',{label:'统计区间',value:['2026-10-01','2026-10-31']}),
 item('单个时间','time-picker',{label:'上课时间',value:'09:30'}),
 item('时间范围','time-range',{label:'开放时间',value:['08:30','17:00']}),
 item('日期与时间','datetime-picker',{label:'报名截止',value:'2026-10-27 18:30'}),
 item('日期时间范围','datetime-range',{label:'活动起止',value:['2026-10-27 09:00','2026-10-28 17:30']}),
 item('选择年份','year-picker',{label:'统计年度',value:'2026'}),
 item('选择月份','month-picker',{label:'统计月份',value:'2026-10'}),
 item('选择季度','quarter-picker',{label:'统计季度',value:'2026-Q4'}),
 item('选择一周','week-picker',{label:'值班周次',value:'2026-W44'},'按 ISO 周，周一至周日；跨年周使用周所属年份。'),
 item('多选日期','multi-date',{label:'授课日期',value:['2026-10-12','2026-10-15','2026-10-20','2026-10-27','2026-10-29']}),
 item('月份范围','month-range',{label:'学期月份',value:['2026-09','2027-01']}),
 item('年份范围','year-range',{label:'年度对比',value:['2024','2026']}),
 item('秒级时间','time-picker',{label:'精确时间',seconds:true,value:'09:30:15'}),
 item('空值与限制','date-picker',{label:'预约日期',min:'2026-10-01',max:'2026-10-31',disabledDates:['2026-10-28'],help:'仅可选 10 月，28 日不可预约。'}),
 item('禁用','date-picker',{label:'已锁定日期',value:'2026-10-27',disabled:true}),
 item('只读','datetime-picker',{label:'创建时间',value:'2026-10-27 09:30',readonly:true}),
 item('错误提示','date-range',{label:'必填区间',state:'invalid'})
];
const forms=[
 item('文本与清空','input',{label:'课程名称',value:'人工智能基础',clearable:true}),
 item('组合输入','input-group',{label:'学校站点',value:'vocational',clearable:true}),
 item('密码显示与隐藏','password',{label:'临时访问密码',value:'demo-password',clearable:true}),
 item('多行与计数','textarea',{label:'课程简介',value:'围绕概念、数据与应用组织课程。',maxLength:120}),
 item('只读文本','input',{label:'课程编号',value:'C-2026-001',readonly:true}),
 item('错误文本','input',{label:'负责人邮箱',type:'email',value:'demo',state:'invalid',help:'请输入有效邮箱地址。'}),
 item('数字与单位','number',{label:'总学时',value:32,min:1,max:200,unit:'学时'}),
 item('单选下拉','select',{label:'所属学院',options:['信息工程学院','智能制造学院','数字艺术学院']}),
 item('多选标签与折叠','multiselect',{label:'关联专业',options:['软件技术','人工智能技术应用','数字媒体技术','工业机器人技术'],values:['软件技术','人工智能技术应用','数字媒体技术','工业机器人技术'],maxTagCount:2}),
 item('单选组','radio',{label:'课程性质',value:'required'}),
 item('按钮式单选','radio',{label:'授课方式',variant:'button',options:['线下','线上','混合'],value:'混合'}),
 item('全选与半选','checkbox',{label:'同步内容',options:['教案','课件','习题','案例'],values:['教案'],checkAll:true}),
 item('开关','switch',{label:'允许学生查看',value:true,checkedText:'已开放',uncheckedText:'未开放'}),
 item('自动补全','autocomplete',{label:'查找课程',options:['人工智能基础','人工智能技术应用','工业机器人技术','数字媒体设计']}),
 item('单值滑块','slider',{label:'掌握程度',value:60,unit:'%',marks:{0:'0%',50:'50%',100:'100%'}}),
 item('双值滑块','slider',{label:'成绩区间',range:true,value:[60,90],unit:'分'}),
 item('树节点勾选','tree',{label:'课程目录',searchable:true,checkable:true,checkedKeys:['concept']}),
 item('组织树多选','tree-select',{label:'关联专业',multiple:true}),
 item('院系专业级联','cascade',{}),
 item('学年学期','academic-term',{}),
 item('人员选择','person-picker',{label:'任课教师'}),
 item('文字分级评价','rate',{label:'课程满意度',value:4}),
 item('颜色选择','color-picker',{label:'日程标记颜色',value:'#155cc3'}),
 item('穿梭选择','transfer',{value:['b']},'勾选后点击添加或移回；左右分别支持搜索。'),
 item('拖放与文件校验','upload',{label:'教学资料',maxCount:3,maxSize:10485760},'上限 3 个、单个 10 MB；只选择本地文件，未上传。'),
 item('独立搜索','search',{label:'搜索资料',placeholder:'输入资源名称，回车搜索'})
];
const display=[
 item('状态与数量','badge',{count:120}),item('可移除标签','tag',{}),item('头像组','avatar',{items:[{name:'林老师'},{name:'周老师'},{name:'李老师'},{name:'张老师'},{name:'王老师'}],max:3}),
 item('描述列表','description',{bordered:true,items:[{label:'课程名称',value:'人工智能基础'},{label:'课程性质',value:'必修课'},{label:'总学时',value:32},{label:'负责人',value:null}]}),
 item('普通内容卡片','card',{title:'教学资料',description:'用于组织资料和相关说明。',meta:'最近更新于 2026-10-27'}),
 item('可操作卡片','card',{title:'人工智能基础',description:'查看课程详情',clickable:true}),
 item('数据列表','list',{actionLabel:'查看'}),item('卡片列表','list',{grid:true,actionLabel:'查看'}),
 item('指标与缺失值','stat',{}),item('条形图','chart',{type:'bar'}),item('折线图','chart',{type:'line',title:'本周资源使用量',data:[{label:'周一',value:12},{label:'周二',value:18},{label:'周三',value:15},{label:'周四',value:24},{label:'周五',value:20}]}),item('环形图','chart',{type:'donut'}),
 item('空数据图表','chart',{title:'暂无统计记录',data:[]}),item('时间线','timeline',{}),item('事件日历','calendar',{}),item('折叠面板','collapse',{})
];
const navigation=[
 item('面包屑','breadcrumb',{}),item('横向页签','tabs',{}),item('纵向页签','tabs',{direction:'vertical'}),item('分段选择','segmented',{items:[{value:'list',label:'列表视图',content:'当前使用列表布局。'},{value:'grid',label:'卡片视图',content:'当前使用卡片布局。'}]}),
 item('步骤导航','steps',{current:1,clickable:true}),item('纵向错误步骤','steps',{direction:'vertical',current:1,status:'error'}),item('锚点导航','anchor',{}),item('分页','pagination',{total:128,page:3,pageSize:10})
];
const feedback=[
 item('成功提示','alert',{title:'资料已保存',description:'可继续编辑或查看内容。',tone:'success',closable:true}),item('错误提示','alert',{title:'资料读取失败',description:'请检查文件格式后重试，已填写内容仍保留。',tone:'danger'}),
 item('线性进度','progress',{value:60}),item('环形进度','progress',{value:75,type:'circle'}),item('失败进度','progress',{value:42,status:'error'}),item('加载指示','loading',{}),
 item('动作菜单','menu',{}),item('选择浮层','popover',{title:'资料范围',content:'仅使用当前对象可见的课程资料。'}),item('悬停与焦点提示','tooltip',{content:'支持鼠标悬停及 Tab 键聚焦。'}),item('普通弹窗','dialog',{title:'核对课程信息',content:'确认当前课程对象后继续。',confirmLabel:'确认'}),item('侧边抽屉','drawer',{title:'课程详情',content:'课程名称：人工智能基础。总学时：32。'}),item('危险操作确认','confirm',{label:'删除资料',description:'确认删除当前示例资料？'}),item('无匹配状态','empty',{kind:'no-match'}),item('读取失败状态','empty',{kind:'failed'}),item('结果反馈','feedback-result',{kind:'success'})
];
const groups=[{id:'date',title:'日期与时间',description:'从单点、范围到年月周季，统一回显和选择方式。',items:temporal},{id:'form',title:'输入与选择',description:'补齐选择方式，并让基本控件能接入真实字段配置。',items:forms},{id:'display',title:'内容与数据',description:'数据、长文本与空值有明确表达，图形配套明细。',items:display},{id:'navigation',title:'导航与布局',description:'页签、步骤和局部导航可配置，禁用项不能被选中。',items:navigation},{id:'feedback',title:'反馈与浮层',description:'就地反馈、进度、结果和浮层各有明确用途。',items:feedback}];
const byKey={};groups.forEach(g=>g.items.forEach(x=>(byKey[x.key]??=[]).push(x)));byKey.date=temporal;
if(window.VocBusinessExamples)for(const batch of VocBusinessExamples.batches){const items=batch.keys.map(key=>{const example=VocBusinessExamples.selected(key);byKey[key]=VocBusinessExamples.cases(key).map(x=>item(x.title,key,x.props,VocBusinessExamples.guides[key]));return item(example.title,key,example.props,VocBusinessExamples.guides[key])});groups.push({id:batch.id,title:batch.name,description:'已填入虚构业务记录、角色与目录；直接操作查看回执，完整类型配置见组件详情。',items})}
window.VocVariants={groups,byKey,total:groups.reduce((n,g)=>n+g.items.length,0)};
})();
