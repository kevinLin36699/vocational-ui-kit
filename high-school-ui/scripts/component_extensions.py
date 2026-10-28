# -*- coding: utf-8 -*-
"""2.2 public contracts, used by build_current.py. No invented source evidence."""
TEMPORAL={
 'date-picker':('单日期选择','YYYY-MM-DD 或 null'), 'date-range':('日期范围选择','[YYYY-MM-DD,YYYY-MM-DD] 或 null'),
 'time-picker':('时间选择','HH:mm；seconds:true 时 HH:mm:ss'), 'time-range':('时间范围选择','[开始时间,结束时间] 或 null'),
 'datetime-picker':('日期时间选择','YYYY-MM-DD HH:mm 或 null'), 'datetime-range':('日期时间范围','[开始日期时间,结束日期时间] 或 null'),
 'year-picker':('年份选择','YYYY 或 null'), 'year-range':('年份范围','[YYYY,YYYY] 或 null'),
 'month-picker':('月份选择','YYYY-MM 或 null'), 'month-range':('月份范围','[YYYY-MM,YYYY-MM] 或 null'),
 'quarter-picker':('季度选择','YYYY-Q1 至 YYYY-Q4 或 null'), 'week-picker':('周选择','ISO 周年与周序号 YYYY-Www；周一至周日'),
 'multi-date':('多日期选择','去重、排序的 YYYY-MM-DD 数组')}
COMMON={'disabled':'禁用','readonly':'只读','state':'default/disabled/readonly/invalid'}
CONTRACTS={k:{'label':'字段标签','value':v,'name':'提交字段名','endName':'范围结束字段名','min':'同 value 格式的最小值','max':'同 value 格式的最大值','disabledDates':'禁选日期；周期与范围内含禁选日期则不可提交','disabledValues':'精确禁选值','seconds':'time/datetime 使用秒精度','step':'时间面板分钟步长，1–30；手动输入不被截断','presets':'可选{label,value}[]；日期范围默认近七天/本周/本月，选择后仍需确认','required':'必填视觉标记；业务提交校验由表单处理','help':'说明','maxTagCount':'multi-date 可见标签数，默认2；+N打开完整管理',**COMMON} for k,(n,v) in TEMPORAL.items()}
CONTRACTS.update({
 'input':{'label':'标签','value':'初始值，保留数字0','name':'字段名','type':'text/email/url/tel/search/number','prefix':'前缀文本','suffix':'后缀文本','clearable':'显示清空按钮','maxLength':'最大字符数','required':'原生必填','min':'number最小值','max':'number最大值','placeholder':'占位','help':'辅助或错误文案',**COMMON},
 'textarea':{'label':'标签','value':'初始值','name':'字段名','rows':'初始行数，至少2','maxLength':'字数上限和计数','placeholder':'占位','help':'说明',**COMMON},
 'checkbox':{'label':'组标签','options':'字符串或 {value,label,disabled?}[]','values':'初始值数组；[]表示全不选','name':'提交字段名','checkAll':'全选和半选联动；不改变禁用项','direction':'horizontal/vertical',**COMMON},
 'radio':{'label':'组标签','options':'字符串或 {value,label,disabled?}[]','value':'初始选中值','name':'提交字段名','variant':'default/button','direction':'horizontal/vertical',**COMMON},
 'switch':{'label':'可访问名称','value':'初始布尔值','name':'隐藏表单字段名','checkedText':'开启文案','uncheckedText':'关闭文案',**COMMON},
 'tag':{'items':'{id,label,tone?,closable?}[]','disabled':'禁用移除'},
 'badge':{'items':'{label,tone?}[]','count':'计数，含0','max':'超过显示max+，默认99'},
 'avatar':{'items':'{name,src?}[]；图片失败回退文字','size':'24/32/40/48/64','shape':'circle/square','max':'可见个数，默认4'},
 'description':{'items':'{label,value}[]，缺失显示—','columns':'1/2','bordered':'边框布局'},
 'breadcrumb':{'items':'{label,href?}[]，末项不可跳转','separator':'分隔字符'},
 'tabs':{'items':'{value,label,content?,disabled?}[]；content为文本','value':'初始页签ID','label':'页签组名称','direction':'horizontal/vertical','disabled':'禁用全部页签'},
 'steps':{'items':'{title,description?,disabled?}[]','current':'当前索引，从0开始','direction':'horizontal/vertical','status':'current/error','clickable':'允许点击；仅通知步骤ID，不代替业务校验','disabled':'禁用点击'},
 'progress':{'value':'0–100，超界裁剪','label':'进度名称','type':'line/circle','status':'normal/success/error/paused'},
 'timeline':{'items':'{title,description?,status?}[]'},
 'alert':{'title':'可选标题','description':'说明','tone':'info/success/warning/danger','closable':'可关闭'},
 'menu':{'label':'触发文案','items':'{id,label,disabled?,danger?}[]；只通知动作，不执行删除'},
 'popover':{'label':'触发文案','title':'标题','content':'纯文本内容'},
 'tooltip':{'label':'触发文案','content':'悬停和键盘提示文本'},
 'dialog':{'label':'入口文案','title':'标题','content':'纯文本内容','confirmLabel':'配置后显示确认按钮并通知动作','cancelLabel':'取消文案','size':'sm/md/lg','disabled':'禁用入口'},
 'slider':{'label':'标签','value':'数字或双值数组','range':'双值模式','min':'下限默认0','max':'上限默认100','step':'步长默认1','unit':'回显单位','marks':'等距刻度标签对象','name':'单值或下限字段名','endName':'上限字段名',**COMMON},
 'autocomplete':{'label':'标签','value':'初始文本','name':'字段名','options':'字符串或{value,label,disabled?}[]','placeholder':'占位','help':'说明',**COMMON},
 'transfer':{'items':'{value,label,disabled?}[]','value':'已选ID数组','titles':'左右标题数组；默认待选/已选',**COMMON},
 'upload':{'label':'标题','help':'说明','accept':'扩展名或MIME，逗号分隔','multiple':'默认true，false为单文件替换','maxCount':'默认5个','maxSize':'单文件字节上限，默认10MB',**COMMON},
 'list':{'items':'{id,title,description?,meta?}[]','grid':'网格模式','actionLabel':'可选逐项动作，发出voc:action'},
 'anchor':{'items':'{id,label,content?}[]；纯文本章节'},
 'loading':{'label':'加载说明'},
 'color-picker':{'label':'标签','value':'#RRGGBB','name':'字段名',**COMMON},
 'chart':{'type':'bar/line/donut','title':'标题','data':'{label,value}[]；非负数值；空数组为空态'}
})
CONTRACTS.update({'tree':{'nodes':'{id,label,disabled?,children?}[]','value':'选中节点ID','expandedKeys':'初始展开ID数组','checkedKeys':'初始勾选叶节点ID数组','checkable':'父子全选和半选','searchable':'筛选树节点',**COMMON},'search':{'label':'可访问名称','value':'初始关键词','name':'字段名','placeholder':'占位','help':'说明','disabled':'禁用'},'stat':{'items':'{label,value,suffix?,description?}[]；null显示—，保留0'},'card':{'title':'标题','description':'正文','meta':'辅助信息','clickable':'整卡可操作','disabled':'禁用'}})
CONTRACTS['password']=dict(CONTRACTS['input']);CONTRACTS['password'].pop('type')
CONTRACTS['input-group']=dict(CONTRACTS['input'])
CONTRACTS['segmented']=dict(CONTRACTS['tabs'])
CONTRACTS['drawer']=dict(CONTRACTS['dialog'])
NAMES={**{k:v[0] for k,v in TEMPORAL.items()},'password':'密码输入','input-group':'组合输入','slider':'滑动输入条','autocomplete':'自动补全','transfer':'穿梭选择','list':'数据列表','anchor':'锚点导航','loading':'加载指示','color-picker':'颜色选择'}
DESCRIPTIONS={
 'checkbox':'可配置选项与禁用项，全选、半选和已选计数联动。','radio':'可配置单选，横向、纵向与按钮变体，保留原生键盘操作。','input':'可配置文本输入，保留初始值，支持前后缀、清空与状态。',
 'textarea':'支持初始内容、只读、禁用和字数计数的多行输入。','chart':'条形、折线和环形图使用同一份配置数据，配套可访问表格明细。',
 'tabs':'可配置页签、禁用项和独立文本面板，横向/纵向排列与方向键切换。',
 'upload':'文件选择与拖放、格式/大小/数量校验及移除；仅本地选择，不声称已上传。',
 'transfer':'双栏搜索、待选/已选复核、显式移入移出及禁用项保护。',
 'autocomplete':'键入建议、中文输入法、键盘选择及自由输入；不触发真实检索。',
 'slider':'单值/双值滑块、步长、上下界与即时数值回显；支持键盘调整。',
 'steps':'可配置步骤、当前项、错误项和垂直方向；可选点击只通知步骤变更。',
 'progress':'直线和环形进度，成功、失败和暂停状态使用语义色。',
 'password':'可访问的密码显示/隐藏、清空和禁用状态，仅用于原型输入。',
 'input-group':'前缀、输入、清空与后缀共用一个外框，支持独立表单字段。',
 'list':'配置记录、空态、列表/卡片布局和逐项动作通知。',
 'anchor':'局部滚动内容与章节导航，点击定位且不改变组件库路由。',
 'loading':'带可访问说明的加载指示，尊重减少动效偏好。',
 'color-picker':'原生颜色面板、十六进制值回显与变更事件。'
}
def apply(catalog,contracts,version):
 existing={c['key'] for c in catalog}
 for key,name in NAMES.items():
  if key in existing:continue
  group='录入' if key in TEMPORAL or key in ['password','input-group','slider','autocomplete','transfer','color-picker'] else '导航布局' if key=='anchor' else '反馈浮层' if key=='loading' else '展示'
  catalog.append({'id':'voc-'+key,'key':key,'name':name,'category':group,'description':'','version':version,'rule':'FAMILY/2.2','evidence':[],'evidenceMatches':0,'evidenceType':'requested-extension','states':['default','selected','disabled','readonly','invalid'] if group=='录入' else ['default'],'implementation':'implemented','maturity':'本地HTML交互组件，未连接生产服务','api':{'render':f'VocUI.render("{key}", props)','mount':f'VocUI.mount(element, "{key}", props)','parameters':{}},'usage':{'recommended':'','avoid':'真实业务数据、权限与后端动作由页面接入。'},'sourcePattern':'requested-extension','extensions':['2.2组件家族补齐'],'alignment':{'reference':'现有蓝白令牌与本次完整性要求','kind':'requested-extension','standardVersion':version}})
 contracts.update(CONTRACTS)
 for c in catalog:
  k=c['key']
  if k not in CONTRACTS:continue
  c['api']['parameters']=CONTRACTS[k]
  c['implementationFiles']=['js/temporal.js' if k in TEMPORAL else 'js/extended-controls.js','css/extended-controls.css']
  if k in ['slider','color-picker','switch']:c['states']=['default','selected','disabled','readonly']
  if k in ['checkbox','radio']:c['states']=['default','selected','disabled','readonly']+(['partial'] if k=='checkbox' else [])
  if k in ['transfer','autocomplete']:c['states']=['default','selected','empty','no-match','disabled','readonly']
  if k in ['tabs','segmented']:c['states']=['default','selected','disabled','vertical']
  if k=='chart':c['states']=['bar','line','donut','empty']
  c['api']['events']=['voc:action'] if k in ['menu','dialog','drawer','list','card'] else ['voc:change'] if k in TEMPORAL or k in ['input','textarea','password','input-group','checkbox','radio','switch','tabs','segmented','steps','slider','transfer','upload','autocomplete','color-picker','tag','alert','tree'] else ['voc:submit'] if k=='search' else []
  c['api']['eventContract']='detail含component/action/value/name；日期时间等格式及空值见COMPLETENESS.md。'
  c['api']['parameterPolicy']='仅列实际支持参数，文本转义；无生产数据服务。'
  c['alignment']={'reference':'现有蓝白令牌与本次完整性要求','kind':'family-completion','standardVersion':version}
  c['description']=DESCRIPTIONS.get(k,('独立'+TEMPORAL[k][0]+'；手动输入与选择面板、清空、取消、限制和事件回传。' if k in TEMPORAL else c['name']+'支持数据配置、空值及实际交互。'))
  c['usage']['recommended']=c['description']
 from common_contracts import upgrade
 upgrade(catalog,contracts,version)
 from family_contracts import upgrade as upgrade_families
 upgrade_families(catalog,contracts,version)
 from education_contracts import upgrade as upgrade_education
 upgrade_education(catalog,contracts,version)
 from education_next_contracts import upgrade as upgrade_education_next
 upgrade_education_next(catalog,contracts,version)
 from education_platform_contracts import upgrade as upgrade_education_platform
 upgrade_education_platform(catalog,contracts,version)
 return catalog
