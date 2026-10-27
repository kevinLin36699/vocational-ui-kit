#!/usr/bin/env python3
"""Rebuild the traceable catalog from the retained source, without changing it."""
from pathlib import Path
from collections import Counter, defaultdict
import json, re, hashlib, csv

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parents[1] / '3-原型设计/high-school-new'
REFERENCE = ROOT.parents[1] / '1-参考资料/DESIGN.md'
VERSION = '2.0.0'
PARAMS={
 'input':dict(label='文本标签',value='初始值',state='disabled/readonly/invalid',disabled='布尔',readonly='布尔',type='HTML input类型',name='字段名',required='布尔',placeholder='占位',min='数值下限',max='数值上限',help='说明文字'),
 'textarea':dict(label='文本标签',value='初始正文',disabled='布尔',state='disabled'),
 'button':dict(label='统一覆盖示例按钮文字',disabled='布尔',state='disabled'),
 'select':dict(label='字段标签',disabled='布尔',state='disabled'),
 'table':dict(state='default/empty/no-match/loading/failed；数据固定为示例集合'),
 'form':dict(value='初始课程名'),
 'process':dict(state='waiting/running/completed/failed/stopped'),
 'composer':dict(files='当前可见我的文件目录，空数组为空',value='初始草稿',placeholder='占位文字',disabled='布尔',id='可选唯一ID',resources='资源目录，见INLINE_RESOURCES.md',resourceTypes='当前可用资源类型',skills='当前可用技能目录',selectedSkill='初始技能ID或记录',segments='正文与资源ID片段数组'),
 'workspace':{'title': '容器标题', 'subtitle': '可选副标题', 'state': 'empty/loading/ready/error', 'statusText': '可选状态文案', 'actions': '可选操作元数据，默认无业务操作'},
 'result':{},
 'chat':dict(files='当前可见我的文件目录',history='false隐藏会话栏',mode='success/failure本地模拟',resources='当前可见资源目录',resourceTypes='当前可用资源类型',skills='当前可用技能目录',selectedSkill='初始技能ID或记录')
}

# id, name, group, source indicators, rule, description, applicability
SPECS = [
('button','按钮','基础','mg-btn|prep-button|upload-button','CMP01/02/06','一个操作区域一个主操作；实体删除及确认统一危险红色，错误反馈保持红色。','default hover active focus disabled loading'),
('icon','图标与图标按钮','基础','ui-icon|UIIcons','CMP08～13','复用现有 24×24 描边图标，操作名称与图形语义一致。','default hover focus disabled'),
('link','链接','基础','bc-link|href=','NAV10/TXT06','导航使用链接，页面行为使用按钮；外部去向明确。','default hover focus'),
('tag','标签与可移除项','基础','resource-chip|ai-selected-skill|type-tag','TXT04/WID07','分类只读，移除只影响当前选择，不删除源对象。','default focus selected disabled'),
('badge','状态徽标','基础','mg-status|badge|status-tag','CMP07/TXT04','状态文字与语义色同时表达，未知值不伪装成功。','neutral info success warning danger'),
('avatar','头像','基础','avatar|profile','TXT05','个人和账号使用中性头像；AI 回答使用28px方圆印章、名称与可选时间元信息。','default fallback'),
('separator','分割线','基础','separator|divider','TXT06','用留白和细线组织内容，避免层层卡片。','horizontal vertical'),
('input','文本输入','录入','mg-field|login-field|input','WID01/FORM','36px控件、10px圆角、14/20px文字；标签13/18px，焦点光晕，错误与说明关联。','default hover focus disabled readonly invalid'),
('textarea','多行输入','录入','textarea|mg-field','WID02','正文自然换行，长内容滚动，不静默截断。','default focus disabled readonly invalid'),
('number','数字与单位','录入','type="number"|学时|分值','WID03','空值与 0 分离，保留业务范围与精度，不擅自取整。','default focus invalid disabled'),
('select','下拉选择','录入','select|mg-filters','WID06','可搜索的自定义选择器，支持方向键、Enter、Escape；全部只用于筛选。','default open selected disabled empty'),
('checkbox','复选框','录入','type="checkbox"|checkbox','WID05','多选不改变正式数据；全选区分部分与全部。','unchecked checked mixed disabled'),
('radio','单选组','录入','type="radio"|login-roles','WID05','互斥选择，不擅自预选评分与业务对象。','unchecked checked focus disabled'),
('switch','开关','录入','switch|toggle','WID08','表单内开关只改草稿，正式生效由保存动作决定。','off on focus disabled'),
('date','日期与范围','录入','type="date"|截止|datetime','WID04','用原生日期控件保证可用性，范围跨字段校验；时区 Asia/Shanghai。','default focus invalid disabled'),
('multiselect','多选标签','录入','selected-skill|multi-select|selectedTags','WID07','显示完整选择，可移除；变更只影响本次草稿。','empty selected open disabled'),
('cascade','院系专业级联','录入','majorName|categoryName|department','WID07/FORM11','保留院系专业业务，变更上级时清除失效专业。','empty selected dependent invalid'),
('upload','文件上传','录入','type="file"|pending-list|file-input','FILE/WID02','选择、校验、移除、失败和重选可演示；不声称已上传服务器或解析。','empty selected invalid removed'),
('form','分区表单与校验','录入','mg-field|loginForm|form','FORM/CON','校验失败保留输入并定位首错，提交防重；取消有未保存保护。','default dirty invalid submitting success'),
('search','搜索','录入','mg-home-search|data-tcc-search|search','LIST01/WID01','搜索范围与生效时点明确，输入法组词不触发误提交。','default composing searching empty'),
('table','数据表格','展示','mg-table|table|thead','TBL01～08','筛选排序后分页，页内全选三态，操作不冒泡，导出有真实文件。','default loading empty no-match failed selected sorted'),
('pagination','分页','展示','pagination|data-page|mg-page','LIST/TBL','总数、当前页与有效结果同步，不把页码当装饰。','default first last disabled'),
('card','内容卡片','展示','mg-card|program-course-card|resource-card','CMP04/05','卡片用于独立对象，内容可读，入口和次级动作分离。','default hover focus selected'),
('description','描述列表','展示','detail|description|简介','TXT/CON02','标签与内容成组，空值明确，长正文完整换行。','default empty long'),
('tree','树与目录','展示','tree|course-directory|unit-list','WID11/EDU02','箭头展开、名称选择分别表达，支持层级和键盘。','collapsed expanded selected'),
('steps','步骤条','展示','steps|wizard|step-bar','WID12/AIC14','步骤反映已完成的阶段，允许返回时保留输入。','pending active completed'),
('progress','进度','展示','progress|进度','VIS04','百分比根据分子分母计算；未知总量采用阶段状态。','determinate indeterminate completed'),
('timeline','时间线与审批记录','展示','timeline|审核|审批','DATA/OPS','记录对象、动作和时间，不因展示演示而声称真实审批。','default long empty'),
('stat','指标卡','展示','stat|metric|统计','VIS01/DATA02','标明范围与单位，0 与未知分别显示。','default zero missing'),
('chart','统计图与明细','展示','chart|radar|dashboard','VIS01～06','图形和明细共享数据，带可读摘要，图例支持键盘切换。','default filtered empty'),
('empty','空状态','展示','empty|暂无|没有匹配','TBL07/STATE','无数据与无匹配区分，提供有效下一步。','empty no-match'),
('skeleton','骨架与加载','展示','skeleton|loading','STATE','模拟真实结构，只在真实等待时使用；可结束。','loading completed'),
('shell','应用外壳与导航','导航布局','sidebar|topbar|nav-item','NAV/LAY','侧栏、头部、正文独立，导航收放不重置业务状态。','expanded collapsed active'),
('breadcrumb','面包屑','导航布局','bcMarkup|breadcrumb|bc-link','NAV07/WID12','父级可返回，当前项为文字，不制造空跳转。','default long'),
('tabs','内容标签页','导航布局','mg-tabs|tabs|aria-selected','LAY03','分段底轨、30px页签与白色滑块；支持方向键，面板状态独立。','default active focus overflow'),
('segmented','分段控件','导航布局','login-roles|role-options','DESIGN 10.6','用于互斥视图模式，不能代替内容导航或表单提交。','default active focus'),
('toolbar','筛选与操作栏','导航布局','mg-filters|toolbar|filters','TPL02/LIST','标题、筛选、表格同轴；关键词和字段共享有效集合。','default filtered reset'),
('menu','更多菜单','反馈浮层','ai-more-tools|account-menu|history-actions','OVR/WID09','纯动作菜单与带输入的选择浮层分开，Escape 和外部点击关闭。','closed open focus disabled'),
('popover','选择浮层','反馈浮层','popover|ai-more-menu','OVR/WID10','带输入的小浮层靠近触发器，视口边缘避让。','closed open empty'),
('tooltip','悬停与焦点提示','反馈浮层','title=|tooltip','WID10/ACC','鼠标和键盘可读；重要错误不藏在悬停提示里。','hover focus closed'),
('dialog','弹窗','反馈浮层','modal|dialog|mg-modal','OVR01～10','有标题、焦点管理、滚动和关闭；取消不改变数据。','closed open scrolling'),
('confirm','危险操作确认','反馈浮层','delete-confirm|confirm|data-action="delete"','CMP06/OVR','说明对象和后果；默认聚焦取消，遮罩不提交。','closed open cancelled confirmed'),
('drawer','抽屉','反馈浮层','drawer|side-panel','OVR/LAY12','局部详情与上下文保留，关闭后焦点返回入口。','closed open scrolling'),
('alert','就地反馈与错误','反馈浮层','notice|alert|error','SYS01/09','错误就地说明原因与恢复动作，不用 Toast 掩盖。','info success warning danger'),
('toast','轻提示','反馈浮层','toast','SYS01/DESIGN10.16','提供可选能力，正式平台普通成功优先就地更新。','shown dismissed'),
('course-card','课程卡片','高职教业务','program-course-card|course-card|tcc','EDU/TXT05','16:9 封面、两行名称，必修选修属性；课程不绑定学期或混入实训。','default hover focus'),
('person-picker','人员选择','高职教业务','teacherId|studentId|person|人员','FORM11/DATA','通过稳定 ID 选择人员，同名不混淆；演示数据为虚构。','empty selected searched'),
('approval','审核与分发','高职教业务','审核|分发|审批','OPS/AIC12','保留审核、生成、保存和分发的语义边界，不扩大为群发或发布。','draft reviewing approved distributed'),
('resource','资源与版本','高职教业务','resource-summary|mg-resource|fileName','FILE/TRN','展示文件名、格式、版本、读取边界，下载真实示例文件。','default versioned downloaded'),
('task-guide','AI 任务引导','AI交互','teacher-task-guide|task-guide|CHAT15','CHAT15','顶部轻量说明、对象上下文和可编辑预填，明确发送后开始。','prepared edited submitted'),
('agent','智能体入口','AI交互','agent|智能体|skills','DESIGN11.11','名称、用途和可用状态清晰；选择只准备任务，不自动发送。','available unavailable selected'),
('conversation','会话列表','AI交互','history-actions|history-heading|协作记录','HIST01～10','本地新建、搜索、重命名、置顶与删除确认；草稿按会话隔离。','empty selected renamed pinned'),
('composer','AI 输入区','AI交互','data-ai-composer|AIComposer|composer','AIC05/16','单层输入面板，支持 / 资源选择、正文内可替换片段及输入法。','empty draft attached running disabled'),
('message','用户与 AI 消息','AI交互','message-bubble|message.assistant|message-avatar','AIC02/03','用户浅蓝气泡，AI 开放正文无重复头像；操作和正文分层。','user assistant completed'),
('prose','Markdown 与代码','AI交互','mgMarkdown|markdown|chat-prose','DESIGN 附录C/AIC02','受控 Markdown 子集，先转义再格式化；宽代码和表格局部滚动。','paragraph list code table'),
('process','处理过程','AI交互','AIProcessUI|ai-process-card|ai-process-steps','AIC06/15','运行中保持展开；完成、停止、失败分别表达，允许查看工具结果。','waiting running completed stopped failed'),
('citation','引用与来源','AI交互','evidence|citation|来源','DESIGN11.7/DATA01','引用可通过点击和键盘打开，演示来源注明性质，不伪造已核验。','default preview open'),
('result','生成内容摘要','AI交互','生成内容|artifact|result-card','AIC07','名称、用途、实际状态和查看入口，不把生成等同已保存或已分发。','generated viewed saved'),
('workspace','生成内容工作区','AI交互','workspace|outline|draft','AIC08/12','仅提供标题、收放、滚动、状态与可选操作栏，内容通过业务插槽接入。','empty loading ready error collapsed'),
('chat','AI 协作组合','AI交互','teacher-main-conversation|studentChatForm|chatForm','AI/CHAT/AIC','本地会话与流式模拟，发送、停止、失败、重试、来源和工作区贯通。','idle running stopped failed completed'),
]

for key in ['composer','chat','conversation']:
    PARAMS.setdefault(key,{}).update(agentOptions='当前业务可用关联Agent目录，[]隐藏整组；见TEACHING_AGENTS.md',selectedAgents='初始选中的关联id数组，默认空')

def dump(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')

def main():
    files=[]; texts={}; occurrences=defaultdict(list); colors=Counter(); radii=Counter(); important=0
    for f in sorted(SOURCE.rglob('*')):
        if not f.is_file() or '.git' in f.parts: continue
        if f.suffix not in {'.html','.js','.css','.md','.json'}: continue
        if 'vendor' in f.parts: continue
        s=f.read_text(errors='replace'); rel=f.relative_to(SOURCE).as_posix(); texts[rel]=s
        files.append(dict(path=rel,lines=len(s.splitlines()),bytes=f.stat().st_size,sha256=hashlib.sha256(s.encode()).hexdigest(),scope='asset' if 'assets' in f.parts else 'design' if f.suffix=='.md' else 'source'))
        if f.suffix in {'.css','.html','.js'}:
            for i,line in enumerate(s.splitlines(),1):
                # Lexical scan only: retains exact file/line, does not claim a full CSS/JS AST.
                found=set(re.findall(r'\.([a-zA-Z_][\w-]*)',line)) if f.suffix=='.css' else set()
                for match in re.finditer(r'class\s*=\s*[\"\']([^\"\']+)[\"\']',line):
                    found.update(c for c in match[1].split() if re.fullmatch(r'[a-zA-Z_][\w-]*',c))
                for c in found: occurrences[c].append({'file':rel,'line':i})
            if f.suffix=='.css':
                colors.update(re.findall(r'#[0-9a-fA-F]{3,8}\b',s)); radii.update(x.strip() for x in re.findall(r'border-radius\s*:\s*([^;}]+)',s)); important+=s.count('!important')
    catalog=[]
    for ident,name,group,pattern,rule,desc,states in SPECS:
        rx=re.compile(pattern,re.I); evidence=[]; matches=0
        for rel,s in texts.items():
            if rel.endswith('.md') or rel.startswith('assets/'): continue
            for i,line in enumerate(s.splitlines(),1):
                m=rx.search(line)
                if m:
                    matches+=1
                    if len(evidence)<8 and (not evidence or evidence[-1]['file']!=rel or len(evidence)<3):
                        a=max(0,m.start()-35); b=min(len(line),m.end()+80)
                        evidence.append({'file':rel,'line':i,'excerpt':line[a:b]})
        catalog.append(dict(id='voc-'+ident,key=ident,name=name,category=group,description=desc,version=VERSION,rule=rule,
            evidence=evidence,evidenceMatches=matches,evidenceType='local-code' if evidence else 'proposed-extension',
            states=states.split(),statePolicy='仅列适用状态；组合组件通过实际交互触发，非全部状态均有独立切换。',
            implementation='implemented',maturity='HTML 原型组件，非生产框架包',
            api={'render':f'VocUI.render("{ident}", props)', 'mount':f'VocUI.mount(element, "{ident}", props)', 'parameters':PARAMS.get(ident,{}),'parameterPolicy':'本表以外是固定示例配方，不假定具有完整业务配置API。','events':['voc:change','voc:submit','voc:action'], 'eventContract':'仅已实现的相关操作产生冒泡 CustomEvent；静态组件不自动产生所有事件，详见 design/API.md'},
            usage={'recommended':desc,'avoid':'不要复制另一套样式或绕过当前业务的权限、草稿与状态控制。'},
            sourcePattern=pattern,extensions=['select 为兼容无依赖项目提供原生 JS 搜索选择；日期使用浏览器原生控件。'] if ident in ['select','date'] else []))
    # Preserve reviewed conformance metadata when explicitly re-scanning sources.
    alignment_file=ROOT/'data/component-alignment.json'
    if alignment_file.exists():
        reviewed={x['key']:x for x in json.loads(alignment_file.read_text()).get('components',[])}
        for c in catalog:
            if c['key'] in reviewed:
                x=reviewed[c['key']];c['description']=x['implementation'];c['usage']['recommended']=x['implementation']
                c['alignment']={'reference':x['reference'],'kind':x['kind'],'standardVersion':VERSION,'implementation':'HTML/CSS/JS adapter; not the reference React/Radix package'}
    for c in catalog:
        if c['key']=='composer':
            contract=json.loads((ROOT/'data/composer-resources.json').read_text())
            c['api']['events']=list(dict.fromkeys(c['api']['events']+contract['events']))
            c['states']+=['resource-open','resource-no-match','resource-selected','resource-unavailable']
            c['extensions'].append({'source':'用户2026-10-26截图与明确要求','scope':'通用 / 资源唤起、稳定ID序列化、内联片段与课程单元联动','standard':contract['standard']})
    for c in catalog:
        if c['key'] in ['composer','chat']:c['api']['events'].append('voc:skill-change')
        if c['key'] in ['message','chat']:c['api']['events'].append('voc:feedback')
        if c['key']=='workspace':c['api']['events'].append('voc:workspace-action')
        if c['key']=='chat':c['api']['events'].append('voc:workspace-open')
    mapping=[]; family=defaultdict(lambda: {'count':0,'examples':[]})
    classify=[(re.compile(p,re.I),'voc-'+k) for k,n,g,p,r,d,st in SPECS]
    for cls,locs in sorted(occurrences.items()):
        # Exact class-like indicators first; broad words only mark candidates for review.
        targets=[cid for rx,cid in classify if rx.search(cls)]
        specialized=bool(re.search(r'(ppt|video|canvas|graph|exam|quiz|mind|player|monaco|draw)',cls,re.I))
        status='specialized-preserve' if specialized else 'candidate-mapped' if targets else 'review-required'
        mapping.append(dict(selector='.'+cls,candidateComponents=targets[:4],decision=status,
            reason='保留画布、媒体、考试或编辑器业务实现，仅统一外壳' if specialized else '词法候选，实施时核对实际结构、事件与角色规则' if targets else '专用样式或动态类，需逐页人工判断，不自动全局替换',
            occurrences=locs,priority='P2' if specialized else 'P1',verifiedMigration=False))
        prefix=cls.split('-')[0]; family[prefix]['count']+=1
        if len(family[prefix]['examples'])<4:family[prefix]['examples'].append('.'+cls)
    report=dict(version=VERSION,sourceRoot=str(SOURCE),referenceDocument=str(REFERENCE),scanMethod='Python 词法扫描；不解析完整 JS/CSS AST，不等同逐页运行验收',
        fileCount=len(files),sourceCount=sum(f['scope']=='source' for f in files),classCount=len(mapping),importantCount=important,
        colors=colors.most_common(45),radii=radii.most_common(30),families=sorted([dict(prefix=k,**v) for k,v in family.items()],key=lambda x:-x['count']),
        mappingSummary=dict(Counter(m['decision'] for m in mapping)),files=files)
    for name,obj in [('components.json',catalog),('source-audit.json',report),('migration-map.json',mapping)]:dump(ROOT/'data'/name,obj)
    with (ROOT/'data/migration-map.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['旧选择器','候选组件','处置','优先级','来源示例','是否已迁移'])
        for m in mapping:w.writerow([m['selector'],' / '.join(m['candidateComponents']),m['decision'],m['priority'],'; '.join(f"{p['file']}:{p['line']}" for p in m['occurrences'][:5]),'否'])
    dump(ROOT/'data/source-manifest.json',files)
    (ROOT/'js/catalog.js').write_text('/* Generated by scripts/build_catalog.py; source evidence, no runtime fetch. */\nwindow.VocCatalog='+json.dumps(catalog,ensure_ascii=False)+';\nwindow.VocAudit='+json.dumps({k:v for k,v in report.items() if k!='files'},ensure_ascii=False)+';\nwindow.VocMigration='+json.dumps([{**m,'occurrences':m['occurrences'][:3]} for m in mapping],ensure_ascii=False)+';\n')
    print(json.dumps({k:report[k] for k in ['fileCount','sourceCount','classCount','importantCount','mappingSummary']},ensure_ascii=False));print('components',len(catalog))

if __name__=='__main__':main()
