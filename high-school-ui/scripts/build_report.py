#!/usr/bin/env python3
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
meta=json.loads((R/'data/library.json').read_text())
static=json.loads((R/'data/static-validation.json').read_text())
checks=[{'name':'当前静态完整性与渲染契约','status':'passed' if not static['failed'] else 'failed','validatedVersion':meta['version'],'evidence':f"{static['passed']}项通过，{static['failed']}项失败；原平台扫描快照差异如实保留，未重置历史基线。"}]
for file,version in [('teacher-agent-validation.json','2.0.0'),('composer-focus-layout-validation.json','2.0.0'),('reference-system-validation.json','2.0.0'),('browser-validation.json','1.0.0'),('delete-color-validation-1.0.1.json','1.0.1'),('resource-composer-validation.json','1.1.0'),('ai-accent-validation.json','1.2.0'),('picker-feedback-validation.json','1.3.0'),('generated-content-validation.json','1.4.0'),('workspace-slot-validation.json','1.5.0'),('reference-alignment-validation.json','1.6.0')]:
    p=R/'data'/file
    if p.exists():
        data=json.loads(p.read_text())
        checks.extend({**c,'validatedVersion':data.get('version',version)} for c in data['checks'])
report={'version':meta['version'],'date':'2026-10-27','timezone':'Asia/Shanghai','summary':'v2.0.0按DESIGN.md统一60项组件、14类组合与122个设计变量，保留蓝白及局部蓝紫、资源类型→对象、技能前置标签与空内容插槽。当前浏览器检查先列，历史记录保留原验证版本；静态检查中的原平台历史快照差异如实登记，不重置基线。','checks':checks,'limitations':'本次未改原平台。原平台文件与最初扫描快照存在差异，详见静态报告；不能标记为快照未改变。资源输入仅使用提供给页面的目录，不包含真实资源检索、后端权限、模型、模板生成或课程绑定服务。生成内容的具体预览、编辑和业务流程由调用页面接入，容器不提供真实生成服务。实际输入法人工候选、跨浏览器撤销分组、全量状态、移动端和完整无障碍认证未验收。'}
(R/'data/validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(f"Static: {static['passed']} passed, {static['failed']} failed; browser evidence retains version labels.")
