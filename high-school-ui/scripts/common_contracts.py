# -*- coding: utf-8 -*-
"""Supported 2.3 APIs; keep renderer contracts and documentation in sync."""
TABLE={
 'rows':'记录数组；稳定唯一rowKey；树形记录可含children',
 'columns':'{key,label,type?,width?,fixed?,sortable?,align?,hidden?,editable?,editor?,required?,min?,max?,options?,merge?,summary?}[]；多层表头用{label,children}，叶子key唯一',
 'rowKey':'记录主键，默认id；树中全部记录均须唯一','childrenKey':'默认children','title':'列表标题','description':'说明','filters':'{key,label,options}[]','filterValues':'初始筛选值对象','query':'初始查询词','sort':'{key,direction:1|-1} 或 null；点击为升序/降序/清除三态',
 'page':'初始页码，从1开始','pageSize':'每页数量，默认10','pageSizes':'可选数量数组','pagination':'false不分页；virtual自动不分页；树形默认不分页，显式true按根节点分页',
 'selectable':'false无选择；single单选；默认复选','selectedKeys':'初始已选ID数组','selectionScope':'page换页清空/across跨页保留','disabledRowKeys':'禁止选择的ID；行_selectionDisabled:true也禁止勾选',
 'editable':'本地增改删；自定义rows默认false','editMode':'dialog（默认）/cell；Enter或双击编辑，Esc取消','readonly':'只读；行_readonly:true禁止该行编辑/删除，包括批量删除',
 'tree':'树形表格；搜索保留祖先路径','expandedKeys':'初始展开节点ID','groupBy':'按字段分组，可折叠组','expandable':'{fields:[] }展开详情字段',
 'virtual':'固定行高窗口渲染，适合大集合','height':'虚拟或scrollY区域高度，默认360，最小160','rowHeight':'虚拟行高，默认44，最小36','scrollY':'在height高度内滚动；表头固定',
 'mergeCells':'{rowId,column,rowSpan?,colSpan?}[]；当前页内稳定ID起始的合并','summary':'true或合计文案；数字列默认sum，可在列设sum/avg/count/min/max',
 'columnReorder':'平铺表头允许拖动列；设置面板支持键盘/按钮换序','rowReorder':'未筛选/排序的本地平铺表支持拖动和Alt+上下键','resizable':'默认true；拖动或左右键调整列宽80–600px','fixedActions':'固定操作列','actions':'false隐藏行操作列','columnSettings':'false隐藏列设置入口','exportable':'false隐藏导出入口',
 'dataMode':'local（默认）/remote；remote的rows仅当前页','total':'remote总条数','size':'compact/default/comfortable','bordered':'边框型','striped':'斑马纹','searchPlaceholder':'占位文案','state':'default/loading/empty/no-match/failed/forbidden/readonly'
}
FORM={
 'fields':'任意字段配置数组；见TABLE_FORM.md字段矩阵；[]明确为空，不注入课程字段','values':'字段初始值对象；优先于兼容value参数','value':'兼容旧课程名称字符串或初始对象，推荐values','title':'可选标题','description':'说明',
 'layout':'vertical/horizontal/inline','columns':'1/2；窄容器单列','presentation':'standard/tabs/steps','sections':'{id,title,fields:字段name数组}[]；字段不可重复归属',
 'submitLabel':'提交文案','resetLabel':'重置文案','validateTrigger':'blur（默认）/input/submit；提交总是完整校验','includeHidden':'默认false，条件隐藏字段不提交','includeDisabled':'默认false，禁用字段不提交','disabled':'禁用全部','readonly':'只读展示，无提交入口','state':'default/disabled/readonly/loading/load-error/forbidden/failed','message':'状态说明'
}
def upgrade(catalog,contracts,version):
 contracts.update(table=TABLE,toolbar=TABLE,form=FORM)
 if not any(c['key']=='richtext' for c in catalog):
  catalog.append({'id':'voc-richtext','key':'richtext','name':'基础富文本编辑','category':'录入','version':version,'description':'基础文本格式、列表、链接、撤销与安全粘贴，支持作为表单字段。','rule':'FORM/2.3','evidence':[],'evidenceMatches':0,'evidenceType':'requested-extension','implementation':'implemented','maturity':'本地基础编辑器，不是Office或协同编辑引擎','api':{'render':'VocUI.render("richtext", props)','mount':'VocUI.mount(host,"richtext", props)','parameters':{},'events':['voc:change']},'usage':{'recommended':'用于普通业务说明、公告和教学文本。','avoid':'不冒充复杂文档、媒体或协同编辑器。'},'states':['default','focus','invalid','disabled','readonly'],'extensions':['2.3常用字段补齐'],'alignment':{'reference':'现有蓝白令牌与本轮通用表单要求','kind':'scenario-extension','standardVersion':version}})
 rich={'label':'可访问名称','value':'初始HTML；DOM白名单清理，不执行脚本/嵌入内容','placeholder':'占位文案','maxLength':'正文最大字数；提示与表单校验','minHeight':'初始编辑高度，至少100px','disabled':'禁用','readonly':'只读','state':'default/disabled/readonly'}
 contracts['richtext']=rich
 for c in catalog:
  if c['key']=='richtext':
   c['api']['parameters']=rich;c['api']['events']=['voc:change'];c['api']['eventContract']='{action:richtext-change,value:安全HTML,text:纯文本}';c['implementationFiles']=['js/common-extras.js','css/common-data.css']
  if c['key']=='chart':
   c['api']['parameters'].update(interactive='区间缩放、聚焦数值和children下钻',window='初始索引范围[start,end]',labels='多系列分类标签',series='{key,label,type:bar|line,axis:left|right,values:{label,value}[]}[]；双轴独立标度')
   c['implementationFiles']=['js/common-extras.js','js/extended-controls.js','css/common-data.css'];c['api']['events']=['voc:change'];c['api']['eventContract']='chart-window/chart-series/chart-drill，含window/path/series';c['description']='可配置条形、折线、环形与双轴组合图；区间缩放、系列显隐、数值提示、children下钻和表格明细。'
  if c['key']=='tree':
   c['api']['parameters'].update(checkStrategy='linked级联叶节点/strict父子独立',inheritDisabled='默认true，禁用祖先锁定后代；不是后端授权')

 for c in catalog:
  k=c['key']
  if k not in ('form','table','toolbar'):continue
  c['api']['parameters']=FORM if k=='form' else TABLE
  c['api']['events']=['voc:change','voc:submit','voc:action'] if k=='form' else ['voc:change']
  c['api']['eventContract']='完整事件、实例方法、异步回执与组合限制见design/TABLE_FORM.md；JSON参数不接受函数，回调在挂载后绑定。'
  c['api']['parameterPolicy']='以上参数由实际公共实现支持；本地状态和模拟提交不等同真实业务写入。'
  c['implementationFiles']=['js/schema-form.js' if k=='form' else 'js/advanced-table.js','css/common-data.css']
  c['description']='按fields/values配置字段、分区与分步，条件联动、重复项、同步/异步校验、错误定位、提交防重与失败恢复。' if k=='form' else '可配置平铺/树形/分组/虚拟表格、多层与合并表头单元格、固定列、编辑校验、行列排序、跨页选择和远程请求。'
  c['usage']['recommended']=c['description'];c['states']=['default','loading','empty','no-match','failed','forbidden','readonly','selected','editing'] if k!='form' else ['default','dirty','invalid','validating','submitting','success','failed','loading','load-error','readonly','disabled','forbidden']
  c['alignment']={'reference':'既有蓝白公共规范；用户要求补齐通用表格与表单','kind':'scenario-extension','standardVersion':version}
