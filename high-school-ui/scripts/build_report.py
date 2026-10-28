#!/usr/bin/env python3
"""Summarize executed checks; never replace source-history failures or old versions."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
def read(file):return json.loads((R/'data'/file).read_text())
meta=read('library.json');static=read('static-validation.json');browser=read('quality-browser-validation.json');unit=read('quality-unit-validation.json')
if (R/'data/interaction-details-validation.json').exists():
 candidate=read('interaction-details-validation.json')
 if candidate['version']==meta['version']:browser=candidate
current=[x for x in static['checks'] if x['name']!='Original scanned files unchanged']
historical=[x for x in static['checks'] if x['name']=='Original scanned files unchanged']
checks=[{'name':'当前静态完整性与渲染契约','status':'passed' if all(x['status']=='passed' for x in current) else 'failed','validatedVersion':meta['version'],'evidence':f"{sum(x['status']=='passed' for x in current)}/{len(current)}；源快照历史检查单列。"}]
checks += [{**x,'validatedVersion':'历史源码快照'} for x in historical]
checks += [{'name':'日期与CSV纯逻辑、API边界','status':'passed' if not unit['failed'] else 'failed','validatedVersion':unit.get('version','未记录'),'evidence':f"{unit['passed']}项通过，{unit['failed']}项失败；TZ={unit['timezone']}"}]
for key,label in [('defaultLayouts','组件默认DOM布局'),('containerLayouts','局部容器DOM布局'),('patternLayouts','页面组合DOM布局')]:
 rows=browser[key];bad=[x for x in rows if x.get('missing') or x.get('pageOverflow') or x.get('issues') or x.get('candidates')]
 checks.append({'name':label,'status':'passed' if not bad else 'failed','validatedVersion':browser['version'],'evidence':f"{len(rows)}次真实浏览器检查；{len(bad)}处可见溢出线索。排除隐藏面板、辅助文本、主动省略与内部滚动；不等同全状态视觉验收。"})
checks += [{**x,'validatedVersion':browser['version']} for x in browser['checks']]
for file,version in [('quality-browser-validation.json','2.1.0'),('teacher-agent-validation.json','2.0.0'),('composer-focus-layout-validation.json','2.0.0'),('reference-system-validation.json','2.0.0'),('browser-validation.json','1.0.0'),('delete-color-validation-1.0.1.json','1.0.1'),('resource-composer-validation.json','1.1.0'),('ai-accent-validation.json','1.2.0'),('picker-feedback-validation.json','1.3.0'),('generated-content-validation.json','1.4.0'),('workspace-slot-validation.json','1.5.0'),('reference-alignment-validation.json','1.6.0')]:
 if (R/'data'/file).exists():
  data=read(file);checks.extend({**c,'validatedVersion':data.get('version',version)} for c in data['checks'])
for name,label in [('browser','第三批业务DOM与配置'),('integration','三批跨组件联动'),('first-batch-regression','第一批业务回归'),('second-batch-regression','第二批业务回归'),('catalog-regression','全目录渲染与基础交互'),('common-regression','表格表单回归'),('family-regression','其他组件家族回归'),('unit','第三批业务规则'),('unit-regressions','既有业务与公共规则回归')]:
 path=R/'data/education-2.7'/f'{name}.json'
 if path.exists():
  data=json.loads(path.read_text());checks.append({'name':label,'status':'passed' if data['failed']==0 else 'failed','validatedVersion':data['version'],'evidence':f"{data['passed']}项通过/{data['failed']}项失败；{str(path.relative_to(R))}"})
for name,label in [('browser','业务示例页面与全部配置'),('catalog-regression','含业务数据的画廊回归'),('unit','示例数据和依赖边界')]:
 path=R/'data/examples-2.7.1'/f'{name}.json'
 if path.exists():
  data=json.loads(path.read_text());checks.append({'name':label,'status':'passed' if data['failed']==0 else 'failed','validatedVersion':data['version'],'evidence':f"{data['passed']}项通过/{data['failed']}项失败；{str(path.relative_to(R))}"})
summary=f"v{meta['version']}：{meta['components']}项组件、{meta['pagePatterns']}类页面组合、{meta['tokens']}个设计变量。当前浏览器布局记录与已执行交互先列；历史记录保留验证版本。原业务工程与最初扫描快照的差异继续登记失败，不重置基线。"
limitations='本轮只更新本地组件库与预览，未修改原业务工程、推送GitHub或覆盖已发布Skill包。'+ '；'.join(browser['limitations'])+'。当前仍为HTML交互组件；生产接口、真实上传/解析、权限、审批、排课引擎和模型未实现。'
report={'version':meta['version'],'date':'2026-10-28','timezone':'Asia/Shanghai','summary':summary,'checks':checks,'limitations':limitations}
(R/'data/validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(summary)
