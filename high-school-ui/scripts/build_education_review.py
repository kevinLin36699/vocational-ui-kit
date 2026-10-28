"""Record current vocational batch scope and versioned verification without rewriting old evidence."""
import json,re
from pathlib import Path
from education_contracts import DATA
R=Path(__file__).resolve().parents[1]
def update():
 meta=json.loads((R/'data/library.json').read_text());catalog=json.loads((R/'data/components.json').read_text());version=meta['version'];validation={}
 for key,file in [('browser','browser'),('catalogRegression','catalog-regression'),('commonRegression','common-regression'),('familyRegression','family-regression'),('unit','unit'),('static','static')]:
  p=R/'data/education-2.5'/f'{file}.json'
  if p.exists():
   data=json.loads(p.read_text());validation[key]={k:data[k] for k in ['version','passed','failed','observedBrowserErrors'] if k in data};validation[key]['report']=str(p.relative_to(R))
 entries=[{'key':c['key'],'name':c['name'],'implementationFiles':c['implementationFiles'],'description':c['description'],'parameters':c['api']['parameters'],'states':c['states'],'source':'本次明确授权的业务组件扩展，依据现有教学、出卷、提交批阅与评价流程','validation':'数据规则、22组类型配置、适用状态与320px、定向业务交互；具体通过范围见对应报告'} for c in catalog if c['key'] in DATA]
 report={'version':version,'components':entries,'componentCount':len(entries),'scenarioCount':22,'validation':validation,'boundaries':['HTML交互原型，不接入真实权限、上传、数据库、成绩公布或模型服务','目录最多三层；支持本平台五类常用试题','取消只使本地等待失效，后端的取消、回滚、幂等和并发检查由业务实现','不提供自动判分、自动排课、跨设备草稿同步或全浏览器认证']}
 (R/'data/education-components.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 current=json.loads((R/'data/component-completeness.json').read_text());current['educationReview']='data/education-components.json';current['educationValidation']=validation
 for row in current['components']:
  if row['key'] in DATA:row.update(source='js/education-controls.js',finding=DATA[row['key']][1],treatment='第一批高职教业务扩展',verification='data/education-2.5/与design/EDUCATION.md',remaining='真实服务、权限和持久化由业务适配')
 (R/'data/component-completeness.json').write_text(json.dumps(current,ensure_ascii=False,indent=2)+'\n')
 alignment=json.loads((R/'data/component-alignment.json').read_text())
 for row in alignment['components']:
  if row.get('key') in DATA:row.update(implementation=DATA[row['key']][1],verification='第一批业务配置与交互验证，见EDUCATION.md')
 (R/'data/component-alignment.json').write_text(json.dumps(alignment,ensure_ascii=False,indent=2)+'\n')
 p=R/'design/EDUCATION.md';text=p.read_text().split('\n## 本轮验证记录')[0];text+='\n## 本轮验证记录\n\n'+'\n'.join('- '+key+'：'+str(value.get('passed','—'))+'项通过 / '+str(value.get('failed','—'))+'项失败；'+value['report'] for key,value in validation.items())+'\n\n静态检查中的原工程历史快照差异保留为失败，不修改原工程或重置历史来源。检查通过不等于生产服务、全设备和全部视觉状态均已验收。\n';p.write_text(text)
 p=R/'design/COMPLETENESS.md';text=p.read_text().replace('## 本轮验证','## 既有验证记录（版本见报告）');text+='\n\n## v2.5 第一批业务组件\n\n新增六类公共业务组件，目录总数'+str(len(catalog))+'。22组配置及类型、状态、回执、版本与校验规则见[EDUCATION.md](EDUCATION.md)；预览入口[education.html](../examples/education.html)。当前验证记录：\n\n'+'\n'.join('- '+key+'：'+str(value.get('passed','—'))+'通过 / '+str(value.get('failed','—'))+'失败；'+value['report'] for key,value in validation.items())+'\n';p.write_text(text)
 print('Education batch:',len(entries),'components;',len(validation),'verification reports')
if __name__=='__main__':update()
