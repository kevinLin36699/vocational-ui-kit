/* Calendar periods and local wall-clock values. No implicit timestamp/timezone conversion. */
(() => {
'use strict';
const U=window.VocUI,E=U.escape,I=U.icon,M=window.VocControls.dateMath;
const states=new WeakMap(); let serial=0,active=null;
const pad=n=>String(n).padStart(2,'0');
const today=()=>new Intl.DateTimeFormat('sv-SE',{timeZone:'Asia/Shanghai',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date());
const disabled=p=>p.disabled||p.state==='disabled', readonly=p=>p.readonly||p.state==='readonly';
const ids=()=>`vt-${++serial}`;
const specs={
 'date-picker':['date',false,'单日期'], 'date-range':['date',true,'日期范围'],
 'time-picker':['time',false,'时间'], 'time-range':['time',true,'时间范围'],
 'datetime-picker':['datetime',false,'日期时间'], 'datetime-range':['datetime',true,'日期时间范围'],
 'month-picker':['month',false,'月份'], 'month-range':['month',true,'月份范围'],
 'year-picker':['year',false,'年份'], 'year-range':['year',true,'年份范围'],
 'quarter-picker':['quarter',false,'季度'], 'week-picker':['week',false,'周'],
 'multi-date':['multiple',false,'多个日期']
};
function utc(v){const d=new Date(0); d.setUTCFullYear(Number(v.slice(0,4)),Number(v.slice(5,7))-1,Number(v.slice(8,10)));d.setUTCHours(12,0,0,0);return d}
function weekOf(v){const d=utc(v),day=d.getUTCDay()||7;d.setUTCDate(d.getUTCDate()+4-day);const y=d.getUTCFullYear(),first=utc(`${String(y).padStart(4,'0')}-01-01`);return `${String(y).padStart(4,'0')}-W${pad(Math.ceil(((d-first)/86400000+1)/7))}`}
function weekStart(v){const y=Number(v.slice(0,4)),w=Number(v.slice(6));if(!y||w<1||w>53)return null;const jan=`${String(y).padStart(4,'0')}-01-04`,day=utc(jan).getUTCDay()||7;const start=M.addDays(jan,1-day+(w-1)*7);return weekOf(start)===v?start:null}
function valid(v,type,seconds=false){
 if(typeof v!=='string')return false;
 if(type==='date'||type==='multiple')return M.validDate(v);
 if(type==='time')return (seconds?/^([01]\d|2[0-3]):[0-5]\d:[0-5]\d$/:/^([01]\d|2[0-3]):[0-5]\d$/).test(v);
 if(type==='datetime'){const a=v.split(' ');return a.length===2&&M.validDate(a[0])&&valid(a[1],'time',seconds)}
 if(type==='year')return /^\d{4}$/.test(v)&&Number(v)>0;
 if(type==='month')return /^\d{4}-(0[1-9]|1[0-2])$/.test(v)&&Number(v.slice(0,4))>0;
 if(type==='quarter')return /^\d{4}-Q[1-4]$/.test(v)&&Number(v.slice(0,4))>0;
 return type==='week'&&/^\d{4}-W\d{2}$/.test(v)&&!!weekStart(v);
}
function dateBounds(v,type){
 if(type==='year')return [v+'-01-01',v+'-12-31'];
 if(type==='quarter'){const m=(Number(v.slice(-1))-1)*3+1;return [v.slice(0,4)+'-'+pad(m)+'-01',M.addDays(M.shiftMonth(v.slice(0,4)+'-'+pad(m)+'-01',3),-1)]}
 if(type==='month')return [v+'-01',M.addDays(M.shiftMonth(v+'-01',1),-1)];
 if(type==='week'){const a=weekStart(v);return [a,M.addDays(a,6)]}
 return [v.slice(0,10),v.slice(0,10)];
}
function allowed(v,p,type){
 if(!valid(v,type,p.seconds))return false;
 if((p.min&&v<p.min)||(p.max&&v>p.max)||(p.disabledValues||[]).includes(v))return false;
 if(type!=='time'){const [a,b]=dateBounds(v,type);if((p.disabledDates||[]).some(d=>d>=a&&d<=b))return false}
 return true;
}
function normalize(p,type,range){
 const v=p.value;
 if(type==='multiple')return Array.isArray(v)?[...new Set(v)].filter(d=>allowed(d,p,type)).sort():[];
 if(range){if(!Array.isArray(v)||v.length!==2||!v.every(x=>allowed(x,p,type))||v[0]>v[1])return null;const dates=p.disabledDates||[];if(type!=='time'&&dates.some(d=>d>=dateBounds(v[0],type)[0]&&d<=dateBounds(v[1],type)[1]))return null;return [...v]}
 return allowed(v,p,type)?v:null;
}
const fmt=(v,type)=>!v?'':type==='year'?v+' 年':type==='month'?v.replace('-',' 年 ')+' 月':type==='quarter'?v.replace('-Q',' 年 第 ')+' 季度':type==='week'?v.replace('-W',' 年 第 ')+' 周':v.replaceAll('-','/');
function render(key,p={}){
 const [type,range,label]=specs[key],id=ids(),v=normalize(p,type,range),parts=range?v||['','']:[v||''];
 const hints={date:'YYYY-MM-DD',time:p.seconds?'HH:mm:ss':'HH:mm',datetime:p.seconds?'YYYY-MM-DD HH:mm:ss':'YYYY-MM-DD HH:mm',month:'YYYY-MM',year:'YYYY',quarter:'YYYY-Q1',week:'YYYY-W01',multiple:'选择多个日期'};
 return `<div class="vt-control" data-vt="${key}" data-vt-props="${E(JSON.stringify(p))}"><label class="v-field-label" for="${id}">${E(p.label||label)}${p.required?'<span class="v-required">*</span>':''}</label><div class="vt-field" data-range="${range}" data-kind="${type}" data-disabled="${!!disabled(p)}" data-readonly="${!!readonly(p)}" aria-invalid="${p.state==='invalid'}"><button type="button" class="vt-icon" data-vt-open aria-label="打开${E(p.label||label)}选择面板" aria-haspopup="dialog" aria-expanded="false" ${disabled(p)||readonly(p)?'disabled':''}>${I(type==='time'?'clock':'calendar',16)}</button>${type==='multiple'?'<div data-vt-tags class="vt-tags"></div>':''}${parts.map((x,i)=>`${i?'<span class="vt-separator">—</span>':''}<input id="${i?id+'-end':id}" data-vt-part="${i}" aria-label="${E((range?(i?'结束':'开始'):'')+(p.label||label))}" placeholder="${E(range?(i?'结束':'开始'):hints[type])}" value="${E(type==='multiple'?(v.length?v.length+' 个日期':''):fmt(x,type))}" ${disabled(p)?'disabled':''} ${readonly(p)||type==='multiple'?'readonly':''} autocomplete="off" ${['time','year'].includes(type)?'inputmode="numeric"':''}>`).join('')}<button type="button" class="vt-clear" data-vt-clear aria-label="清空${E(p.label||label)}" ${!v||type==='multiple'&&!v.length||disabled(p)||readonly(p)?'hidden':''}>${I('close',14)}</button></div>${type!=='multiple'?'<div data-vt-tags class="vt-tags"></div>':''}${parts.map((x,i)=>`<input type="hidden" ${disabled(p)?'disabled':''} name="${E(i?(p.endName||'end'):(p.name||key))}" value="${E(type==='multiple'?JSON.stringify(v):x)}">`).join('')}<p class="v-error" data-vt-error role="status">${p.state==='invalid'?'请选择有效的'+E(p.label||label):''}</p>${p.help?`<p class="v-caption">${E(p.help)}</p>`:''}</div>`;
}
function report(s,message=''){s.root.querySelector('[data-vt-error]').textContent=message;s.root.querySelector('.vt-field').setAttribute('aria-invalid',String(!!message))}
function update(s){
 const {root,type,range,p,value:v}=s,a=range?v||['','']:[v||''];
 root.querySelectorAll('[data-vt-part]').forEach((x,i)=>{x.value=type==='multiple'?(v.length?v.length+' 个日期':''):fmt(a[i],type)});
 root.querySelectorAll('input[type=hidden]').forEach((x,i)=>x.value=type==='multiple'?JSON.stringify(v):a[i]);
 root.querySelector('[data-vt-clear]').hidden=disabled(p)||readonly(p)||!v||type==='multiple'&&!v.length;
 const tags=root.querySelector('[data-vt-tags]');tags.innerHTML=type==='multiple'&&v.length?v.slice(0,p.maxTagCount??2).map(d=>`<span class="v-multi-chip"><span>${E(d.replaceAll('-','/'))}</span><button type="button" data-vt-remove="${d}" aria-label="移除 ${d}" ${disabled(p)||readonly(p)?'disabled':''}>${I('close',12)}</button></span>`).join('')+(v.length>(p.maxTagCount??2)?`<button type="button" class="v-multi-overflow" data-vt-open ${disabled(p)||readonly(p)?'disabled':''}>+${v.length-(p.maxTagCount??2)}</button>`:''):'';
}
function emit(s){s.root.dispatchEvent(new CustomEvent('voc:change',{bubbles:true,detail:{component:s.key,action:s.type==='time'?'time-change':s.type==='date'?'date-change':s.key+'-change',value:s.value===null?null:JSON.parse(JSON.stringify(s.value)),name:s.p.name||s.key}}))}
function commit(s,v,keep=false){s.value=v;update(s);report(s);emit(s);if(!keep)close(s,true)}
function validatePair(s,a){if(a.some(v=>!allowed(v,s.p,s.type)))return '值无效、超出限制或包含不可选日期';if(s.range&&a[0]>a[1])return '结束值不能早于开始值';if(s.range&&s.type!=='time'&&(s.p.disabledDates||[]).some(d=>d>=dateBounds(a[0],s.type)[0]&&d<=dateBounds(a[1],s.type)[1]))return '范围内包含不可选日期';return ''}
function parse(s){if(disabled(s.p)||readonly(s.p)||s.type==='multiple')return;const a=[...s.root.querySelectorAll('[data-vt-part]')].map((x,i)=>{const current=s.range?s.value?.[i]:s.value;return x.value===fmt(current,s.type)?current||'':x.value.trim().replaceAll('/','-').replace('T',' ')});if(a.every(x=>!x)){commit(s,null);return}if(a.some(x=>!x)){report(s,'请填写完整的开始与结束值');return}const error=validatePair(s,a);if(error){report(s,error);return}commit(s,s.range?a:a[0])}
function position(s){if(!s.popup)return;const b=s.root.querySelector('.vt-field').getBoundingClientRect(),n=s.popup;n.style.width=Math.min(s.range&&s.type!=='time'?624:s.type==='datetime'?352:320,innerWidth-24)+'px';n.style.maxHeight=Math.max(140,innerHeight-24)+'px';const h=n.offsetHeight,w=n.offsetWidth,below=innerHeight-b.bottom-12,above=b.top-12,down=below>=h||below>=above;n.style.maxHeight=Math.max(120,(down?below:above)-6)+'px';n.style.left=Math.max(12,Math.min(b.left,innerWidth-w-12))+'px';n.style.top=Math.max(12,down?b.bottom+6:b.top-Math.min(h,above)+-6)+'px'}
function close(s,focus=false){if(!s.popup)return;s.popup.remove();s.popup=null;s.popAbort.abort();s.root.querySelector('[data-vt-open]')?.setAttribute('aria-expanded','false');if(active===s)active=null;if(focus&&s.root.isConnected)s.root.querySelector('[data-vt-open]').focus()}
function periodValue(s,d){return s.type==='week'?weekOf(d):s.type==='month'?d.slice(0,7):s.type==='year'?d.slice(0,4):s.type==='quarter'?d.slice(0,4)+'-Q'+Math.ceil(Number(d.slice(5,7))/3):d}
function selected(s,v){return s.type==='multiple'?s.draft.includes(v):s.draft.includes(v)}
function availableDay(s,d){if(s.type==='datetime'){return !(s.p.disabledDates||[]).includes(d)&&(!s.p.min||d>=s.p.min.slice(0,10))&&(!s.p.max||d<=s.p.max.slice(0,10))}return allowed(periodValue(s,d),s.p,s.type)}
function grid(s,month){
 const first=month.slice(0,7)+'-01',weekday=(utc(first).getUTCDay()+6)%7,start=M.addDays(first,-weekday);let cells='';
 for(let i=0;i<42;i++){const d=M.addDays(start,i),v=periodValue(s,d),other=d.slice(0,7)!==first.slice(0,7),sel=s.type==='datetime'?s.draft.some(x=>x.slice(0,10)===d):selected(s,v),between=s.range&&s.draft[0]&&s.draft[1]&&v>s.draft[0]&&v<s.draft[1];cells+=`<button type="button" data-vt-day="${d}" aria-label="${d}" aria-pressed="${!!sel}" data-other="${other}" data-between="${!!between}" ${d===today()?'aria-current="date"':''} ${!availableDay(s,d)?'disabled':''} tabindex="${!other&&d===(s.focusDay||first)?'0':'-1'}">${Number(d.slice(-2))}</button>`}
 return `<div class="vt-month">${s.range&&s.type==='date'?`<div class="vt-month-title">${first.slice(0,4)} 年 ${Number(first.slice(5,7))} 月</div>`:''}<div class="vt-weekdays">${'一二三四五六日'.split('').map(x=>'<span>'+x+'</span>').join('')}</div><div class="vt-days" role="group" aria-label="${first.slice(0,7)} 日历">${cells}</div></div>`;
}
function periodGrid(s){const y=Number(s.month.slice(0,4)),type=s.type;let entries=[];
 if(type==='year'){const base=Math.floor(y/12)*12;entries=Array.from({length:12},(_,i)=>String(base+i).padStart(4,'0')).filter(x=>Number(x)>0&&Number(x)<10000)}
 if(type==='month')entries=Array.from({length:12},(_,i)=>y+'-'+pad(i+1));
 if(type==='quarter')entries=Array.from({length:4},(_,i)=>y+'-Q'+(i+1));
 return `<div class="vt-periods" data-kind="${type}">${entries.map(v=>`<button type="button" data-vt-period="${v}" aria-pressed="${selected(s,v)}" ${!allowed(v,s.p,type)?'disabled':''}>${E(type==='month'?Number(v.slice(-2))+' 月':type==='quarter'?'第 '+v.slice(-1)+' 季度':v+' 年')}</button>`).join('')}</div>`;
}
function timeColumns(s,index){let v=s.draft[index]||'',parts=v.split(':'),count=s.p.seconds?3:2;return `<div class="vt-time" data-time-index="${index}">${Array.from({length:count},(_,col)=>{const max=col===0?24:60,step=col===1?Math.min(30,Math.max(1,Math.floor(Number(s.p.step)||15))):1,values=[...new Set([...Array.from({length:Math.ceil(max/step)},(_,i)=>pad(i*step)),...(parts[col]?[parts[col]]:[])])].sort();return `<div><span class="v-caption">${['时','分','秒'][col]}</span><div class="vt-time-list" role="listbox" aria-label="${s.range?(index?'结束':'开始'):''}${['小时','分钟','秒'][col]}">${values.map(x=>`<button type="button" role="option" aria-selected="${x===parts[col]}" data-vt-time="${index}:${col}:${x}">${x}</button>`).join('')}</div></div>`}).join('')}</div>`}
function draw(s,restore){const n=s.popup;if(!n)return;const y=Number(s.month.slice(0,4)),period=['year','month','quarter'].includes(s.type),time=s.type==='time';
 const presets=s.p.presets||(s.type==='date'&&s.range?[{label:'近七天',value:M.preset('7')},{label:'本周',value:M.preset('week')},{label:'本月',value:M.preset('month')}]:[]);n.innerHTML=`${presets.length?`<div class="vt-presets">${presets.map((x,i)=>`<button type="button" class="v-btn" data-variant="ghost" data-vt-preset="${i}">${E(x.label)}</button>`).join('')}</div>`:''}${!time?`<header class="vt-head"><button type="button" class="v-btn v-icon-btn" data-vt-nav="-1" aria-label="上${period?'一组':'个月'}">${I('back',15)}</button><div><input type="number" min="1" max="9999" value="${y}" aria-label="定位年份" data-vt-year><span>年</span>${!period?`<select aria-label="定位月份" data-vt-month>${Array.from({length:12},(_,i)=>`<option value="${i+1}" ${i+1===Number(s.month.slice(5,7))?'selected':''}>${i+1} 月</option>`).join('')}</select>`:''}</div><button type="button" class="v-btn v-icon-btn" data-vt-nav="1" aria-label="下${period?'一组':'个月'}">${I('arrow',15)}</button></header>`:''}${time?`<div class="vt-time-panels">${timeColumns(s,0)}${s.range?timeColumns(s,1):''}</div>`:period?periodGrid(s):`<div class="vt-calendar-panels">${grid(s,s.month)}${s.range&&s.type==='date'?grid(s,M.shiftMonth(s.month,1)):''}</div>`}${s.type==='datetime'?s.clock.map((v,i)=>`<label class="vt-datetime-time">${s.range?(i?'结束时间':'开始时间'):'时间'}<input type="time" data-vt-clock="${i}" aria-label="${s.range?(i?'结束时间':'开始时间'):'时间'}" value="${E(v)}" ${s.p.seconds?'step="1"':''}></label>`).join(''):''}<div class="vt-selection" data-vt-selection>${E(s.type==='multiple'?`已选 ${s.draft.length} 个日期`:s.draft.filter(Boolean).map(v=>fmt(v,s.type)).join(' → ')||'请选择'+(s.range?'开始值':'一个值'))}</div>${s.type==='multiple'?`<div class="vt-selected-dates">${s.draft.map(d=>`<button type="button" class="v-tag" data-vt-unpick="${d}" aria-label="取消 ${d}">${d}${I('close',12)}</button>`).join('')}</div>`:''}<p class="v-error" data-vt-warning role="status"></p><footer class="vt-foot"><button type="button" class="v-btn" data-variant="ghost" data-vt-cancel>取消</button>${s.type==='date'||s.type==='multiple'?'<button type="button" class="v-btn" data-variant="ghost" data-vt-today>今天</button>':''}<button type="button" class="v-btn" data-variant="primary" data-vt-apply>确定</button></footer>`;
 position(s);if(restore)n.querySelector(restore)?.focus();
 n.querySelectorAll('.vt-time-list [aria-selected=true]').forEach(b=>{b.parentElement.scrollTop=Math.max(0,b.offsetTop-b.parentElement.offsetTop-54)});
}
function choose(s,v){if(s.type==='datetime'){const i=s.range&&s.draft[0]&&!s.draft[1]&&v>=s.draft[0].slice(0,10)?1:0;v=v+' '+s.clock[i]}if(s.type==='multiple')s.draft=s.draft.includes(v)?s.draft.filter(x=>x!==v):[...s.draft,v].sort();else if(s.range){if(!s.draft[0]||s.draft[1]||v<s.draft[0])s.draft=[v,''];else s.draft=[s.draft[0],v]}else s.draft=[v];draw(s)}
function apply(s){let a=[...s.draft];
 if(s.type==='multiple'){commit(s,a);return}if(a.some(v=>!v)||s.range&&a.length!==2){s.popup.querySelector('[data-vt-warning]').textContent='请完成'+(s.range?'开始与结束':'')+'选择';return}
 const error=validatePair(s,a);if(error){s.popup.querySelector('[data-vt-warning]').textContent=error;return}commit(s,s.range?a:a[0]);
}
function open(s){if(disabled(s.p)||readonly(s.p))return;if(s.popup){close(s,true);return}if(active)close(active);active=s;
 const v=s.value;s.draft=s.type==='multiple'?[...v]:s.range?v?[...v]:['','']:[v||''];
 if(s.type==='time')s.draft=s.draft.map(x=>x||('09:00'+(s.p.seconds?':00':'')));
 let base=s.draft[0]||today();if(s.type==='week')base=weekStart(base)||today();if(s.type==='time')base=today();s.month=base.slice(0,4)+'-'+(s.type==='year'||s.type==='quarter'?'01':base.slice(5,7)||'01')+'-01';s.focusDay=base.length>=10?base.slice(0,10):s.month;s.clock=(s.range?[0,1]:[0]).map(i=>{const x=s.range?v?.[i]:v;return s.type==='datetime'&&x?x.split(' ')[1]:'09:00'+(s.p.seconds?':00':'')});
 const n=document.createElement('div');n.className='vt-popup';n.id=ids();n.setAttribute('role','dialog');n.setAttribute('aria-label',(s.p.label||specs[s.key][2])+'选择');n.dataset.kind=s.type;(s.root.closest('dialog')||document.body).append(n);s.popup=n;s.root.querySelector('[data-vt-open]').setAttribute('aria-expanded','true');s.popAbort=new AbortController();const signal=s.popAbort.signal;
 draw(s);(n.querySelector('[aria-pressed=true],.vt-time-list [aria-selected=true]')||n.querySelector('[data-vt-day]:not([data-other=true]):not(:disabled),[data-vt-period]:not(:disabled)')||n.querySelector('button'))?.focus();
 n.addEventListener('click',e=>{const b=e.target.closest('button');if(!b||b.disabled)return;if(b.hasAttribute('data-vt-nav')){const step=Number(b.dataset.vtNav)*(s.type==='year'?144:['month','quarter'].includes(s.type)?12:1),next=M.shiftMonth(s.month,step);if(Number(next.slice(0,4))>0&&Number(next.slice(0,4))<10000)s.month=next;draw(s,`[data-vt-nav="${b.dataset.vtNav}"]`)}
 else if(b.dataset.vtDay){s.focusDay=b.dataset.vtDay;choose(s,periodValue(s,b.dataset.vtDay));n.querySelector(`[data-vt-day="${s.focusDay}"]`)?.focus()}
 else if(b.dataset.vtPeriod){choose(s,b.dataset.vtPeriod);n.querySelector(`[data-vt-period="${b.dataset.vtPeriod}"]`)?.focus()}
 else if(b.dataset.vtTime){const [idx,col,v]=b.dataset.vtTime.split(':'),a=s.draft[idx].split(':');a[col]=v;s.draft[idx]=a.join(':');draw(s,`[data-vt-time="${b.dataset.vtTime}"]`)}
 else if(b.hasAttribute('data-vt-preset')){const presets=s.p.presets||[{label:'近七天',value:M.preset('7')},{label:'本周',value:M.preset('week')},{label:'本月',value:M.preset('month')}],v=presets[Number(b.dataset.vtPreset)].value,a=Array.isArray(v)?v:[v];const error=s.type==='multiple'?a.every(x=>allowed(x,s.p,s.type))?'':'快捷日期包含不可选值':validatePair(s,a);if(error)n.querySelector('[data-vt-warning]').textContent=error;else {s.draft=s.type==='multiple'?[...new Set(a)].sort():[...a];if(s.type==='datetime')s.clock=a.map(x=>x.split(' ')[1]);const first=s.type==='week'?weekStart(a[0]):a[0];if(s.type!=='time')s.month=first.slice(0,4)+'-'+(s.type==='year'||s.type==='quarter'?'01':first.slice(5,7)||'01')+'-01';draw(s)}}
 else if(b.dataset.vtUnpick){s.draft=s.draft.filter(x=>x!==b.dataset.vtUnpick);draw(s)}
 else if(b.hasAttribute('data-vt-apply'))apply(s);else if(b.hasAttribute('data-vt-cancel'))close(s,true);else if(b.hasAttribute('data-vt-today')){const d=today();if(allowed(d,s.p,s.type)){s.month=d.slice(0,7)+'-01';choose(s,d)}}});
 n.addEventListener('change',e=>{if(e.target.matches('[data-vt-year],[data-vt-month]')){const year=Number(n.querySelector('[data-vt-year]').value),month=Number(n.querySelector('[data-vt-month]')?.value||1);if(year>=1&&year<=9999){s.month=String(year).padStart(4,'0')+'-'+pad(month)+'-01';draw(s,e.target.matches('[data-vt-year]')?'[data-vt-year]':'[data-vt-month]')}}if(e.target.matches('[data-vt-clock]')){const i=Number(e.target.dataset.vtClock);s.clock[i]=e.target.value;if(s.draft[i])s.draft[i]=s.draft[i].slice(0,10)+' '+s.clock[i];n.querySelector('[data-vt-selection]').textContent=s.draft.filter(Boolean).map(v=>fmt(v,s.type)).join(' → ')}});
 n.addEventListener('keydown',e=>{if(e.key==='Escape'){e.preventDefault();close(s,true);return}const day=e.target.closest('[data-vt-day]');if(day&&['ArrowLeft','ArrowRight','ArrowUp','ArrowDown','Home','End','PageUp','PageDown'].includes(e.key)){e.preventDefault();let v=day.dataset.vtDay;v=e.key==='PageUp'||e.key==='PageDown'?M.shiftMonth(v,e.key==='PageUp'?-1:1):M.addDays(v,e.key==='Home'?-(utc(v).getUTCDay()+6)%7:e.key==='End'?6-(utc(v).getUTCDay()+6)%7:({ArrowLeft:-1,ArrowRight:1,ArrowUp:-7,ArrowDown:7})[e.key]);if(Number(v.slice(0,4))<1||Number(v.slice(0,4))>9999)return;s.focusDay=v;s.month=v.slice(0,7)+'-01';draw(s,`[data-vt-day="${v}"]`)}
 else if(['ArrowDown','ArrowUp','Home','End'].includes(e.key)&&e.target.matches('[role=option],[data-vt-period]')){e.preventDefault();const options=[...e.target.parentElement.querySelectorAll('button:not(:disabled)')],i=options.indexOf(e.target),next=e.key==='Home'?0:e.key==='End'?options.length-1:(i+(e.key==='ArrowDown'?1:-1)+options.length)%options.length;options[next]?.focus()}});
 document.addEventListener('pointerdown',e=>{if(!n.contains(e.target)&&!s.root.contains(e.target))close(s)},{capture:true,signal});document.addEventListener('focusin',e=>{if(!n.contains(e.target)&&!s.root.contains(e.target))close(s)},{signal});window.addEventListener('resize',()=>position(s),{signal});window.addEventListener('scroll',e=>{if(!n.contains(e.target))position(s)},{capture:true,signal});
}
function all(root){return [...(root.matches?.('[data-vt]')?[root]:[]),...root.querySelectorAll('[data-vt]')]}
function hydrate(root){all(root).forEach(r=>{if(states.has(r))return;const p=JSON.parse(r.dataset.vtProps),key=r.dataset.vt,[type,range]=specs[key];const s={root:r,key,p,type,range,value:normalize(p,type,range),abort:new AbortController()};states.set(r,s);update(s);const signal=s.abort.signal;r.addEventListener('focusin',e=>{if(!e.target.matches('[data-vt-part]')||disabled(p)||readonly(p)||type==='multiple')return;const a=range?s.value||['','']:[s.value||''];e.target.value=a[Number(e.target.dataset.vtPart)]||''},{signal});r.addEventListener('focusout',e=>{if(!e.target.matches('[data-vt-part]')||type==='multiple')return;const a=range?s.value||['','']:[s.value||''];const v=a[Number(e.target.dataset.vtPart)]||'';if(e.target.value===v)e.target.value=fmt(v,type)},{signal});r.addEventListener('click',e=>{if(disabled(p)||readonly(p))return;if(e.target.closest('[data-vt-open]')||type==='multiple'&&e.target.matches('[data-vt-part]'))open(s);else if(e.target.closest('[data-vt-clear]'))commit(s,type==='multiple'?[]:null);else if(e.target.closest('[data-vt-remove]'))commit(s,s.value.filter(d=>d!==e.target.closest('[data-vt-remove]').dataset.vtRemove))},{signal});r.addEventListener('change',e=>{if(e.target.matches('[data-vt-part]'))parse(s)},{signal});r.addEventListener('keydown',e=>{if(e.key==='ArrowDown'&&e.target.matches('[data-vt-part]')){e.preventDefault();open(s)}else if(e.key==='Enter'&&e.target.matches('[data-vt-part]')){e.preventDefault();parse(s)}else if(e.key==='Escape')close(s,true)},{signal})})}
function destroy(root){all(root).forEach(r=>{const s=states.get(r);if(s){close(s);s.abort.abort();states.delete(r)}})}
Object.keys(specs).forEach(key=>U.register(key,p=>render(key,p)));
window.VocTemporal={hydrate,destroy,getValue(el){const r=el.matches?.('[data-vt]')?el:el.querySelector('[data-vt]'),s=states.get(r);return s?JSON.parse(JSON.stringify(s.value)):undefined},math:{valid,weekOf,weekStart,dateBounds,normalize,allowed},specs};
})();
