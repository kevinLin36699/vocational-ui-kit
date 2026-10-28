"""Current third-batch evidence and explicit cross-batch integration coverage."""
import json
from pathlib import Path
from education_platform_contracts import DATA
R=Path(__file__).resolve().parents[1]
def update():
 catalog=json.loads((R/'data/components.json').read_text());version=json.loads((R/'data/library.json').read_text())['version'];validation={}
 for key in ['browser','integration','first-batch-regression','second-batch-regression','catalog-regression','common-regression','family-regression','unit','unit-regressions','static']:
  path=R/'data/education-2.7'/f'{key}.json'
  if path.exists():
   data=json.loads(path.read_text());validation[key]={k:data[k] for k in ['version','passed','failed','observedBrowserErrors'] if k in data};validation[key]['report']=str(path.relative_to(R))
 entries=[dict(key=c['key'],name=c['name'],description=c['description'],parameters=c['api']['parameters'],states=c['states'],implementationFiles=c['implementationFiles'],source='用户明确授权第三批成长就业、办学评估与学校运营业务扩展；沿用公共蓝白标准',verification='data/education-2.7/；配置与普通操作及跨批链路单独验证',remaining='真实服务、上传、鉴权、并发和持久化需业务适配') for c in catalog if c['key'] in DATA]
 report=dict(version=version,componentCount=9,scenarioCount=36,allBusinessComponentCount=22,allBusinessScenarioCount=86,integrationFlowCount=7,integrationKindCount=14,components=entries,validation=validation,remaining=['真实业务服务、权限、上传、持久化与服务端并发事务','全浏览器、触摸设备和完整无障碍认证','历史原工程扫描快照差异保留，不改原工程或基线'])
 (R/'data/education-platform-components.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 for file in ['component-completeness.json','component-alignment.json']:
  p=R/'data'/file;data=json.loads(p.read_text());data['version']=version
  if file=='component-completeness.json':data.update(educationPlatformReview='data/education-platform-components.json',educationPlatformValidation=validation)
  for row in data['components']:
   if row['key'] in DATA:row.update(source='js/education-platform.js',finding=DATA[row['key']][1],treatment='第三批业务扩展及三批联查',verification='data/education-2.7/、design/EDUCATION_PLATFORM.md',remaining='真实服务、上传、鉴权、并发和持久化需业务适配')
  p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 results='\n'.join('- '+k+'：'+str(v.get('passed','—'))+'项通过 / '+str(v.get('failed','—'))+'项失败；'+v['report'] for k,v in validation.items())
 p=R/'design/EDUCATION_PLATFORM.md';p.write_text(p.read_text().split('\n## 本轮验证记录')[0]+'\n## 本轮验证记录\n\n'+(results or '浏览器执行后更新证据。')+'\n')
 p=R/'design/COMPLETENESS.md';p.write_text(p.read_text().split('\n## v2.7 第三批与三批联查')[0]+'\n## v2.7 第三批与三批联查\n\n新增九类、36组配置；三批合计22类、86组配置，目录118项。七条整链路/14种显式关联，支持替换配置、真实普通表单及异常复核。入口[三批联动](../examples/education-integration.html)，规则见[EDUCATION_PLATFORM.md](EDUCATION_PLATFORM.md)。\n\n'+results+'\n')
 print('Education platform:',len(entries),'components;',len(validation),'verification reports')
if __name__=='__main__':update()
