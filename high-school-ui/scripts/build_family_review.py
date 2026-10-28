"""Versioned review of the whole library excluding table/form. Historical evidence stays intact."""
import json
from pathlib import Path
from family_contracts import PARAMS
R=Path(__file__).resolve().parents[1]
def update():
 catalog=json.loads((R/'data/components.json').read_text());meta=json.loads((R/'data/library.json').read_text());version=meta['version'];entries=[]
 types={'button':['primary','soft','outline','ghost','destructive','sm/default/lg'], 'tag':['semantic','checkable','closable'],'badge':['status','count','dot'],'avatar':['image/text','circle/square','group'],'description':['1/2/3 columns','bordered','copyable'],'progress':['line','circle','dashboard','steps','indeterminate'],'timeline':['vertical','horizontal','alternate','pending'],'tabs':['line','card','vertical','closable','dynamic'],'menu':['action','checkbox','radio','separator','submenu'],'drawer':['left','right','top','bottom'],'list':['list','grid','search/sort','incremental','remote append'],'calendar':['month','week','day','agenda'],'image-preview':['single','gallery'],'carousel':['text/image','bounded/loop','manual/automatic'],'splitter':['horizontal','vertical'],'pagination':['full','simple'],'message':['user','assistant','completed/streaming/failed/stopped'],'approval':['draft','review','approved','rejected','distributed'],'navigation-menu':['horizontal','vertical','nested','collapsed'],'course-card':['required/elective labels','cover/placeholder','local favorite']}
 hardening={'select','multiselect','cascade','tree-select','academic-term','person-picker','steps','anchor','autocomplete','input','password','textarea','search','process'}
 for c in catalog:
  if c['key'] in ['table','toolbar','form']:continue
  k=c['key'];entry={'key':k,'name':c['name'],'category':c['category'],'treatment':'parameterized-family-upgrade' if k in PARAMS else 'interaction-hardening' if k in hardening else 'review-and-retain','types':types.get(k,[]),'states':c['states'],'implementationFiles':c.get('implementationFiles',[]),'verification':'本轮目录默认与常用状态挂载、320px检查；定向交互以浏览器报告具体断言为准','remaining':'服务端权限、数据持久化、生产网络或完整浏览器认证未接入'}
  entries.append(entry)
 reports={}
 for key,name in [('families','family-browser'),('catalogRegression','catalog-regression'),('tableFormRegression','table-form-regression'),('unit','unit')]:
  p=R/'data/families-2.4'/f'{name}.json'
  if p.exists():
   data=json.loads(p.read_text());reports[key]={k:data.get(k) for k in ['version','passed','failed','observedBrowserErrors']};reports[key]['path']=str(p.relative_to(R))
 report={'version':version,'scope':'All catalog entries except table/form/toolbar','reviewedCount':len(entries),'upgradedCount':len([x for x in entries if x['treatment']=='parameterized-family-upgrade']),'hardenedCount':len([x for x in entries if x['treatment']=='interaction-hardening']),'components':entries,'validation':reports,'remaining':['日历为本地事件查看，不提供自动排课、拖拽改期、时区转换或冲突服务','图片以预览为主，不提供裁剪/批注/媒体编辑；轮播不含视频播放器','HTML原型组件，没有React/Vue框架包和可视化页面搭建器','交互权限仅为客户端约束，真实上传、消息投递、审批、分发、Agent/模型执行需业务回执','全浏览器、触摸设备、屏幕阅读器与全量视觉状态验收尚未覆盖']}
 (R/'data/component-families.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 text='''# 全家族组件完整性 · v2.4.0

[全家族交互实验室](../examples/families.html)逐类提供目录与配置，覆盖基础、录入、展示、导航布局、反馈、高职教业务、AI交互。表格/表单/toolbar沿用TABLE_FORM.md。组件总数为96项，本次范围为其余93项；新增导航菜单、图文轮播、可调整分栏与局部返回顶部。

## 本轮补齐

- 基础与内容：单实例可配置按钮、链接、可选标签、计数/圆点徽标、头像组展开与失败回退、三列描述与复制、可折叠卡片、精度指标、横纵时间线、环形/仪表/分段/不确定进度、静态/动画骨架和局部遮罩。
- 导航：可关闭/新增请求/未保存保护页签、嵌套横纵导航、同层面包屑、完整/简洁分页、手风琴键盘操作、滚动锚点跟随、分栏键盘及拖动、局部返回顶部。
- 反馈：普通/复选/单选/子菜单，焦点与悬停提示、说明浮层、四向抽屉、可控弹窗、危险确认、异步防重和失败保留、可关闭提示与多动作结果反馈。
- 数据内容：列表/网格、搜索排序与逐批显示，异步追加失败保留；日历月/周/日/日程、边界和禁选、键盘选日；图片组切换、缩放旋转、重置、重试；通知筛选、单项/批量已读及禁用项保护。
- 业务与AI：课程卡片、助手目录、任务预填、消息正文/附件/反馈、Markdown、来源、成果摘要、审核状态和平台外壳均接受业务配置。没有把固定课程名称或固定问题放进通用控制器。自定义公开处理阶段可通过process.stages传入。
- 既有录入：只读单选/多选/树选择/人员选择锁定入口和移除；树禁用父项继承；保留禁用已选人员；中文组合输入完成后才提交值或搜索。

## 参数、状态与使用约定

依次加载data/library.json内styles与runtime，最后的family-controls.js注册本轮公共渲染器。使用VocUI.mount(host,key,props)，切换和移除前调用destroy；不直接运行预览控制器。

参数详见API.md和data/control-contracts.json。项目ID唯一；tabs/segmented使用value作为ID，其余集合使用id。层级目录ID在整棵树内唯一。文本与Markdown均转义；只允许已定义的安全链接和图片地址。

- loading/empty/failed/forbidden是本轮数据组件的内容状态，遮蔽正文。forbidden不会把数据仅仅藏进折叠区。静态分隔线、骨架、加载指示和结果页不套用不适用的状态。
- disabled锁定动作；readonly用于保留当前值、禁止数据修改，仍可查看允许浏览的内容。树可以在只读时展开目录，但不可改变选中项。
- 旧录入组件的空态由options/items/nodes等空集合提供，无匹配由实际搜索产生；focus/hover为真实浏览器状态，不使用state字符串伪造。
- 示例“下一次模拟失败”仅绑定本地演示处理器；确认成功文案明确注明未写入真实业务。无处理器只发出动作，不自动改变审核状态或声称已保存。

## 本轮实例接口

```javascript
VocUI.mount(host,'notification',{items:[{id:'n1',title:'资料待复核',read:false}]});
VocFamilies.getState(host); // 当前值、项目、请求编号、挂起状态等快照
VocFamilies.setState(host,'failed','读取失败，可重试');
VocFamilies.setLoader(host, async(params,{signal,requestId}) => {
  return {items: await businessRead({signal})};
});
```

- getValue/getState：读取当前值/快照；VocUI.getValue也识别本轮组件。
- setItems(host,items)：替换列表、通知、导航、页签、图片组等集合，保留仍有效的选中ID；无效页签回退首个可用项。替换会中断旧请求。
- setState(host,state,message?)：切换适用内容状态；不会自动执行真实读取。retry通过loader或load-request动作接续。
- setHandler(host, async(request,{signal,requestId})=>({ok,message?}))：按钮、弹窗、确认、消息重试、审核动作处理器。request含action与value。挂起时防重复；取消、卸载、替换请求将使迟到响应失效。
- setLoader(host, async({query,cursor},{signal,requestId})=>({items,cursor?,hasMore?}),{immediate?:true})；load(host,{append?:false})。list追加失败保留原记录与游标，重复ID明确报错，不悄悄覆盖。
- cancel(host)：取消本地等待并AbortSignal；服务端是否实际中断或回滚由业务决定。
- setPagination(host,{total?,page?,pageSize?})：总数变化后裁剪页码；setProgress(host,value,{status?})更新进度。
- setApproval(host,value)：应用业务确认状态。默认动作转换为draft→review→approved→distributed；review可退回rejected，填原因后才能退回；rejected可重新提交review。没有处理器时发出approval-request，由业务接续。

所有事件通过voc:action或voc:change冒泡，detail包含component/action/value。常用action：tab/tab-add-request/tab-remove、navigate、pagination、list-search/list-sort/list-action、calendar-select/calendar-view/calendar-event、notice-open/read-all、menu、confirm/close、agent-select/task-prepare、message-feedback、citation-open/result-open、approval-request/approval-state、shell-navigate。

需要主站路由、实际跳转或新增页签时，由业务收到请求后调用setItems或自身路由；本轮不会为用户自动创建业务对象、发送消息、发布成果或执行模型任务。

自动轮播默认关闭；鼠标悬停、焦点在组件内、页面隐藏时暂停；减少动画偏好下不自动滚动。工具提示支持上下左右与边缘翻转。浮层优先置于所属dialog顶层，退出恢复焦点；drawer提供left/right/top/bottom。异步操作结束前关闭弹层会中断本地等待。

## 逐项复查与证据

目录挂载/状态结构/320px通过只代表这些范围；定向交互结果应看具体断言。没有给只测挂载的组件标记“全部行为验收”。本轮浏览器检查入口examples/family-checks.html，既有回归examples/completeness-checks.html、examples/common-checks.html。

| 组件 | 本轮处理 | 类型 / 状态记录 |
| --- | --- | --- |
'''
 text=text.replace('v2.4.0','v'+version).replace('组件总数为96项，本次范围为其余93项','组件总数为'+str(len(catalog))+'项，表格/表单/toolbar之外共'+str(len(entries))+'项；第一批业务组件另见EDUCATION.md，第二批见EDUCATION_NEXT.md')
 for x in entries:
  treatment={'parameterized-family-upgrade':'参数化升级','interaction-hardening':'交互补强','review-and-retain':'复查并沿用'}[x['treatment']]
  text+=f"| {x['name']} `{x['key']}` | {treatment} | "+'; '.join(x['types']+x['states'])+' |\n'
 text+='\n## 验证报告\n\n'+('\n'.join('- '+k+'：'+str(v['passed'])+'通过 / '+str(v['failed'])+'失败，'+v['path'] for k,v in reports.items()) or '浏览器验证执行后写入data/families-2.4/。')
 text+='\n\n静态检查仍保留原工程与历史来源快照差异的既有失败；本轮未改原业务工程，不重置历史快照。\n\n## 明确边界\n\n'+'\n'.join('- '+x for x in report['remaining'])+'\n'
 (R/'design/FAMILIES.md').write_text(text)
 completeness=R/'design/COMPLETENESS.md'
 summary='\n\n## v2.4 其他家族复查\n\n表格/表单/toolbar之外的'+str(len(entries))+'项已逐项记录，其中'+str(report['upgradedCount'])+'项作参数化升级。入口：[全家族交互实验室](../examples/families.html)；类型、状态、交互与边界见[FAMILIES.md](FAMILIES.md)。本轮报告：data/component-families.json。\n'
 completeness.write_text(completeness.read_text()+summary)
 current=json.loads((R/'data/component-completeness.json').read_text());current['familyReview']='data/component-families.json';current['familyValidation']=reports;(R/'data/component-completeness.json').write_text(json.dumps(current,ensure_ascii=False,indent=2)+'\n')
 alignment=json.loads((R/'data/component-alignment.json').read_text())
 for row in alignment['components']:
  if row.get('key') in PARAMS:row.update(implementation=next(c['description'] for c in catalog if c['key']==row['key']),verification='本轮参数化实现与浏览器定向检查；详见data/component-families.json')
 (R/'data/component-alignment.json').write_text(json.dumps(alignment,ensure_ascii=False,indent=2)+'\n')
 print('Family review:',len(entries),'components;',report['upgradedCount'],'upgraded')
if __name__=='__main__':update()
