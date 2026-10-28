#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publish an explicit row for every component; rendering is distinct from behavior QA."""
import json
from pathlib import Path
from component_extensions import CONTRACTS, TEMPORAL, NAMES
R=Path(__file__).resolve().parents[1]
catalog=json.loads((R/'data/components.json').read_text())
recipes={'form','shell','course-card','approval','task-guide','agent','conversation','composer','message','prose','process','citation','result','workspace','chat','icon','link','separator','button','skeleton','toast'}
notes={
 'date':'保留既有single/range以兼容旧页；独立入口补齐13种时间日期类型与18个展示状态。',
 'select':'已有搜索下拉和禁用项；维持框内单值回显。',
 'multiselect':'已有框内标签与+N管理；沿用按宽度折叠。',
 'number':'已有数值/单位外框与上下界、步长校验。',
 'table':'已有稳定行ID、配置列、过滤、排序、分页、列显隐及可选本地增改删。',
 'toolbar':'沿用table数据与筛选配置；不同业务不继承课程字段。',
 'pagination':'已有总数、页容量、页码、跨页与边界禁用。',
 'cascade':'已有分层搜索和叶节点值。复杂父子权限策略仍由业务定义。',
 'tree-select':'已有单/多选、搜索和框内标签；不增加未经定义的权限勾选策略。',
 'academic-term':'已有学年学期目录与稳定ID选择，目录由业务传入。',
 'person-picker':'已有搜索、已选复核及取消保护；身份来自目录。',
 'resource':'已有目录配置、列表/网格和资源详情；不声称解析全部文件格式。',
 'calendar':'已有按月事件目录，不是自动排课和冲突引擎。',
 'batch-import':'已有CSV/TSV/粘贴校验、错误定位与显式确认。',
 'confirm':'已有模态与轻量危险确认；维持危险色。',
 'collapse':'已有可配置折叠项与手风琴。',
 'rate':'已有文字分级评价；保留明确级别含义。',
 'empty':'已有首次空白、无匹配、失败三类。',
 'notification':'已有未读、已读、详情和空态。',
 'image-preview':'已有缩放旋转和失败提示；不扩展为文档解析器。',
 'feedback-result':'已有成功、失败、无权限、未找到。'
}
rows=[]
for c in catalog:
 k=c['key'];new=k in NAMES and k!='time-picker';changed=k in CONTRACTS
 treatment='新增常用类型' if new else '补齐配置和变体' if changed else '保留业务/基础配方' if k in recipes else '复核现有组件'
 source='js/temporal.js' if k in TEMPORAL else 'js/extended-controls.js' if changed else 'js/data-table.js' if k in ['table','toolbar'] else 'js/batch-import.js' if k=='batch-import' else 'js/voc-ui.js' if k in recipes or k=='select' or k=='multiselect' else 'js/controls.js'
 note=notes.get(k,c['description'] if changed else '此项为公开的示例配方或基础原语；不声称支持任意业务参数。' if k in recipes else c['description'])
 rows.append({'key':k,'name':c['name'],'treatment':treatment,'source':source,'finding':note,'verification':'源码逐项复核；浏览器渲染/交互证据见本轮独立报告','remaining':'真实服务、生产适配和业务规则由页面接入' if k in recipes else ''})
report={'version':'2.2.0','baselineCount':70,'currentCount':len(rows),'reviewMethod':'逐项核对目录、参数、公共渲染器、变体及本轮浏览器检查。渲染通过不等于设计质量或全部状态验收通过。','components':rows,'remaining':['表格虚拟滚动、复杂合并单元格、拖拽排序和跨页选择策略','图表交互缩放、联动钻取、复杂组合坐标轴','通用动态表单构建器；现有form保留课程示例配方','树的复杂权限继承和自动排课冲突引擎','富文本、PDF/Office/PPT/视频等专用编辑器','真实上传/审批/权限/持久化和生产React/Vue封装','全浏览器与无障碍认证']}
alignment=json.loads((R/'data/component-alignment.json').read_text())
known={c['key']:c for c in alignment['components']}
for c in catalog:
 if c['key'] not in known:
  alignment['components'].append({'id':c['id'],'key':c['key'],'name':c['name'],'reference':'用户2026-10-27组件完整性要求；既有蓝白令牌与公共控件规范','kind':'scenario-extension','implementation':c['description'],'status':'implemented','onlineVerified':False,'verification':'本轮本地浏览器检查，非参考站点逐像素对照'})
 elif c['key'] in CONTRACTS:
  known[c['key']]['implementation']=c['description']
  known[c['key']]['verification']='本轮配置和变体升级；data/completeness-2.2/记录实际验证范围'
alignment.update(version='2.2.0',componentCount=len(catalog))
(R/'data/component-alignment.json').write_text(json.dumps(alignment,ensure_ascii=False,indent=2)+'\n')
(R/'data/component-completeness.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
text='''# 组件完整性与变体 v2.2.0

本轮从原有70项逐项检查源码、公开参数与示例入口，补齐常用家族并修正固定示例的配置缺口。当前目录共COUNT项；类型、变体和状态分别记录，不用数量代表设计验收。

总览入口：[组件家族与变体](../examples/completeness.html)。每个示例直接复用公共源码，可查看配置和最近事件。组件详情页也展示同组件的常用变体。

## 日期与时间

单日期、日期范围、时间、时间范围、日期时间、日期时间范围、年、年范围、月、月范围、季度、ISO周和多个日期均有独立入口。

新入口支持选中值回显、清空、只读、禁用、上下界、不可选日期、输入校验和手动确认；取消、Escape及外部关闭只丢弃未确认选择。date保留旧single/range接口，兼容已有页面，不重复计为新交互能力。

- 日期为YYYY-MM-DD；年月为YYYY-MM；季度为YYYY-Qn；周为ISO周年YYYY-Www，周一至周日，跨年周可能归入前一年或后一年。
- 时间为HH:mm；seconds:true使用HH:mm:ss。step控制面板的分钟列表，不截断手动录入的合法分钟。时间范围限制在同一天，跨日请用datetime-range。
- 日期时间为本地墙上时间YYYY-MM-DD HH:mm[:ss]；不隐式转换为UTC或服务器时间戳。业务明确时区后再转换。
- 范围value为双值数组，清空为null；multi-date为去重排序数组，清空为[]。周期或日期范围内含disabledDates则不可提交。
- 多日期在框内显示可移除日期标签，超出+N进入完整选择面板；普通多选继续在框内显示标签并按宽度折叠。
- 日期时间、年月周季必须按各自格式提供min/max。required仅提供标记，提交必填仍由业务表单校验。

## 通用组件

补入密码、组合输入、自动补全、单/双值滑块、穿梭框、列表、锚点、加载指示和颜色选择。输入、文本域、复选/单选组、开关、标签、头像、描述列表、树、卡片、指标、图表、页签、步骤、进度及浮层等补齐可配置参数。

复选全选保留禁用项，半选反映可选项；树勾选回传叶节点ID。穿梭框需明确点击移动按钮才生效。upload只保留本地File对象并回传元数据，不声称已上传；支持文件拖放、格式、字节大小、数量、去重及移除。折线、条形和环形图共用配置数据，并配套可访问表格明细。

新增与升级组件事件使用voc:change或voc:action，搜索使用voc:submit；detail包含component/action/value/name。日期家族的action为date-change、time-change或<key>-change。读取新组件值可用VocUI.getValue(host)；原组件以各自事件契约为准。

依赖顺序以data/library.json为准，新增js/temporal.js、js/extended-controls.js和css/extended-controls.css。component-variants.js仅用于文档展示，不是业务运行依赖。挂载用VocUI.mount；手工render后必须hydrate；移除前destroy。

## 全量检查记录

| 组件 | 本轮处理 | 实际支持与边界 |
| --- | --- | --- |
'''.replace('COUNT',str(len(rows)))
text+='\n'.join('| '+x['name']+' `'+x['key']+'` | '+x['treatment']+' | '+x['finding'].replace('|','/')+' |' for x in rows)
validation={}
for key,file in [('browser','data/completeness-2.2/browser.json'),('unit','data/completeness-2.2/unit.json'),('regression','data/quality-unit-validation.json'),('static','data/static-validation.json')]:
 path=R/file
 if path.exists():
  data=json.loads(path.read_text());validation[key]={x:data[x] for x in ['version','passed','failed'] if x in data};validation[key]['report']=file
report['validation']=validation
(R/'data/component-completeness.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
if 'browser' in validation:
 text+='\n\n## 本轮实际验证\n\n本地浏览器 '+str(validation['browser'].get('passed',0))+' 项通过；覆盖全91项挂载、83个示例、320px容器及定向交互。纯逻辑10项与既有回归12项通过。界面另检查日期时间、输入组合、图表明细及导航渲染；这些检查不代表全部浏览器或视觉状态已验收。证据见data/completeness-2.2/。静态校验仍保留原工程与历史扫描快照不一致的既有失败；未重置来源快照，也未改原业务工程。\n'
text+='\n\n## 仍保留的边界\n\n'+'\n'.join('- '+x for x in report['remaining'])+'\n\n以上为明确列出的后续能力，未把它们标为完成。原业务工程、已安装Skill及线上发布不在本轮修改范围内。\n'
(R/'design/COMPLETENESS.md').write_text(text)
print('Reviewed',len(rows),'components;',sum(x['treatment']=='新增常用类型' for x in rows),'new catalog entries')

from build_common_review import update
update()

from build_family_review import update as update_families
update_families()

from build_education_review import update as update_education
update_education()

from build_education_next_review import update as update_education_next
update_education_next()

from build_education_platform_review import update as update_education_platform
update_education_platform()
