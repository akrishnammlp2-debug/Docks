# Usage: serve a copy of the app at http://localhost:8765 (with fonts/fonts.css next to it), then: python3 tools/contrast_check.py <folder-with-fonts>
# Must report TOTAL issues: 0 before any colour/theme change is pushed (Apoorva, 13 Nov 2026).
# Contrast check: every visible text element on every tab (+ key sheets), light and dark. Flags WCAG ratio < 4.5 (normal) / < 3 (large >= 18.66px bold or 24px).
import sys,asyncio,json
from playwright.async_api import async_playwright
S=sys.argv[1]; TABS=['today','reminders','study','todos','calendar','advances','ot','roster','cases','music','nba','backup','others']
JS=r"""()=>{
const parse=c=>{const m=c.match(/rgba?\(([^)]+)\)/);if(!m)return null;const p=m[1].split(',').map(x=>parseFloat(x));return {r:p[0],g:p[1],b:p[2],a:p.length>3?p[3]:1};};
const lum=c=>{const f=v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)};return .2126*f(c.r)+.7152*f(c.g)+.0722*f(c.b);};
const blend=(top,bot)=>({r:top.r*top.a+bot.r*(1-top.a),g:top.g*top.a+bot.g*(1-top.a),b:top.b*top.a+bot.b*(1-top.a),a:1});
const bgOf=el=>{const layers=[];let e=el;while(e){const cs=getComputedStyle(e);if(cs.backgroundImage&&cs.backgroundImage!=='none'&&!/url\(/.test(cs.backgroundImage)){const m=cs.backgroundImage.match(/rgba?\([^)]+\)/g);if(m){const cols=m.map(parse);const avg=cols.reduce((a,c)=>({r:a.r+c.r/cols.length,g:a.g+c.g/cols.length,b:a.b+c.b/cols.length,a:1}),{r:0,g:0,b:0,a:1});layers.push(avg);break;}}
 if(/url\(/.test(cs.backgroundImage)&&e.tagName!=='BODY'){return null;}
 const c=parse(cs.backgroundColor);if(c&&c.a>0){layers.push(c);if(c.a>=.98)break;}e=e.parentElement;}
 let base={r:255,g:255,b:255,a:1};for(let i=layers.length-1;i>=0;i--)base=blend(layers[i],base);return base;};
const out=[];const seen=new Set();
document.querySelectorAll('body *').forEach(el=>{ if(!el.offsetParent&&getComputedStyle(el).position!=='fixed')return;
 const txt=[...el.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent.trim()).join(' ').trim(); if(!txt)return;
 const r=el.getBoundingClientRect(); if(r.width<2||r.height<2||r.bottom<0||r.top>innerHeight*3)return;
 const cs=getComputedStyle(el); if(cs.visibility==='hidden'||+cs.opacity<.2)return;
 if(el.closest('.tban,.pwx,.hero-top,.mplay,.ldot,[aria-hidden=true]'))return; // text over pictures handled by overlays
 let op=1,e=el;while(e){op*=+getComputedStyle(e).opacity;e=e.parentElement;} if(op<.2)return;
 const fg=parse(cs.color); const bg=bgOf(el); if(!fg||!bg)return;
 const f=blend({...fg,a:fg.a*op},bg); const L1=lum(f),L2=lum(bg); const ratio=(Math.max(L1,L2)+.05)/(Math.min(L1,L2)+.05);
 const size=parseFloat(cs.fontSize),bold=+cs.fontWeight>=700; const need=(size>=24||(size>=18.66&&bold))?3:4.5;
 const sheet=!!el.closest('#sheet'); if(sheet&&!document.getElementById('sheet').classList.contains('open'))return;
 const key=txt.slice(0,30)+'|'+Math.round(ratio*10); if(seen.has(key))return; seen.add(key);
 if(ratio<need) out.push({t:txt.slice(0,40),ratio:+ratio.toFixed(2),need,cls:(el.className&&el.className.baseVal===undefined?el.className:'')+' <'+el.tagName.toLowerCase()+'>',sheet});});
return out;}"""
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(); report={}
    for sc in ['light','dark']:
      c=await b.new_context(viewport={'width':390,'height':844},color_scheme=sc)
      await c.add_init_script("(()=>{const D=Date;const off=(()=>{const d=new D();const t=new D(d);t.setHours(22,10,0,0);return t-d;})();window.Date=class extends D{constructor(...a){if(a.length)super(...a);else super(D.now()+off);}static now(){return D.now()+off;}};})()")
      pg=await c.new_page()
      await pg.route('**/fonts.googleapis.com/**',lambda r:r.fulfill(path=S+'/e2e/fonts/fonts.css',content_type='text/css'))
      await pg.goto('http://localhost:8765/#today'); await pg.wait_for_timeout(1200)
      await pg.evaluate("state.private=state.private||{};state.private.ot=state.private.ot||{};OTL().forEach(r=>{state.private.ot[r.id]={patient:'Test Patient',age:'40 M',uhid:'00000000'}});state.settings.weatherOn=true;render();")
      for t in TABS:
        await pg.evaluate(f"goTab('{t}')"); await pg.wait_for_timeout(350)
        report[f'{sc}:{t}']=await pg.evaluate(JS)
      for name,js in [('sheet:item',"goTab('today');itemSheet(REG[0]||{title:'x',date:today()})"),('sheet:bite',"biteSheet('psv')"),('sheet:habits',"habitMonthSheet()"),('sheet:book',"bookSheet('chambers-physiology')"),('sheet:search',"searchSheet();document.querySelector('[data-search]').value='a';renderSearch('a')"),('sheet:mycase',"mcPick()"),('drawer',"closeSheet();openDrawer()")]:
        try:
          await pg.evaluate(js); await pg.wait_for_timeout(350); report[f'{sc}:{name}']=await pg.evaluate(JS)
        except Exception as e: report[f'{sc}:{name}']=[{'error':str(e)[:80]}]
        await pg.evaluate("closeSheet();closeDrawer&&closeDrawer()")
      await c.close()
    await b.close()
    bad={k:v for k,v in report.items() if v}
    json.dump(report,open(S+'/contrast_report.json','w'),indent=1)
    for k,v in bad.items():
      print(k, len(v)); [print('   ',x) for x in v[:8]]
    print('TOTAL issues:',sum(len(v) for v in bad.values()))
asyncio.run(main())
