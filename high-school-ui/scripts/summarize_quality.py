#!/usr/bin/env python3
"""Summarize existing browser evidence without executing or inventing UI checks."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
def load(file):return json.loads((R/'data'/file).read_text())
meta=load('library.json');browser=load('quality-browser-validation.json');review=load('ui-review.json');catalog={c['id']:c for c in load('components.json')}
if (R/'data/interaction-details-validation.json').exists():
 candidate=load('interaction-details-validation.json')
 if candidate['version']==meta['version']:browser=candidate
if browser['version']!=meta['version']:raise SystemExit('Browser evidence belongs to another version; rerun browser checks first.')
links={
 'date':['日期'], 'time-picker':['时间'], 'number':['数字'],
 'table':['表格'], 'toolbar':['表格'], 'select':['大量选项'], 'multiselect':['大量选项','多选'], 'pagination':['分页'], 'tree':['树节点'], 'chart':['图表'],
 'tree-select':['组织、人员','组织多选','树多选'], 'person-picker':['组织、人员'], 'academic-term':['组织、人员'],
 'collapse':['时间、评价'], 'rate':['时间、评价'], 'calendar':['事件日历'], 'notification':['时间、评价'],
 'image-preview':['图片预览'], 'confirm':['图片预览'], 'resource':['资源列表'], 'batch-import':['名单'],
 'composer':['AI 资源'], 'chat':['AI','320px'], 'conversation':['320px'], 'workspace':['AI 资源','AI 失败'],
 'upload':['通用上传']}
controls=set(load('control-contracts.json')['parameters'])-{'table','toolbar','select','multiselect','batch-import'}
for item in review['components']:
 c=catalog[item['id']];key=c['key'];defaults=[x for x in browser['defaultLayouts'] if x['key']==key];containers=[x for x in browser['containerLayouts'] if x['component']==key]
 actual=[x for x in browser['checks'] if any(word in x['name'] for word in links.get(key,[]))]
 item['validation']='layout-and-sampled-interaction-checked' if actual else 'default-layout-checked'
 item['scenario']=c['category']+' / '+c['name']
 item['resolution']=c['description'] if key in controls|{'table','toolbar','batch-import','multiselect','tree','chart'} else '统一弱阴影、无衬线控件、可收缩布局和长文本规则；'+('为超长按钮文案增加独立省略层及完整title。' if key=='button' else '窄容器收起侧栏并保留可达图标。' if key=='shell' else '保留原组件标识与适用交互。')
 item['implementationFiles']=['css/refinements.css','js/data-table.js' if key in {'table','toolbar'} else 'js/batch-import.js' if key=='batch-import' else 'js/controls.js' if key in controls else 'js/voc-ui.js']
 item['coverage']={'defaultViewports':[x['viewport'] for x in defaults],'localWidths':[int(x['container']) for x in containers],'interactionChecks':[x['name'] for x in actual],'allStatesVerified':False}
 item['evidence']=['data/quality-browser-validation.json#'+key]+[x['evidence'] for x in actual]
 item['remaining']='完整状态矩阵、多浏览器和真实业务服务未逐项验收；不把默认布局检查当作这些项目通过。'
review['patternValidation']='default-layout-checked'
review['patterns']=[{'id':key,'viewports':[x['viewport'] for x in browser['patternLayouts'] if x['key']==key],'status':'default-layout-checked'} for key in dict.fromkeys(x['key'] for x in browser['patternLayouts'])]
(R/'data/ui-review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
md=f'''# 逐项整改与实际验收 · {meta['version']}

2.1系列共有{meta['components']}项组件、{meta['pagePatterns']}类页面组合和122个设计变量；本次2.1.1不增加数量，重点修正交互与视觉细节。历史来源证据保留。只更新本地组件库，不修改原业务工程、推送GitHub或覆盖已发布Skill。

## 实际检查范围

- 默认组件：{meta['components']}项 × 1440/1280/1024/768px，共{len(browser['defaultLayouts'])}次真实浏览器DOM布局检查。
- 局部容器：{meta['components']}项 × 320/480px，共{len(browser['containerLayouts'])}次；舞台内边框使实际clientWidth为318/478px。
- 页面组合：{meta['pagePatterns']}类 × 四档视口，共{len(browser['patternLayouts'])}次。
- 上述最终记录均没有未处理的可见横向溢出线索。排除隐藏/收起面板、辅助文本、主动省略与内部滚动，不代表480张截图逐张视觉批准。
- 当前重点实测分页、树行、图表、日期、多选和实际组合；2.1.0的其他测试仍保留原版本，不提升为本次通过。当前细节与截图见INTERACTION_DETAILS.md。
- 日期、表格、AI、选择、文件和导入的实际操作记录如下。默认布局、静态渲染和真实交互分开登记。

## 逐项整改

| 标识 / 场景 | 问题或缺口 | 处理 | 验收范围 |
| --- | --- | --- | --- |
'''
for x in review['components']:
 names='；'.join(x['coverage']['interactionChecks']) or '仅默认布局；其他状态未逐项验收'
 md+='| '+x['id']+' / '+x['name']+' | '+x['issue']+' | '+x['resolution']+' | 四档视口、两档容器；'+names+' |\n'
md+='\n## 已实测的关键交互\n\n| 检查 | 结果 | 实际证据 |\n| --- | --- | --- |\n'
for x in browser['checks']:md+='| '+x['name']+' | '+x['status']+' | '+x['evidence'].replace('|','／')+' |\n'
md+='''
## 截图与复查入口

- data/review-2.1/date-before-user.png：用户提供的旧日期双框截图，保留为前态证据。
- data/review-2.1/date-after.png：统一范围外框、相邻双月、范围高亮。
- data/review-2.1/table-after.png：统一筛选、数据密度、操作列与分页。
- data/review-2.1/ai-after.png：教师输入和空生成容器的当前视觉。
- examples/quality-review.html：日期、管理、资源与AI组合。
- examples/import.html：本地名单流程；fixtures只含虚构测试数据。
- examples/stress.html：全部组件、长文本与容器宽度切换。
- examples/control-states.html：跨年、闰年、边界、禁用与只读日期。

## 缺口与未验收范围

这是HTML交互组件库，保留生产适配边界，不承诺每个状态已验收。尚未覆盖全组件完整状态矩阵、所有原业务页面、多浏览器、真实移动设备、系统文件对话框取消、上传大小上限的浏览器端边界、图片失败恢复和完整WCAG认证。日期与CSV的纯逻辑测试不能替代上述检查。

真实上传/解析、持久化、审批、角色权限、模型、资源服务、自动排课、PPT/视频/考试引擎仍由业务项目实现。部分既有组件仍是默认配方，不能假设未声明参数可用；参见API.md参数矩阵。生成区域只提供空容器，按业务需求挂载内容。

静态检查保留一项历史失败：原业务工程与最初来源扫描快照已有差异；不重置该基线。当前源码完整性、日期/CSV纯逻辑和实际浏览器证据分别见static-validation.json、quality-unit-validation.json、quality-browser-validation.json。该历史差异不代表本轮修改了原业务代码。
'''
md+='\n## 当前细节修正版\n\n本次截图与直接预览：examples/design-refinement.html、data/review-2.1.1/overview-after.png、data/review-2.1.1/multiselect-gallery.png。实际证据以data/interaction-details-validation.json为准；quality-browser-validation.json是2.1.0历史记录。\n'
(R/'design/QUALITY_REVIEW.md').write_text(md)
print('Wrote per-component evidence and review; no new browser checks inferred.')
