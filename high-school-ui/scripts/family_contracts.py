"""Actual supported families; kept separate from historical source scan."""
PARAMS={
'pagination':{'total':'总条数，0时边界禁用','page':'当前页1起','pageSize':'每页条数','pageSizes':'允许容量数组','simple':'简洁模式','showSize':'默认true','showJump':'默认true'},
 'tooltip':{'label':'入口','content':'纯文本提示','placement':'top/right/bottom/left；空间不足自动翻转'},
'button':{'label':'文本','variant':'primary/soft/outline/ghost/destructive','size':'sm/default/lg','icon':'现有图标名','loading':'锁定并显示等待','confirm':'执行前确认','value':'动作载荷'},
'link':{'label':'文本','href':'http(s)/hash/站内路径；危险地址不生成链接','external':'新窗口并说明去向'},
'separator':{'direction':'horizontal/vertical','label':'水平分隔文本','align':'left/center/right'},
'badge':{'items':'{label,tone}[]','count':'计数，保留0','max':'封顶99+','dot':'小圆点','showZero':'默认显示0','label':'语义说明'},
'avatar':{'items':'{name,src?}[]，失败回退文字','size':'24/32/40/48/64','max':'可见成员数，溢出可展开全部成员','shape':'circle/square'},
'description':{'items':'{label,value,copyable?,span?}[]','columns':'1/2/3','bordered':'边框布局'},
'card':{'title':'标题','description':'文本正文','meta':'辅助信息','collapsible':'内容收放','clickable':'主动作','actions':'{id,label,disabled?}[]'},
'stat':{'items':'{label,value,prefix?,suffix?,precision?,change?,changeUnit?,description?}[]，null显示—'},
'progress':{'value':'0–100','type':'line/circle/dashboard','status':'normal/success/error/paused','steps':'分段数1–40','indeterminate':'不确定进度，不伪造百分比','label':'名称'},
'skeleton':{'rows':'1–12行','avatar':'头像骨架','active':'是否动画','label':'等待说明'},
'loading':{'label':'等待说明','overlay':'遮罩模式，内容inert','content':'遮罩下文本'},
'list':{'items':'{id,title,description?,meta?,disabled?}[]，ID唯一','grid':'卡片布局','actionLabel':'逐项动作','searchable':'本地搜索','sortable':'名称排序','pageSize':'逐批显示条数','remote':'启用loader追加读取','hasMore':'是否还有后续页'},
'calendar':{'value':'YYYY-MM-DD','month':'未提供value时使用YYYY-MM','view':'month/week/day/agenda','events':'{id,date,title,time?,type?,disabled?}[]','min':'最早可选日','max':'最晚可选日','disabledDates':'禁选日期数组'},
'notification':{'items':'{id,title,description?,time?,read?,disabled?}[]','dismissible':'可移除当前内存通知','title':'标题'},
'image-preview':{'items':'{id,src,alt?}[]图片组；仅src时单图','src':'单图地址','alt':'单图说明','title':'预览标题'},
'collapse':{'items':'{id,title,content,disabled?}[]','openKeys':'展开ID数组','accordion':'最多展开一项'},
'breadcrumb':{'items':'{id,label,href?,disabled?,children?}[]','separator':'分隔符，children提供同层切换菜单'},
'navigation-menu':{'items':'{id,label,icon?,disabled?,children?}[]','value':'选中叶子ID','openKeys':'初始展开ID','direction':'horizontal/vertical','collapsed':'侧栏收起','accordion':'展开父项时收起其他项'},
'carousel':{'items':'{id,title,description?,src?,alt?}[]','current':'当前索引','loop':'是否循环','autoplay':'自动播放，默认关闭','interval':'默认4000ms；至少1200ms','label':'可访问名称'},
'splitter':{'first':'第一面板文本','second':'第二面板文本','value':'第一面板百分比','min':'默认15','max':'默认85','direction':'horizontal/vertical'},
'backtop':{'items':'段落文本数组','threshold':'出现按钮滚动距离，默认80','buttonLabel':'按钮文本'},
'menu':{'items':'{id,label,type?,checked?,group?,danger?,disabled?,children?}[]；type=checkbox/radio/separator','label':'入口文本'},
'popover':{'label':'入口','title':'标题','content':'纯文本内容'},
'dialog':{'label':'入口','title':'标题','content':'纯文本内容','confirmLabel':'确认按钮，绑定handler后等待真实回执','cancelLabel':'取消文案','size':'sm/md/lg','maskClosable':'默认true','keyboard':'默认true'},
'drawer':{'placement':'left/right/top/bottom'},
'confirm':{'label':'入口','title':'标题','description':'后果说明','confirmLabel':'确认文案'},
'alert':{'title':'标题','description':'说明','tone':'info/success/warning/danger','closable':'可关闭','actions':'{id,label,disabled?}[]'},
'toast':{'label':'入口','content':'消息','tone':'info/success/warning/danger','duration':'默认3500ms；0持续显示直到关闭；悬停/焦点暂停'},
'empty':{'kind':'empty/no-match/failed/forbidden','title':'标题','description':'说明','actions':'{id,label,disabled?}[]','actionLabel':'默认动作文案；false隐藏'},
'feedback-result':{'kind':'success/error/forbidden/notfound/warning/info','title':'标题','description':'说明','actions':'{id,label,disabled?}[]'},
 'tabs':{'items':'{value,label,content?,disabled?,closable?,dirty?}[]，value唯一','value':'当前ID','direction':'horizontal/vertical','variant':'line/card','addable':'只通知新增请求，由业务调用setItems'},
 'timeline':{'items':'{id,title,description?,time?,status?,pending?,actionLabel?,disabled?}[]','direction':'horizontal/vertical','alternate':'交错层级显示'}
}
PARAMS.update({
 'icon':{'name':'现有图标名','size':'12–64','label':'语义名称','clickable':'可点击图标入口'},
 'course-card':{'id':'课程ID','title':'课程名','description':'课程说明','type':'必修/选修等标签','hours':'学时','teachers':'教师名称数组','cover':'封面图片','favorite':'配置后显示本地收藏开关'},
 'agent':{'items':'{id,name,description?,available?,reason?}[]；只准备，不自动发送'},
 'task-guide':{'title':'标题','description':'说明','context':'{label,value}[]','prompt':'可编辑预填文本','actionLabel':'准备需求按钮'},
 'message':{'id':'消息ID','role':'user/assistant','text':'正文；助手使用安全Markdown子集','author':'名称','createdAt':'时间文本','messageState':'completed/streaming/failed/stopped','attachments':'{name}[]'},
 'prose':{'content':'安全Markdown子集，支持标题/代码/列表/表格，不执行HTML'},
 'citation':{'items':'{id,title,description?,href?,verified?}[]；核验状态由业务提供'},
 'result':{'id':'成果ID','title':'标题','description':'摘要','statusText':'业务状态','actionLabel':'查看按钮，仅通知result-open'},
 'approval':{'value':'draft/review/approved/rejected/distributed','title':'标题','description':'业务说明；handler确认后才更新状态'},
 'shell':{'title':'平台名称','items':'{id,label,content?,disabled?}[]','value':'选中ID','collapsed':'初始收起侧栏'},
})

PARAMS['drawer']={**PARAMS['dialog'],**PARAMS['drawer']};PARAMS['segmented']=dict(PARAMS['tabs']);PARAMS['tag']={'items':'{id,label,tone?,closable?,disabled?}[]','checkable':'可选择标签','value':'已选ID数组'}
NEW={'navigation-menu':('业务导航菜单','导航布局'),'carousel':('图文轮播','展示'),'splitter':('可调整分栏','导航布局'),'backtop':('局部返回顶部','导航布局')}
DESCRIPTIONS={
'calendar':'月/周/日/日程视图、今天定位、键盘选日、边界和禁选日、事件详情动作。',
'notification':'全部/未读/已读筛选、逐项切换、批量已读、详情和本地移除，保护禁用项。',
'image-preview':'单图/图片组、切图、缩放、旋转、重置、失败重试和键盘控制。',
'menu':'普通/复选/单选菜单、分隔项、子菜单、禁用项与键盘退出；业务动作只通知。',
'list':'可配置列表/网格、本地搜索排序、批次展示与异步追加读取，失败保留原列表。',
'navigation-menu':'可配置多层导航、横纵方向、收放、禁用继承、键盘移动和选中事件。',
'carousel':'图文轮播、边界/循环、指示器与键盘切换；自动播放可暂停且尊重减少动画。',
'splitter':'双面板拖动和键盘调节、上下限、横纵布局，值以比例回传。',
'backtop':'局部滚动容器的阈值显隐与返回顶部；减少动画时即时定位。',
'dialog':'可配置弹窗、取消与焦点恢复、可控关闭、异步确认防重复和失败保留。',
'drawer':'左/右/上/下抽屉，继承弹窗取消、焦点与异步回执约定。',
'confirm':'明确对象后果的确认，取消不执行；绑定异步处理器后等待业务回执。',
'button':'单实例按钮，样式/尺寸/图标/禁用/等待与异步回执，不写死示例动作。',
 'tabs':'页签/卡片/纵向页签，禁用项跳过、独立面板、可关闭与未保存保护、动态配置。'
}
def upgrade(catalog,contracts,version):
 import copy
 known={c['key']:c for c in catalog}
 for k,(name,category) in NEW.items():
  if k not in known:
   c=copy.deepcopy(known['list']);c.update(id='voc-'+k,key=k,name=name,category=category,evidence=[],evidenceMatches=0,evidenceType='family-extension',sourcePattern='family-extension');catalog.append(c);known[k]=c
 for k,params in PARAMS.items():
  c=known[k];contracts[k]={**params,'state':'default/loading/empty/failed/forbidden/disabled/readonly；仅适用的交互受禁用/只读影响','disabled':'禁止当前组件动作','readonly':'保留展示，适用的数据编辑锁定'}
  c['api']['parameters']=contracts[k];c['api']['events']=['voc:action','voc:change'];c['api']['eventContract']='detail含component/action/value；请求生命周期和逐项事件见FAMILIES.md'
  c['implementationFiles']=['js/family-controls.js','css/family-controls.css'];c['states']=['default','disabled']
  if k not in ['separator','link','loading','skeleton']:c['states']+=['loading','empty','failed','forbidden']
  if k in ['list','calendar','notification']:c['states']+=['readonly']
  if k in ['separator','description','stat','timeline','progress','skeleton','loading','badge','avatar']:c['states']=[x for x in c['states'] if x!='disabled']
  if k in ['skeleton','loading']:c['states']=['default']
  if k=='empty':c['states']=['empty','no-match','failed','forbidden']
  if k=='feedback-result':c['states']=['success','error','forbidden','notfound','warning','info']
  if k in ['select','multiselect','cascade','academic-term','tree-select','person-picker','upload','number']:c['states']=list(dict.fromkeys(c['states']+['disabled','readonly']))
  c['description']=DESCRIPTIONS.get(k,c['name']+'支持参数化类型与适用状态，交互见FAMILIES.md。');c['usage']['recommended']=c['description'];c['extensions']=list(dict.fromkeys(c.get('extensions',[])+['2.4全家族复查']))
 for c in catalog:
  if c['key']=='process':
   c['api']['parameters'].update(stages='自定义公开阶段{title,description?,detail?}[]',current='当前阶段索引',state='waiting/running/completed/failed/stopped')
  if c['key'] in ['select','multiselect','cascade','academic-term','tree-select','person-picker','upload','number','tree','steps']:
   c['states']=list(dict.fromkeys(c['states']+['disabled','readonly']))
   c['api']['parameters']['readonly']='只读；保留当前值并锁定选择与移除'
  c['version']=version;c['alignment']['standardVersion']=version
