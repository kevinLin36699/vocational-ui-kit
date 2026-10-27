#!/usr/bin/env python3
"""Static integrity and render-contract checks. Browser interaction is reported separately."""
from pathlib import Path
from html.parser import HTMLParser
import json, re, subprocess, tempfile, hashlib
R=Path(__file__).resolve().parents[1]; results=[]
def check(name,condition,detail=''):
    results.append({'name':name,'status':'passed' if condition else 'failed','evidence':detail})
for f in sorted((R/'js').glob('*.js')):
    p=subprocess.run(['node','--check',str(f)],capture_output=True,text=True);check('JS syntax '+f.name,p.returncode==0,p.stderr.strip())
catalog=json.loads((R/'data/components.json').read_text());tokens=json.loads((R/'data/tokens.json').read_text())
vm=r'''
const fs=require('fs'),vm=require('vm');
const context={window:{addEventListener(){}},document:{addEventListener(){},querySelectorAll(){return []}},console,setTimeout,clearTimeout,CustomEvent:class{},Map,WeakMap,WeakSet,Set,URL,Blob};context.window.window=context.window;
vm.createContext(context);
for(const file of ['icons.js','resource-composer.js','skill-picker.js','content-workspace.js','voc-ui.js','patterns.js'])vm.runInContext(fs.readFileSync(process.argv[1]+'/js/'+file,'utf8'),context,{filename:file});
const u=context.window.VocUI,p=context.window.VocPatterns;
const cases=[];for(const key of u.supportedComponents){cases.push({key,html:u.render(key)});for(const state of ['disabled','readonly','invalid','loading','failed','stopped'])cases.push({key:key+':'+state,html:u.render(key,{state})})}
const bad=u.render('input',{label:'<img src=x onerror=alert(1)>',value:'"><script>alert(1)</script>'});
const md=u.markdown('<img src=x onerror=alert(1)>\n```html\n<script>alert(1)</script>\n```');
const composerHtml=u.render('composer');const composerSafe=u.render('composer',{files:[{id:'x',name:'<script>alert(1)</script>'}]}).includes('<script>')===false;const composerEntry=composerHtml.includes('data-v-action="ai-add"')&&!composerHtml.includes('data-v-action="ai-upload"')&&!composerHtml.includes('data-v-action="ai-resources"');
const ws=u.render('workspace');const wsUnsafe=u.render('workspace',{title:'<script>alert(1)</script>'});
console.log(JSON.stringify({composerEntry,composerSafe,workspaceSlot:ws.includes('data-workspace-slot'),workspaceEmpty:!ws.includes('data-content-select')&&!ws.includes('data-workspace-action='),workspaceSafe:!wsUnsafe.includes('<script>'),keys:u.supportedComponents,patterns:p.list.map(x=>x.id),renders:cases,patternRenders:p.list.map(x=>({key:x.id,html:p.render(x.id)})),safe:!bad.includes('<img src=x')&&!bad.includes('<script>')&&!md.includes('<script>')&&!md.includes('<img src=x')}));
'''
p=subprocess.run(['node','-e',vm,str(R)],capture_output=True,text=True)
check('VM renderer execution',p.returncode==0,p.stderr[:500]);v=json.loads(p.stdout) if p.returncode==0 else {}
if v:
    check('60 catalog keys match runtime',set(v['keys'])==set(c['key'] for c in catalog),str(len(v['keys']))+' keys')
    check('All variants render without exception',len(v['renders'])==len(catalog)*7,str(len(v['renders']))+' render cases')
    check('14 page patterns render',len(v['patterns'])==14 and len(v['patternRenders'])==14)
    check('Untrusted input and Markdown escaped',v['safe'],'HTML and script payload escaped')
if v:
    check('Workspace is an empty extension slot',v['workspaceSlot'] and v['workspaceEmpty'],'No business editor, type catalog or default business action')
    check('Workspace metadata escaped',v['workspaceSafe'])
    check('Composer uses one add-content trigger',v['composerEntry'])
    check('File catalog text escaped',v['composerSafe'])
class Parser(HTMLParser):
    def __init__(self):super().__init__(convert_charrefs=True);self.refs=[];self.duplicates=[];self.ids=[];self.labels=[];self.actions=[]
    def handle_starttag(self,tag,attrs):
        keys=[k for k,val in attrs]
        if len(keys)!=len(set(keys)):self.duplicates.append((tag,keys))
        a=dict(attrs)
        if a.get('id'):self.ids.append(a['id'])
        if tag=='label' and a.get('for'):self.labels.append(a['for'])
        if tag in ['script','link','a','img']:
            x=a.get('src') if tag in ['script','img'] else a.get('href')
            if x:self.refs.append(x)
        if a.get('data-v-action'):self.actions.append(a['data-v-action'])
badrefs=[];badattrs=[];badlabels=[];badids=[]
for f in [R/'index.html',*sorted((R/'examples').glob('*.html'))]:
    h=Parser();h.feed(f.read_text());
    for ref in h.refs:
        if ref.startswith(('http:','https:','data:','#','mailto:')):continue
        target=(f.parent/ref.split('#')[0].split('?')[0]).resolve()
        if not target.exists():badrefs.append(str(f.relative_to(R))+':'+ref)
    if h.duplicates:badattrs.append([str(f),h.duplicates])
for item in v.get('renders',[])+v.get('patternRenders',[]):
    h=Parser();h.feed(item['html'])
    if h.duplicates:badattrs.append([item['key'],h.duplicates])
    if len(h.ids)!=len(set(h.ids)):badids.append(item['key'])
    if any(l not in h.ids for l in h.labels):badlabels.append(item['key'])
check('Local HTML resources resolve',not badrefs,json.dumps(badrefs,ensure_ascii=False))
check('No duplicate HTML attributes',not badattrs,json.dumps(badattrs[:5],ensure_ascii=False))
check('Renderer IDs unique within instances',not badids,str(badids[:5]))
check('Explicit labels resolve to controls',not badlabels,str(badlabels[:8]))
used=set();defined=set()
for f in (R/'css').glob('*.css'):
    s=f.read_text();used.update(re.findall(r'var\((--[\w-]+)',s));defined.update(re.findall(r'(--[\w-]+)\s*:',s))
check('CSS variable references defined',not (used-defined-{'--token-color'}),str(used-defined))
literal=[]
for f in [R/'css/components.css',R/'css/showcase.css']:
    if re.search(r'#[0-9a-fA-F]{3,8}\b|\brgba?\(|\boklch\(',f.read_text()):literal.append(f.name)
check('Component CSS colors only use tokens',not literal,str(literal))
manifest=json.loads((R/'data/source-manifest.json').read_text()); source=R.parents[1]/'3-原型设计/high-school-new'
changed=[f['path'] for f in manifest if hashlib.sha256((source/f['path']).read_text(errors='replace').encode()).hexdigest()!=f['sha256']]
check('Original scanned files unchanged',not changed,str(changed[:5]))
missing=[]
for c in catalog:
    for e in c['evidence']:
        f=source/e['file']
        if not f.exists() or e['line']>len(f.read_text(errors='replace').splitlines()):missing.append(c['id'])
check('Source evidence file/line exists',not missing,str(missing[:5]))
check('Migration records not falsely completed',all(not m['verifiedMigration'] for m in json.loads((R/'data/migration-map.json').read_text())))
check('No external runtime resource dependency',not any(re.search(r'<(?:script|link)[^>]+(?:src|href)=["\']https?://',f.read_text()) for f in [R/'index.html',*list((R/'examples').glob('*.html'))]))
def luminance(hex):
    vals=[int(hex[i:i+2],16)/255 for i in (1,3,5)]
    vals=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in vals]
    return sum(a*b for a,b in zip(vals,[.2126,.7152,.0722]))
ratios=[]
for fg,bg in [('foreground','card'),('secondary','card'),('muted-foreground','background'),('brand-foreground','brand'),('danger','danger-soft'),('success','success-soft'),('warning','warning-soft')]:
    a=luminance(tokens['tokens'][fg]['resolved']);b=luminance(tokens['tokens'][bg]['resolved']);ratio=(max(a,b)+.05)/(min(a,b)+.05);ratios.append(f'{fg}/{bg}={ratio:.2f}')
    check('Text contrast '+fg+'/'+bg,ratio>=4.5,f'{ratio:.2f}:1; text pair only, not full accessibility certification')
# AI accents must remain readable across the complete two-stop gradient.
start=tokens['tokens']['ai-start']['resolved'];end=tokens['tokens']['ai-end']['resolved']
white=luminance(tokens['tokens']['brand-foreground']['resolved']);ai_ratios=[]
for i in range(7):
    t=i/6
    color='#'+''.join(f"{round(int(start[j:j+2],16)*(1-t)+int(end[j:j+2],16)*t):02x}" for j in (1,3,5))
    lum=luminance(color);ai_ratios.append((max(white,lum)+.05)/(min(white,lum)+.05))
check('AI gradient white foreground contrast',min(ai_ratios)>=4.5,'7 samples, minimum '+f'{min(ai_ratios):.2f}:1')
a=luminance(tokens['tokens']['ai-ink']['resolved']);b=luminance(tokens['tokens']['ai-soft']['resolved']);ratio=(max(a,b)+.05)/(min(a,b)+.05)
check('AI soft label contrast',ratio>=4.5,f'{ratio:.2f}:1')
a=luminance(tokens['tokens']['ai-border-focus']['resolved']);b=luminance(tokens['tokens']['card']['resolved']);ratio=(max(a,b)+.05)/(min(a,b)+.05)
check('AI focus border contrast against white',ratio>=3,f'{ratio:.2f}:1')
meta=json.loads((R/'data/library.json').read_text())
check('Manifest token count/version match',meta['tokens']==len(tokens['tokens']) and meta['version']==tokens['version'])
alignment=json.loads((R/'data/component-alignment.json').read_text())
check('Every component has reviewed reference mapping',alignment['version']==meta['version'] and {c['key'] for c in alignment['components']}=={c['key'] for c in catalog} and all(c.get('reference') and c.get('kind') in ('document-rule','common-primitives-composition') for c in alignment['components']),'60 records; document rule vs shared-primitives composition explicitly distinguished')
check('Current component metadata matches library version',all(c['version']==meta['version'] and c.get('alignment',{}).get('standardVersion')==meta['version'] for c in catalog))
# Binding rules from the actual DESIGN.md, checked independently of implementation selectors.
expected={'control':'36px','control-sm':'30px','radius-control':'10px','radius-card':'14px','radius-dialog':'20px','sidebar-width':'272px','sidebar-collapsed':'64px','header-height':'56px','conversation-max':'46rem','panel-width':'360px','font-prose':'15px'}
check('Reference geometry and typography token contract',all(tokens['tokens'][k]['resolved']==v for k,v in expected.items()),'DESIGN.md sections 4,5,6,10,11; user theme overrides kept separate')
out=R/'data/static-validation.json';out.write_text(json.dumps({'checks':results,'passed':sum(x['status']=='passed' for x in results),'failed':sum(x['status']=='failed' for x in results)},ensure_ascii=False,indent=2)+'\n')
for r in results:print(r['status'].upper(),r['name'],r['evidence'][:140])
raise SystemExit(1 if any(x['status']=='failed' for x in results) else 0)
