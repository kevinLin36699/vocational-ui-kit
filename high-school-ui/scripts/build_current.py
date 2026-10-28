#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Maintain current 2.1 metadata without rescanning or replacing historical source evidence."""
from pathlib import Path
import json
import re

R=Path(__file__).resolve().parents[1]
VERSION='2.7.1'
def write(path,value): (R/path).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
catalog=json.loads((R/'data/components.json').read_text())
contracts={
 'pagination':{'total':'总条数','page':'当前页，从1开始','pageSize':'每页数量','pageSizes':'每页条数选项'},
 'date':{'mode':'range（默认）/single','label':'标签','value':'YYYY-MM-DD 或双日期数组或 null','name':'开始或单日期字段名','endName':'结束字段名','min':'最早日期','max':'最晚日期','disabledDates':'禁选日期数组','disabled':'禁用','readonly':'只读','required':'字段标记','help':'说明','state':'default/disabled/readonly/invalid'},
 'select':{'label':'标签','options':'字符串或 {value,label,disabled?,reason?} 数组','value':'初始字符串值','name':'字段名','placeholder':'占位','disabled':'禁用','state':'default/disabled'},
 'multiselect':{'maxTagCount':'框内最多可见标签，默认2；还按可用宽度收纳','label':'标签','options':'候选数组','values':'初始字符串 ID 数组','name':'字段名','disabled':'禁用'},
 'number':{'label':'标签','value':'数值','name':'字段名','unit':'单位','min':'下限','max':'上限','step':'步长','disabled':'禁用'},
 'table':{'rows':'具有稳定 ID 的记录数组；未传为课程示例','columns':'{key,label,type?,sortable?,align?,hidden?,required?,min?,max?,options?,editable?}[]','filters':'{key,label,options}[]','rowKey':'唯一标识字段，默认 id','pageSize':'每页数量，默认10','title':'列表名称','searchPlaceholder':'搜索占位','selectable':'false 关闭行选择','editable':'是否提供本地增改删；自定义 rows 默认 false','state':'default/empty/no-match/loading/failed'},
 'time-picker':{'label':'标签','value':'HH:mm','name':'字段名','step':'分钟列表步长，默认15','min':'最早时间','max':'最晚时间','disabled':'禁用','readonly':'只读'},
 'tree-select':{'maxTagCount':'多选时框内最多可见标签，默认2','label':'标签','nodes':'{id,label,children?,disabled?}[]','value':'单个 ID 或多选 ID 数组','multiple':'是否多选','leafOnly':'仅叶节点可选','placeholder':'占位','disabled':'禁用'},
 'academic-term':{'label':'标签','terms':'{id,year,label}[]；真实目录由业务提供','value':'学期 ID','name':'字段名','disabled':'禁用'},
 'collapse':{'items':'{id,title,content,disabled?}[]；content 为文本','openKeys':'初始展开 ID 数组','accordion':'是否只展开一项'},
 'rate':{'label':'评价问题','labels':'五级评价文字，也可提供其他级数','value':'从1开始的选项序号','disabled':'禁用','readonly':'只读'},
 'calendar':{'month':'YYYY-MM 初始月份','value':'初始选中日期','events':'{id,date,title,type?}[]；type为徽标语义色'},
 'notification':{'items':'{id,title,description?,read?}[]'},
 'image-preview':{'src':'本地、http(s)、blob 或 image data 地址','alt':'图片说明'},
 'feedback-result':{'kind':'success/error/forbidden/notfound','title':'自定义标题','description':'说明','actionLabel':'动作文案，触发事件后由页面处理'},
 'empty':{'kind':'empty/no-match/failed','title':'标题','description':'说明','actionLabel':'文案或 false 隐藏按钮'},
 'person-picker':{'items':'{id,name,department?,disabled?}[]','value':'初始 ID 数组','label':'标签','disabled':'禁用'},
 'resource':{'items':'{id,name,type?,size?,version?,description?}[]','view':'list/grid 初始布局'},
 'cascade':{'label':'标签','nodes':'院系和专业的树结构','value':'专业 ID','disabled':'禁用'},
 'confirm':{'label':'触发文案','description':'确认说明'},
 'batch-import':{}
}
contracts['toolbar']=contracts['table']
new=[
 ('time-picker','时间选择','录入','排课时间单框与小时/分钟面板，支持手动输入和范围校验。',['default','focus','disabled','readonly','invalid'],'js/teacher-training-arrangement.js','排课'),
 ('tree-select','树选择','录入','院系、专业、班级分层搜索选择，支持多选和已选项移除。',['default','selected','disabled','empty','no-match'],'js/centers/administration/views/teaching.js','学期'),
 ('academic-term','学年学期选择','高职教业务','用稳定学期ID选择学年学期，目录由当前业务提供。',['default','selected','disabled','empty'],'js/centers/administration/views/teaching.js','学期'),
 ('collapse','折叠面板','展示','按章节组织教学说明，独立展开或手风琴模式；内容只作文本处理。',['open','closed','disabled'],'js/teacher-training-materials.js','资料'),
 ('rate','五级评价','录入','有明确文字含义的分级评价，支持键盘选择和只读展示。',['default','selected','disabled','readonly'],'js/centers/administration/views/course-evaluation.js','五级'),
 ('calendar','事件日历','展示','按月查看教学日程与截止提醒，选择日期查看事件，不执行排课。',['default','selected','empty'],'js/student-training-dashboard.js','今日'),
 ('notification','通知提醒','反馈浮层','通知摘要、未读状态、全部已读及详情；仅更新本地示例。',['unread','read','empty'],'js/student-training-dashboard.js','提醒'),
 ('image-preview','图片预览','展示','缩略图、大图缩放与旋转，支持失败提示和模态键盘关闭。',['default','open','failed'],'js/teacher-training-materials.js','预览'),
 ('feedback-result','操作结果反馈','反馈浮层','区分成功、失败、无权限和未找到；后续业务动作通过事件处理。',['success','error','forbidden','notfound'],'js/course-hub.js','error'),
 ('batch-import','名单导入校验','高职教业务','CSV/TSV或粘贴名单，预览校验、错误定位、错误导出和显式确认。',['draft','invalid','valid','confirmed','failed'],'js/course-hub.js','导入学生')
]
existing={c['key'] for c in catalog}
for key,name,category,description,states,source,term in new:
 if key in existing: continue
 origin=R.parents[1]/'3-原型设计/high-school-new'/source
 evidence=[]
 if origin.exists():
  for line,text in enumerate(origin.read_text().splitlines(),1):
   if term in text:evidence=[{'file':source,'line':line,'excerpt':text.strip()[:180]}];break
 catalog.append({'id':'voc-'+key,'key':key,'name':name,'category':category,'description':description,'version':VERSION,'rule':'EDU/QUALITY-2.1','evidence':evidence,'evidenceMatches':len(evidence),'evidenceType':'scenario-extension','states':states,'statePolicy':'仅列实际适用状态；以真实交互和已记录测试为准。','implementation':'implemented','maturity':'可配置HTML交互组件，未连接生产服务','api':{'render':f'VocUI.render("{key}", props)','mount':f'VocUI.mount(element, "{key}", props)','parameters':contracts[key],'events':['voc:change'] if key!='batch-import' else ['voc:submit'],'eventContract':'实际事件及字段见 design/CONTROLS.md'},'usage':{'recommended':description,'avoid':'不把示例业务数据或本地状态当作真实服务。'},'sourcePattern':'scenario-extension','extensions':['2.1.1场景补齐'],'alignment':{'reference':'2.1高职教场景；Ant Design分类和通用控件交互参考','kind':'scenario-extension','implementation':'本地HTML/CSS/JS；未移植第三方付费模板源码','standardVersion':VERSION}})
descriptions={
 'pagination':'总数在左，每页条数与数字分页在右聚合；支持直接选页、跨页及边界禁用。',
 'multiselect':'框内标签回显、按宽度省略、+N管理已选；保留搜索、键盘和移除。',
 'tree':'带层级引导、整行悬停和明确选中状态的课程目录；展开与选择分别操作。',
 'chart':'带刻度的课程数量图表，筛选与表格明细共享数据，支持明细收放。',
 'date':'统一外框的单日期/日期范围，日历面板、快捷范围、输入校验与键盘操作；日期值不作时区转换。',
 'table':'可配置数据与列、筛选排序、列显隐、本页选择、分页、CSV及可选本地增改删。',
 'toolbar':'组合搜索、业务筛选、列显隐和列表操作；按可用宽度换行。',
 'cascade':'单框树层级选择院系与专业，父级仅组织目录，专业ID作为选择值。',
 'person-picker':'搜索、多选、已选结果复核与取消保护；确认后才应用至草稿。',
 'resource':'可配置资源目录，列表/卡片切换、关键词搜索、详情与本地文本下载。',
 'number':'数字与单位置于同一外框，范围校验后发出变更事件。',
 'empty':'区分首次空白、无匹配与读取失败，提供适用引导和恢复动作。',
 'confirm':'删除使用危险色，模态与轻量气泡确认均先说明对象和后果。'
}
for c in catalog:
 c['version']=VERSION;c.setdefault('alignment',{})['standardVersion']=VERSION
 if c['key'] in contracts:
  c['api']['parameters']=contracts[c['key']];c['api']['parameterPolicy']='仅以上实际支持参数可用；复杂行为通过文档定义的事件处理。'
 if c['key'] in descriptions:c['description']=descriptions[c['key']];c['usage']['recommended']=c['description']
 if c['key']=='date':c['states']=['default','focus','selected','partial','invalid','disabled','readonly']
 if c['key'] in ['table','toolbar']:c['states']=['default','loading','empty','no-match','failed','selected']
 if c['key']=='empty':c['states']=['empty','no-match','failed']
from component_extensions import apply
apply(catalog,contracts,VERSION)
for c in catalog:c['version']=VERSION
write('data/components.json',catalog)
text=(R/'js/catalog.js').read_text();text=re.sub(r'window\.VocCatalog=.*?;\nwindow\.VocAudit=',lambda _: 'window.VocCatalog='+json.dumps(catalog,ensure_ascii=False)+';\nwindow.VocAudit=',text,flags=re.S);(R/'js/catalog.js').write_text(text)
meta=json.loads((R/'data/library.json').read_text());meta.update(version=VERSION,components=len(catalog),styles=['css/tokens.css','css/components.css','css/refinements.css','css/extended-controls.css','css/common-data.css','css/family-controls.css','css/education-controls.css','css/education-next.css','css/education-platform.css'],runtime=['js/icons.js','js/resource-composer.js','js/skill-picker.js','js/content-workspace.js','js/voc-ui.js','js/controls.js','js/data-table.js','js/batch-import.js','js/temporal.js','js/extended-controls.js','js/schema-form.js','js/advanced-table.js','js/common-extras.js','js/family-controls.js','js/education-controls.js','js/education-next.js','js/education-platform.js','js/education-bridge.js'],pagePatterns=len(json.loads((R/'data/page-patterns.json').read_text())),controlStandard='design/CONTROLS.md',controlContract='data/control-contracts.json',qualityReview='data/ui-review.json',completenessReview='data/component-completeness.json',variantsExample='examples/completeness.html',educationPlatformStandard='design/EDUCATION_PLATFORM.md',educationPlatformReview='data/education-platform-components.json',educationIntegrationExample='examples/education-integration.html',showcaseRuntime=['js/education-scenarios.js','js/education-next-scenarios.js','js/education-platform-scenarios.js','js/business-examples.js','js/component-variants.js'],businessExamplesStandard='design/BUSINESS_EXAMPLES.md',businessExamplesReview='data/business-examples.json',showcaseStyles=['css/business-examples.css']);write('data/library.json',meta)
write('data/control-contracts.json',{'version':VERSION,'parameters':contracts,'events':{'date-change':'{action,value:string|[start,end]|null,name}','time-change':'{action,value:HH:mm|null}','tree-select':'{action,value:id|id[]}','people-select':'{action,value:id[]}','calendar-select':'{action,value:date,events:[]}','rate':'{action,value:number}','roster-import':'voc:submit {action,rows:[{id,name,className}],simulated:true}','table-save':'voc:change {action,row,simulated:true}'}})
specific={'pagination':'总数、每页条数、页数拆散，缺少直达页码与清晰分组','tree':'缺少整行悬停反馈与稳定的选中层级','chart':'图形缺少清晰刻度，原生明细未排版且有重复展开指示','button':'无空格超长文案撑宽，缺少可收缩文本容器','shell':'320px局部容器仍保留完整侧栏，挤压主体','date':'2.0为双原生日期框；2.1单框后仍存在日期值留白过大、图标层次欠清晰','number':'单位游离在输入框外，缺少统一范围反馈','table':'固定示例数据；窄容器筛选栏溢出，缺少列配置','toolbar':'窄容器字段最小宽度导致筛选栏溢出','chat':'窄容器会话栏未收起，挤压标题和输入工具栏','conversation':'与AI组合共用窄容器挤压问题','select':'固定候选与选中长文本处理不足','multiselect':'框内只回显已选N项，标签脱离控件；溢出与已选管理欠缺','cascade':'两个分离下拉，层级关系与搜索体验不足','person-picker':'缺少完整搜索多选及已选结果复核','empty':'单一空状态不能区分首次引导与恢复','resource':'单个固定资源，未覆盖目录视图和长文件名','confirm':'仅模态示例，缺少轻量就地确认'}
review=[]
for c in catalog:
 k=c['key'];review.append({'id':c['id'],'name':c['name'],'baseline':'2.0.0' if k not in {x[0] for x in new} else None,'issue':specific.get(k,'未发现独立结构缺陷；纳入统一视觉、长文本和容器回归' if k not in {x[0] for x in new} else '场景缺口，依据原平台业务补齐'),'treatment':'rebuild' if k in specific else 'add' if k in {x[0] for x in new} else 'refine-and-verify','implementation':'implemented','validation':'pending','evidence':[]})
old=R/'data/ui-review.json'
if old.exists():
 previous_report=json.loads(old.read_text());previous={x['id']:x for x in previous_report['components']}
 for x in review:
  if x['id'] in previous:x.update({k:previous[x['id']][k] for k in ['validation','evidence','coverage','scenario','resolution','implementationFiles','remaining'] if k in previous[x['id']]})
write('data/ui-review.json',{'version':VERSION,'baselineComponents':60,'baselinePatterns':14,'components':review,'patternValidation':previous_report.get('patternValidation','pending') if old.exists() else 'pending','patterns':previous_report.get('patterns',[]) if old.exists() else [],'notInScope':['原业务工程改造','生产接口','GitHub推送','发布Skill覆盖']})
print('Current metadata:',len(catalog),'components; historical scan evidence retained.')
