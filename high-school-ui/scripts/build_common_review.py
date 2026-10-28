# -*- coding: utf-8 -*-
"""Upgrade the current completeness review without replacing historical snapshots."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def update():
 meta=json.loads((R/'data/library.json').read_text());catalog=json.loads((R/'data/components.json').read_text());review=json.loads((R/'data/component-completeness.json').read_text());by={x['key']:x for x in review['components']}
 files={'table':'js/advanced-table.js','toolbar':'js/advanced-table.js','form':'js/schema-form.js','chart':'js/common-extras.js','tree':'js/extended-controls.js','richtext':'js/common-extras.js'}
 for c in catalog:
  if c['key'] in files:
   row=by[c['key']];row.update(source=files[c['key']],finding=c['description'],treatment='本轮通用能力升级' if c['key']!='richtext' else '新增常用字段',remaining='实际服务与专用编辑器按业务接入',verification='本轮源码、浏览器定向交互与窄容器检查；见data/common-2.3/')
 review.update(version=meta['version'],currentCount=len(catalog),remaining=['虚拟表固定行高；树/分组/展开/合并与多层固定列的组合限制见TABLE_FORM.md','重复字段组支持一层；可视化低代码搭建器和复杂嵌套由业务适配','图表支持非负分类数据与左右两轴；专用地理、3D、股票图不在本通用实现中','真实上传、审批、权限、持久化与生产框架封装','自动排课和Office/PPT/PDF/视频等专用编辑器','全浏览器、全部移动端与无障碍认证'])
 validation={}
 for key,file in [('browser','data/common-2.3/browser.json'),('regressionBrowser','data/common-2.3/regression-browser.json'),('unit','data/common-2.3/unit.json'),('static','data/static-validation.json')]:
  p=R/file
  if p.exists():
   data=json.loads(p.read_text());validation[key]={k:data[k] for k in ['version','passed','failed','observedBrowserErrors'] if k in data};validation[key]['report']=file
 review['currentValidation']=validation;(R/'data/component-completeness.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
 alignment=json.loads((R/'data/component-alignment.json').read_text());known={c['key']:c for c in alignment['components']}
 for c in catalog:
  if c['key'] in files and c['key'] in known:known[c['key']].update(implementation=c['description'],verification='本轮本地源码、参数和实际浏览器检查；不是线上逐像素对照')
 alignment.update(version=meta['version'],componentCount=len(catalog));(R/'data/component-alignment.json').write_text(json.dumps(alignment,ensure_ascii=False,indent=2)+'\n')
 text='# 组件完整性与变体 v'+meta['version']+'\n\n当前目录共'+str(len(catalog))+'项。本轮继续把表格与表单升级为真正可配置的公共组件，并补齐交互图表、树勾选策略和基础富文本字段。历史扫描与验证保留为各自版本证据，不把目录数量当设计验收。\n\n[常用组件实验室](../examples/table-form.html)提供12类表格、11类表单和6类补充交互，支持直接编辑JSON配置。[前一轮家族总览](../examples/completeness.html)保留日期、选择和反馈变体。\n\n## 本轮已补齐\n\n- 表格：平铺、树形、分组、多层表头、合并、固定列、行详情、虚拟滚动、跨页选择、行列调整、行内/弹窗编辑与同步校验；本地数据和远程查询/写入分开。\n- 表单：任意fields/values、纵横/行内、分区/分步、联动、重复项、同步/异步校验、跨字段约束、错误定位、取消与失败恢复、异步加载和业务回执。\n- 图表：区间缩放、系列切换、双轴组合、下钻和明细同步。树支持级联/独立勾选与禁用继承。富文本支持安全格式、粘贴、链接和表单集成。\n\n类型、参数、事件、实例方法和组合约束详见[TABLE_FORM.md](TABLE_FORM.md)，通用参数矩阵见[API.md](API.md)。日期时间原有13类入口继续沿用，格式与时区规则见CONTROLS.md。\n\n## 全量逐项记录\n\n| 组件 | 处理 | 实际支持与边界 |\n| --- | --- | --- |\n'
 text+='\n'.join('| '+x['name']+' `'+x['key']+'` | '+x['treatment']+' | '+x['finding'].replace('|','/')+' |' for x in review['components'])
 text+='\n\n## 本轮验证\n\n'
 text+='\n'.join('- '+key+'：'+str(v.get('passed','—'))+'项通过、'+str(v.get('failed','—'))+'项失败；'+v['report'] for key,v in validation.items())
 text+='\n\n静态检查保留“原工程与历史来源快照不同”的既有失败；不重置快照或修改原业务工程。断言通过不代表全部视觉状态、全部浏览器或生产服务已验收。\n\n## 保留边界\n\n'+'\n'.join('- '+x for x in review['remaining'])+'\n\n本轮只修改本地组件库及预览，不覆盖已安装Skill、不发布、不改原业务工程。\n'
 (R/'design/COMPLETENESS.md').write_text(text)
 print('Current common-component review:',meta['version'],len(catalog),'entries')
if __name__=='__main__':update()
