"""Versioned second-batch evidence; preserve earlier batches and original source snapshots."""
import json
from pathlib import Path
from education_next_contracts import DATA
R=Path(__file__).resolve().parents[1]
def update():
 catalog=json.loads((R/'data/components.json').read_text());version=json.loads((R/'data/library.json').read_text())['version'];validation={}
 for key,name in [('browser','browser'),('firstBatchRegression','first-batch-regression'),('catalogRegression','catalog-regression'),('commonRegression','common-regression'),('familyRegression','family-regression'),('unit','unit'),('static','static')]:
  path=R/'data/education-2.6'/f'{name}.json'
  if path.exists():
   d=json.loads(path.read_text());validation[key]={k:d[k] for k in ['version','passed','failed','observedBrowserErrors'] if k in d};validation[key]['report']=str(path.relative_to(R))
 entries=[{'key':c['key'],'name':c['name'],'implementationFiles':c['implementationFiles'],'description':c['description'],'parameters':c['api']['parameters'],'states':c['states'],'source':'前轮业务方向建议中的组织、实训、学习过程、资源版本与评价，依据本轮明确授权扩展；不冒称原代码已存在','verification':'具体类型、状态、规则和交互断言见data/education-2.6/','remaining':'真实服务、权限、上传、并发与持久化由业务适配'} for c in catalog if c['key'] in DATA]
 report={'version':version,'componentCount':len(entries),'scenarioCount':28,'components':entries,'validation':validation,'remaining':['成长就业、办学评估与学校运营尚未包含在第二批','HTML交互组件，实际服务、权限和持久化需业务接入','资源差异为提供文本的逐行对照，不含PDF/Word二进制解析','未做全部浏览器、触摸设备和完整无障碍认证']}
 (R/'data/education-next-components.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 current=json.loads((R/'data/component-completeness.json').read_text());current['educationNextReview']='data/education-next-components.json';current['educationNextValidation']=validation
 for row in current['components']:
  if row['key'] in DATA:row.update(source='js/education-next.js',finding=DATA[row['key']][1],treatment='第二批高职教业务扩展',verification='data/education-2.6/与design/EDUCATION_NEXT.md',remaining='真实服务、权限、文件持久化和并发由业务适配')
 (R/'data/component-completeness.json').write_text(json.dumps(current,ensure_ascii=False,indent=2)+'\n')
 alignment=json.loads((R/'data/component-alignment.json').read_text())
 for row in alignment['components']:
  if row['key'] in DATA:row.update(reference='当前蓝白公共设计标准与第二批业务方向扩展',kind='scenario-extension',implementation=DATA[row['key']][1],verification='配置与实际DOM交互；证据见EDUCATION_NEXT.md')
 (R/'data/component-alignment.json').write_text(json.dumps(alignment,ensure_ascii=False,indent=2)+'\n')
 results='\n'.join('- '+key+'：'+str(v.get('passed','—'))+'项通过 / '+str(v.get('failed','—'))+'项失败；'+v['report'] for key,v in validation.items()) or '验证执行后写入data/education-2.6/。'
 p=R/'design/EDUCATION_NEXT.md';text=p.read_text().split('\n## 本轮验证记录')[0]+'\n## 本轮验证记录\n\n'+results+'\n\n静态检查中的原工程历史扫描快照差异保留为失败；本轮仅修改组件库，不修改原工程或重置来源快照。检查通过范围以报告断言为准，不等于生产服务、全设备或全状态视觉认证。\n';p.write_text(text)
 p=R/'design/COMPLETENESS.md';text=p.read_text().split('\n## v2.6 第二批业务组件')[0];p.write_text(text+'\n## v2.6 第二批业务组件\n\n新增七类、28组配置，组件总数'+str(len(catalog))+'。入口[education-next.html](../examples/education-next.html)；规则、接口与边界见[EDUCATION_NEXT.md](EDUCATION_NEXT.md)。\n\n'+results+'\n')
 print('Education second batch:',len(entries),'components;',len(validation),'verification reports')
if __name__=='__main__':update()
