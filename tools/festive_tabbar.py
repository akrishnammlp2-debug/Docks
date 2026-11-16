import math
def svg(w,h,g,vb=None): return ("url(\"data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='%s' height='%s' viewBox='%s'>%s</svg>\")"%(w,h,vb or f'0 0 {w} {h}',g)).replace('#','%23')
E=lambda g: svg(24,24,g)
rays=lambda c,c2: "".join(f"<path d='M{12+4*math.cos(a*math.pi/4):.1f} {12+4*math.sin(a*math.pi/4):.1f} L{12+9*math.cos(a*math.pi/4):.1f} {12+9*math.sin(a*math.pi/4):.1f}' stroke='{c if a%2 else c2}' stroke-width='1.8' stroke-linecap='round'/>" for a in range(8))+f"<circle cx='12' cy='12' r='1.6' fill='{c2}'/>"
petals=lambda n,r,pr,c,cx=12,cy=12: "".join(f"<circle cx='{cx+r*math.cos(a*2*math.pi/n):.1f}' cy='{cy+r*math.sin(a*2*math.pi/n):.1f}' r='{pr}' fill='{c}'/>" for a in range(n))
tree="<rect x='10.500' y='17' width='3' height='5' rx='.8' fill='#B98A5A'/><path d='M12 3 L18 11 H15.500 L20 18 H4 L8.500 11 H6 Z' fill='#6CC487'/><circle cx='12' cy='3.500' r='1.800' fill='#F2C14E'/><circle cx='10' cy='13' r='1.100' fill='#E25555'/><circle cx='14.500' cy='15.500' r='1.100' fill='#F2C14E'/>"
gift="<rect x='4.500' y='11' width='15' height='10' rx='1.500' fill='#E25555'/><rect x='3.500' y='8' width='17' height='4' rx='1.200' fill='#F07A7A'/><rect x='10.700' y='8' width='2.600' height='13' fill='#F2C14E'/><path d='M12 8 C9 2.500 4.500 4.500 8 8 Z M12 8 C15 2.500 19.500 4.500 16 8 Z' fill='#F2C14E'/>"
kite="<path d='M12 21 q-3 1.500 0 3' fill='none' stroke='#F4EDE0' stroke-width='1.200' stroke-linecap='round'/><path d='M12 2 L19 11 L12 20 L5 11 Z' fill='#F2A541'/><path d='M12 2 L19 11 H12 Z' fill='#E25555'/><path d='M12 11 V20 L5 11 Z' fill='#6CC487'/>"
sun="<circle cx='12' cy='12' r='4.500' fill='#F2C14E'/>"+"".join(f"<path d='M{12+6.5*math.cos(a*math.pi/4):.1f} {12+6.5*math.sin(a*math.pi/4):.1f} L{12+9.5*math.cos(a*math.pi/4):.1f} {12+9.5*math.sin(a*math.pi/4):.1f}' stroke='#F2C14E' stroke-width='1.800' stroke-linecap='round'/>" for a in range(8))
chakra="<circle cx='12' cy='12' r='8' fill='none' stroke='#A9C0FF' stroke-width='1.600'/><circle cx='12' cy='12' r='1.500' fill='#A9C0FF'/>"+"".join(f"<path d='M12 12 L{12+8*math.cos(a*math.pi/6):.1f} {12+8*math.sin(a*math.pi/6):.1f}' stroke='#A9C0FF' stroke-width='.9'/>" for a in range(12))
def flag(b,flip=False,ex=''):
    h=12/len(b); g="<rect x='4' y='3' width='1.800' height='19' rx='.9' fill='#D8C7A8'/>"+"".join(f"<rect x='5.800' y='{4+i*h:.1f}' width='15' height='{h+.2:.1f}' fill='{c}'/>" for i,c in enumerate(b))+ex
    return f"<g transform='translate(24 0) scale(-1 1)'>{g}</g>" if flip else g
moon="<path d='M13 3 A9 9 0 1 0 21 15.500 A7.200 7.200 0 1 1 13 3Z' fill='#F2C14E'/><path d='M17.500 6 l1.100 2.400 2.600 .3 -1.900 1.800 .5 2.600 -2.300 -1.300 -2.300 1.300 .5 -2.600 -1.900 -1.800 2.600 -.3z' fill='#FFE7A3'/>"
lantern="<path d='M12 1.500 V4' stroke='#F2C14E' stroke-width='1.400' stroke-linecap='round'/><rect x='9' y='4' width='6' height='2.400' rx='.8' fill='#F2C14E'/><path d='M8.500 6.400 h7 l2.300 6.300 -2.300 6.300 h-7 l-2.300 -6.300z' fill='#F2C14E'/><path d='M10.300 8.500 h3.400 l1.400 4.200 -1.400 4.200 h-3.400 l-1.400 -4.200z' fill='#FFF3C4'/><rect x='10' y='19' width='4' height='2.400' rx='.8' fill='#F2C14E'/>"
splat=lambda c,c2: f"<circle cx='11' cy='12' r='6.500' fill='{c}'/><circle cx='18.500' cy='8' r='2.600' fill='{c}'/><circle cx='5' cy='5.500' r='1.800' fill='{c2}'/><circle cx='17' cy='19' r='2.200' fill='{c2}'/><circle cx='4.500' cy='18.500' r='1.300' fill='{c}'/>"
mango="<path d='M8.500 6.500 C14 3.500 20 8 19 14 C18 20 10.500 22 6.500 17.500 C3.500 14 4.500 8.500 8.500 6.500Z' fill='#F2B632'/><path d='M8.500 6.500 C8 3 11 1.500 13.500 2.500 C12.500 5 10.500 6.300 8.500 6.500Z' fill='#6CC487'/>"
sprig="<path d='M12 22 V8' stroke='#6CC487' stroke-width='1.400' stroke-linecap='round'/><path d='M12 9 C8 8 6 5 6.500 2 C10 3 12 5.500 12 9Z M12 14 C16 13 18.500 10 18 7 C14.500 8 12 10.500 12 14Z M12 18 C8.500 17.500 6 15 6 12 C9.500 12.500 12 15 12 18Z' fill='#6CC487'/>"
marigold=petals(8,6.5,3.2,'#F28C28')+"<circle cx='12' cy='12' r='5.500' fill='#FFC93C'/><circle cx='12' cy='12' r='2.200' fill='#F28C28'/>"
lotus="<path d='M12 4 C15 9 15 14 12 19 C9 14 9 9 12 4Z' fill='#F7A8C4'/><path d='M4 9 C9 10 12 14 12 19 C7 19 4 14 4 9Z M20 9 C15 10 12 14 12 19 C17 19 20 14 20 9Z' fill='#EE86AD'/><path d='M2 15 C6 15 10 17 12 19 C8 21 4 19 2 15Z M22 15 C18 15 14 17 12 19 C16 21 20 19 22 15Z' fill='#E06C99'/>"
feather="<g transform='rotate(18 12 12)'><path d='M12 23 V12' stroke='#6CC487' stroke-width='1.400' stroke-linecap='round'/><ellipse cx='12' cy='9' rx='6' ry='8' fill='#3FAE7A'/><ellipse cx='12' cy='10' rx='4' ry='5.500' fill='#F2C14E'/><ellipse cx='12' cy='10.800' rx='2.700' ry='3.800' fill='#3C8FE0'/><ellipse cx='12' cy='11.500' rx='1.400' ry='2' fill='#1B2A6B'/></g>"
flute="<g transform='rotate(-28 12 12)'><rect x='1.500' y='10.300' width='21' height='3.400' rx='1.700' fill='#E3B663'/><circle cx='8' cy='12' r='.8' fill='#6B4A1E'/><circle cx='11.500' cy='12' r='.8' fill='#6B4A1E'/><circle cx='15' cy='12' r='.8' fill='#6B4A1E'/><rect x='18' y='10.300' width='1.600' height='3.400' fill='#E25555'/><path d='M19 13.700 q1 4 -1 6' fill='none' stroke='#E25555' stroke-width='1.200' stroke-linecap='round'/></g>"
modak="<path d='M12 3 C13 7 20 10 20 16 C20 19.500 16.500 21 12 21 C7.500 21 4 19.500 4 16 C4 10 11 7 12 3Z' fill='#FFF1DC'/><path d='M12 5 V21 M8.500 10.500 C7.500 14 7.500 18 8.500 20.500 M15.500 10.500 C16.500 14 16.500 18 15.500 20.500' fill='none' stroke='#E3C9A4' stroke-width='1'/>"
hibiscus=petals(5,5.6,4.6,'#E5484D')+"<circle cx='12' cy='12' r='2.400' fill='#F2C14E'/>"
diya="<path d='M12 2 C15.500 7 15 10.500 12 12 C9 10.500 8.500 7 12 2Z' fill='#FFB629'/><path d='M12 6.500 C13.600 9 13.300 10.800 12 11.600 C10.700 10.800 10.400 9 12 6.500Z' fill='#FFF3C4'/><path d='M3 13.500 Q12 24.500 21 13.500 Z' fill='#D98A3D'/><rect x='2' y='12' width='20' height='3' rx='1.500' fill='#B96A22'/>"
rangoli="<path d='M12 2 L14.500 9.500 L22 12 L14.500 14.500 L12 22 L9.500 14.500 L2 12 L9.500 9.500 Z' fill='#EE86AD'/><path d='M12 6 L16.200 7.800 L18 12 L16.200 16.200 L12 18 L7.800 16.200 L6 12 L7.800 7.800 Z' fill='none' stroke='#F2C14E' stroke-width='1.200'/><circle cx='12' cy='12' r='2' fill='#F2C14E'/>"
G="linear-gradient(180deg,#2C4A41,#1D3530)"
hair=lambda *c: "linear-gradient(180deg,"+",".join(f"{x} {i*2}px {i*2+2}px" for i,x in enumerate(c))+f",transparent {len(c)*2}px)"
snow=svg(48,9,"<path d='M0 0 H48 V4 Q42 8 36 5 T24 5.500 T12 5 T0 4 Z' fill='#FFFFFF' opacity='.92'/>")+" 0 0/48px 9px repeat-x"
toran=svg(18,13,"<path d='M0 1.500 H18' stroke='#D8C7A8' stroke-width='1.200'/><path d='M4.500 1.500 q-3.200 5.500 0 10.500 q3.200 -5 0 -10.500z' fill='#6CC487'/><path d='M13.500 1.500 q-3.200 4.500 0 8.500 q3.200 -4 0 -8.500z' fill='#4FAE6C'/>")+" 0 0/18px 13px repeat-x"
garland=svg(40,11,"".join(f"<circle cx='{2.5+5*i}' cy='{2.6+5.2*(1-((i-3.5)/3.5)**2):.1f}' r='2.700' fill='{'#F28C28' if i%2 else '#FFC93C'}'/>" for i in range(8)))+" 0 0/40px 11px repeat-x"
bunting=svg(36,9,"<path d='M0 1 H36' stroke='#F4EDE0' stroke-width='1'/><path d='M1 1 h8 l-4 7z' fill='#F2C14E'/><path d='M13 1 h8 l-4 7z' fill='#E25555'/><path d='M25 1 h8 l-4 7z' fill='#6CC487'/>")+" 0 0/36px 9px repeat-x"
dust=lambda c,c2: svg(90,60,f"<g opacity='.45'><circle cx='8' cy='7' r='.9' fill='{c}'/><circle cx='30' cy='5' r='.7' fill='{c2}'/><circle cx='52' cy='8' r='1' fill='{c2}'/><circle cx='74' cy='5' r='.8' fill='{c}'/><circle cx='84' cy='36' r='.8' fill='{c}'/><circle cx='40' cy='37' r='.7' fill='{c}'/></g>")+" 0 0/90px 60px repeat"
dotline=svg(10,6,"<circle cx='5' cy='3' r='1.300' fill='#F2C14E'/>")+" 0 1px/10px 6px repeat-x"
ring=lambda a,b=None: f"0 8px 18px -6px rgba(0,0,0,.5),0 0 0 4px #1D3530,"+(f"0 -1px 0 5px {a},0 1px 0 5px {b}" if b else f"0 0 0 5.500px {a}")
# theme: (left emblem, right emblem, bar background, home ring)
T={
'christmas':(tree,gift,snow+","+G,ring('#E25555')),
'newyear':(rays('#F2C14E','#FFF3C4'),rays('#9FC5FF','#FFFFFF'),dust('#F2C14E','#FFFFFF')+",linear-gradient(180deg,#27335C,#161D3A)",ring('#F2C14E')),
'sankranti':(kite,sun,bunting+","+G,ring('#F2C14E')),
'india':(chakra,flag(['#FF9933','#FFFFFF','#2FA84F'],True),hair('#FF9933','#FFFFFF','#2FA84F')+","+G,ring('#FF9933','#2FA84F')),
'rajyotsava':(flag(['#FFD400','#E8463E']),flag(['#FFD400','#E8463E'],True),hair('#FFD400','#E8463E')+","+G,ring('#FFD400','#E8463E')),
'eid':(moon,lantern,dust('#F2C14E','#FFF3C4')+",linear-gradient(180deg,#1F4A55,#12303C)",ring('#F2C14E')),
'holi':(splat('#FF6FB5','#FFD36B'),splat('#5CCBF5','#7CE38B'),"radial-gradient(70px 50px at 6% 100%,rgba(255,111,181,.36),transparent),radial-gradient(80px 50px at 34% 0,rgba(92,203,245,.28),transparent),radial-gradient(80px 50px at 68% 100%,rgba(255,211,107,.26),transparent),radial-gradient(70px 50px at 96% 0,rgba(124,227,139,.26),transparent),"+G,ring('#FF8CC4','#5CCBF5')),
'ugadi':(mango,sprig,toran+","+G,ring('#7CE38B')),
'dasara':(marigold,lotus,garland+","+G,ring('#F2A541')),
'janmashtami':(feather,flute,"linear-gradient(180deg,#1F5068,#143350)",ring('#8DB9FF','#F2C14E')),
'ganesha':(modak,hibiscus,dotline+",linear-gradient(180deg,#4A3A2C,#2E2A22)",ring('#F2A541')),
'diwali':(diya,rangoli,"radial-gradient(60% 110% at 50% 125%,rgba(255,170,60,.5),transparent 70%),linear-gradient(180deg,#33304A,#1E1B33)",ring('#FFC14E')),
}
Q='body[data-fest]:not([data-fest=""])'
css=f"""/* festive tab bar: each festival has its own bar (own colours or edge trim), two small emblems in the gaps between buttons, and its own ring on Home */
{Q} .tabbar>button{{position:relative;z-index:1}}
{Q} .tabbar{{background:var(--fb-bar);background-clip:padding-box}}
{Q} .tabbar::before,{Q} .tabbar::after{{content:"";position:absolute;top:11px;width:21px;height:21px;margin-left:-10.500px;background:center/contain no-repeat;opacity:.92;pointer-events:none;z-index:0}}
{Q} .tabbar::before{{left:calc(7px + (100% - 84px) / 4);background-image:var(--fb-l)}}
{Q} .tabbar::after{{left:calc(100% - 7px - (100% - 84px) / 4);background-image:var(--fb-r)}}
{Q} .tb-home{{box-shadow:var(--fb-ring)}}
"""+"".join(f"body[data-fest=\"{k}\"]{{--fb-l:{E(l)};--fb-r:{E(r)};--fb-bar:{bar};--fb-ring:{rg}}}\n" for k,(l,r,bar,rg) in T.items())
p='index.html'; L=open(p,encoding='utf-8').read().split('\n')
a=[k for k,l in enumerate(L) if l.startswith('/* festive tab bar:')][0]
b=max(k for k,l in enumerate(L) if l.startswith('body[data-fest="') and '--fb-' in l)
L[a:b+1]=css.rstrip('\n').split('\n'); s='\n'.join(L)
import re; s=re.sub(r"const APP_VERSION = '5\.4[89][^']*';","const APP_VERSION = '5.49 · a bar for every festival';",s)
open(p,'w',encoding='utf-8').write(s)
