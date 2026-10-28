#!/usr/bin/env python3
from pathlib import Path
import json, re
R=Path(__file__).resolve().parents[1]
values={
'blue-50':'#eff6ff','blue-100':'#dbeafe','blue-200':'#bfdbfe','blue-300':'#93c5fd','blue-400':'#60a5fa','blue-500':'#3b82f6','blue-600':'#2563eb','blue-700':'#155cc3','blue-800':'#0b3a9b','blue-900':'#15356c',
'brand':'{blue-700}','brand-hover':'{blue-800}','brand-soft':'#eaf2ff','brand-foreground':'#ffffff','background':'#f5f7fb','card':'#ffffff','sidebar':'#f8faff','foreground':'#20344f','secondary':'#52657e','muted-foreground':'#5e7088','muted':'#eef2f7','border':'#dce5f0','input-border':'#b8c9df','border-hover':'#a4bbd9','ring':'#1769d1','success':'#23734f','success-soft':'#e9f5ef','warning':'#8b5c12','warning-soft':'#fff4db','danger':'#b52e3b','danger-soft':'#fff0f2','info':'{brand}','info-soft':'{brand-soft}','bubble-user':'#eaf2ff','code-bg':'#f0f4f9','trace-line':'#d3deec','overlay':'rgb(20 37 65 / 0.32)','ink-inverse':'#ffffff','accent-violet':'#6954b8','accent-violet-soft':'#f1edfc','transparent':'transparent',
'font-sans':'"PingFang SC","Hiragino Sans GB","Noto Sans SC","Microsoft YaHei",system-ui,sans-serif','font-mono':'ui-monospace,"SF Mono","Cascadia Mono",Menlo,Consolas,monospace',
'font-caption':'12px','font-small':'13px','font-body':'14px','font-prose':'15px','font-section':'17px','font-page':'28px','font-display':'32px','leading-body':'1.5','leading-title':'1.285714',
'space-1':'4px','space-2':'8px','space-3':'12px','space-4':'16px','space-5':'20px','space-6':'24px','space-7':'28px','space-8':'32px','space-10':'40px','space-ai':'18px',
'control-sm':'30px','control':'36px','control-lg':'44px','icon-size':'18px','radius-sm':'6px','radius-control':'10px','radius-card':'14px','radius-dialog':'20px','radius-full':'999px','sidebar-width':'272px','panel-width':'360px','page-max':'1040px','conversation-max':'46rem','reading-max':'46rem','header-height':'56px','z-sticky':'10','z-popover':'50','z-dialog':'50','z-toast':'50','duration-fast':'120ms','duration-base':'200ms','duration-slow':'320ms','ease-out':'cubic-bezier(.2,.8,.2,1)','shadow-sm':'0 1px 2px rgb(24 39 62 / .04)','shadow-pop':'0 8px 28px rgb(24 39 62 / .10),0 2px 6px rgb(24 39 62 / .04)','shadow-dialog':'{shadow-pop}'}
values.update({'font-serif':'"Songti SC","STSong","Noto Serif SC","Source Han Serif SC","Noto Serif CJK SC",serif','sidebar-collapsed':'64px','control-nav':'34px','control-chip':'28px','badge-height':'22px','radius-stage':'24px','radius-nav':'9px','radius-message-action':'8px','space-half':'2px','space-compact':'6px','space-field':'10px','space-turn':'30px','space-section':'34px','home-max':'800px','welcome-max':'720px','focus-shadow':'0 0 0 3px var(--v-brand-soft)','danger-focus-shadow':'0 0 0 3px var(--v-danger-soft)','duration-exit':'180ms','ease-spring':'cubic-bezier(.22,1,.36,1)'})
values.update({'radius-composer':'18px','composer-send-size':'34px','radius-send':'11px'})
values.update({'ai-start': '{brand}', 'ai-end': '{accent-violet}', 'ai-ink': '#54429d', 'ai-soft': '{accent-violet-soft}', 'ai-border': '#d5d1ed', 'ai-border-focus': '#8175cb', 'ai-gradient': 'linear-gradient(135deg, var(--v-ai-start), var(--v-ai-end))', 'ai-surface': 'linear-gradient(115deg, var(--v-brand-soft), var(--v-ai-soft))', 'ai-outline': 'linear-gradient(115deg, var(--v-border-hover), var(--v-ai-border))', 'ai-outline-focus': 'linear-gradient(115deg, var(--v-brand), var(--v-ai-end))', 'ai-focus-shadow': '0 0 0 3px rgb(105 84 184 / .12)', 'ai-action-shadow': '0 3px 10px rgb(71 72 165 / .18)'})
aliases={'ui-primary':'brand','ui-primary-hover':'brand-hover','ui-primary-soft':'brand-soft','ui-canvas':'background','ui-surface':'card','ui-ink':'foreground','ui-secondary':'secondary','ui-muted':'muted-foreground','ui-border':'border','ui-border-hover':'border-hover','ui-focus':'ring','ui-font':'font-sans','ui-radius':'radius-card','ui-radius-control':'radius-control','ui-radius-dialog':'radius-dialog','ui-control-sm':'control-sm','ui-control-md':'control','ui-control-lg':'control-lg','ui-page-title-size':'font-page','ui-page-max':'page-max','ui-motion':'duration-base'}
tokens={'version':'2.7.1','theme':'vocational-blue-white','colorMode':'light','tokens':{},'aliases':aliases}
def resolve(v):
    if v.startswith('{'):return resolve(values[v[1:-1]])
    return re.sub(r'var\(--v-([\w-]+)\)',lambda m:resolve(values[m[1]]),v)
for k,v in values.items():tokens['tokens'][k]={'value':v,'resolved':resolve(v),'cssVariable':'--v-'+k,'type':'gradient' if v.startswith('linear-gradient') else 'color' if resolve(v).startswith(('#','rgb')) else 'dimension' if v.endswith(('px','rem')) else 'string'}
(R/'data/tokens.json').write_text(json.dumps(tokens,ensure_ascii=False,indent=2)+'\n')
css='/* Vocational UI 2.5.0 · generated from data/tokens.json by build_tokens.py */\n:root {\n'
for k,v in values.items():css+=f'  --v-{k}: '+('var(--v-'+v[1:-1]+')' if v.startswith('{') else v)+';\n'
for k,v in aliases.items():css+=f'  --{k}: var(--v-{v});\n'
css+='}\n@media (prefers-reduced-motion: reduce) { :root { --v-duration-fast:0ms; --v-duration-base:0ms; --v-duration-slow:0ms; } }\n'
(R/'css/tokens.css').write_text(css)
(R/'js/tokens.js').write_text('window.VocTokens='+json.dumps(tokens,ensure_ascii=False)+';\n')
print('Generated',len(values),'tokens and',len(aliases),'migration aliases')
