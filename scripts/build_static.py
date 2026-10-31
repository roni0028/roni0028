# Generates static animated SVGs (dark + light) for the profile README.
import os
OUT=os.path.join(os.path.dirname(__file__),'..','assets')
T={'dark':dict(bg='#0d1117',fg='#e6edf3',mut='#8b949e',card='#161b22',bd='#30363d',a='#7c3aed',b='#06b6d4',c='#f472b6'),
   'light':dict(bg='#ffffff',fg='#1f2328',mut='#59636e',card='#f6f8fa',bd='#d0d7de',a='#6d28d9',b='#0891b2',c='#db2777')}
FONT="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
SANS="-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"
def w(n,s): open(os.path.join(OUT,n),'w').write(s)

def hero(t,m):
    stars=''.join(f'<circle cx="{(i*137)%1200}" cy="{(i*71)%300}" r="{1+(i%3)*.5}" fill="{t["fg"]}" opacity=".5" style="animation:tw {2+i%4}s {i%5*.4}s infinite"/>' for i in range(40))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="300" viewBox="0 0 1200 300">
<style>
@keyframes g{{0%{{stop-color:{t["a"]}}}50%{{stop-color:{t["b"]}}}100%{{stop-color:{t["a"]}}}}}
@keyframes g2{{0%{{stop-color:{t["c"]}}}50%{{stop-color:{t["a"]}}}100%{{stop-color:{t["c"]}}}}}
@keyframes tw{{0%,100%{{opacity:.15}}50%{{opacity:.9}}}}
@keyframes gl1{{0%,88%,100%{{transform:translate(0,0)}}90%{{transform:translate(-6px,2px)}}93%{{transform:translate(5px,-2px)}}96%{{transform:translate(-3px,0)}}}}
@keyframes gl2{{0%,88%,100%{{transform:translate(0,0)}}90%{{transform:translate(6px,-2px)}}93%{{transform:translate(-5px,2px)}}96%{{transform:translate(3px,0)}}}}
@keyframes up{{from{{opacity:0;transform:translateY(14px)}}to{{opacity:1;transform:none}}}}
@keyframes scan{{from{{transform:translateY(-20px)}}to{{transform:translateY(320px)}}}}
@keyframes grid{{from{{transform:translateY(0)}}to{{transform:translateY(40px)}}}}
.n{{font:800 76px {SANS};letter-spacing:-2px}}
.r{{animation:gl1 4s infinite}} .c{{animation:gl2 4s infinite}}
.s{{font:500 24px {SANS};fill:{t["mut"]};animation:up 1s .4s both}}
.p{{font:600 15px {FONT};animation:up 1s .9s both}}
</style>
<defs><linearGradient id="gr" x1="0" x2="1"><stop offset="0" style="animation:g 6s infinite"/><stop offset="1" style="animation:g2 6s infinite"/></linearGradient>
<clipPath id="cp"><rect width="1200" height="300" rx="18"/></clipPath></defs>
<g clip-path="url(#cp)"><rect width="1200" height="300" fill="{t["bg"]}"/>
<g opacity=".18" style="animation:grid 3s linear infinite">{''.join(f'<line x1="0" y1="{y}" x2="1200" y2="{y}" stroke="{t["b"]}"/>' for y in range(-40,340,40))}{''.join(f'<line x1="{x}" y1="-40" x2="{x}" y2="340" stroke="{t["b"]}"/>' for x in range(0,1240,40))}</g>
{stars}
<rect width="1200" height="3" fill="{t["b"]}" opacity=".35" style="animation:scan 5s linear infinite"/>
<g transform="translate(70,150)">
<text class="n r" fill="{t["c"]}" opacity=".7">Ronicarlos Ferreira</text>
<text class="n c" fill="{t["b"]}" opacity=".7">Ronicarlos Ferreira</text>
<text class="n" fill="url(#gr)">Ronicarlos Ferreira</text></g>
<text x="72" y="200" class="s">Senior Full Stack Developer · Tech Lead @ Nimo Club</text>
<g class="p"><rect x="72" y="228" width="330" height="34" rx="17" fill="none" stroke="{t["a"]}"/><circle cx="92" cy="245" r="5" fill="#22c55e"><animate attributeName="opacity" values="1;.2;1" dur="1.5s" repeatCount="indefinite"/></circle>
<text x="106" y="250" fill="{t["fg"]}">open to remote · BR · US · PT</text></g>
<g transform="translate(1010,150)" opacity=".9"><g><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="18s" repeatCount="indefinite"/>
<ellipse rx="95" ry="36" fill="none" stroke="{t["b"]}" stroke-width="2"/><ellipse rx="95" ry="36" fill="none" stroke="{t["a"]}" stroke-width="2" transform="rotate(60)"/><ellipse rx="95" ry="36" fill="none" stroke="{t["c"]}" stroke-width="2" transform="rotate(120)"/></g>
<circle r="14" fill="url(#gr)"/><text y="5" text-anchor="middle" font-family="{FONT}" font-size="11" font-weight="700" fill="{t["bg"]}">TS</text></g>
</g></svg>'''

LINES=[('$ ','whoami'),('','ronicarlos — senior full stack dev · tech lead @ nimo club'),
('$ ','cat stack.json | jq .'),('','{ "lang": ["TypeScript","JavaScript"], "front": ["React","Next.js","Vite"],'),
('','  "back": ["Node.js","Prisma","Supabase"], "infra": ["nginx","Vercel"] }'),
('$ ','nimo --status'),('','✔ community · AI studio · tournaments · subscription plans'),
('','✔ TypeScript full stack · sales landing page'),
('$ ','echo $OPEN_TO_WORK'),('','remote → 🇧🇷 Brazil · 🇺🇸 USA · 🇵🇹 Portugal'),('$ ','')]
def term(t,m):
    rows=[];y=70;delay=0
    for p,cmd in LINES:
        if p:
            n=max(len(cmd),1);dur=n*0.06
            rows.append(f'<g style="animation:sh 0s {delay:.2f}s both"><text x="24" y="{y}" fill="{t["b"]}">❯</text>'
              f'<svg x="44" y="{y-16}" width="900" height="22"><text y="16" fill="{t["fg"]}" style="animation:sh 0s {delay:.2f}s both">{cmd}</text><rect width="900" height="22" fill="{t["card"]}" style="animation:rev {dur:.2f}s {delay:.2f}s steps({n}) both"/></svg></g>')
            delay+=dur+0.3
        else:
            rows.append(f'<text x="44" y="{y}" fill="{t["mut"]}" style="animation:sh 0s {delay:.2f}s both">{cmd.replace("&","&amp;")}</text>');delay+=0.25
        y+=26
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="{y+10}" viewBox="0 0 900 {y+10}">
<style>@keyframes sh{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes rev{{from{{transform:translateX(0)}}to{{transform:translateX(900px)}}}}
@keyframes wipe{{from{{opacity:0}}to{{opacity:0}}}}
@keyframes blink{{50%{{opacity:0}}}}
text{{font:14px {FONT};white-space:pre}}</style>
<rect width="900" height="{y+10}" rx="12" fill="{t["card"]}" stroke="{t["bd"]}"/>
<rect width="900" height="36" rx="12" fill="{t["bd"]}" opacity=".5"/>
<circle cx="22" cy="18" r="6" fill="#ff5f57"/><circle cx="42" cy="18" r="6" fill="#febc2e"/><circle cx="62" cy="18" r="6" fill="#28c840"/>
<text x="450" y="23" text-anchor="middle" fill="{t["mut"]}" style="font-size:12px">roni0028 — zsh — 120×30</text>
{''.join(rows)}
<rect x="44" y="{y-26-14}" width="9" height="18" fill="{t["b"]}" style="animation:sh 0s {delay:.2f}s both,blink 1s {delay:.2f}s step-end infinite"/>
</svg>'''

STACK=[('TypeScript','TS','#3178c6'),('React','⚛','#61dafb'),('Next.js','N','#888'),('Node.js','⬢','#5fa04e'),
('Vite','⚡','#a855f7'),('Prisma','◭','#5a67d8'),('Supabase','⚡','#3ecf8e'),('nginx','N','#009639'),('Vercel','▲','#888'),('JavaScript','JS','#f7df1e')]
def cards(t,m):
    out=[]
    for i,(name,ic,col) in enumerate(STACK):
        x=10+(i%5)*176;y=10+(i//5)*110;d=i*.15
        out.append(f'''<g transform="translate({x},{y})"><g style="animation:pop .6s {d}s both,fl 4s {d}s ease-in-out infinite">
<rect width="160" height="92" rx="14" fill="{t["card"]}" stroke="{t["bd"]}"/>
<rect width="160" height="92" rx="14" fill="none" stroke="{col}" stroke-width="2" stroke-dasharray="80 420" style="animation:run 3s {d}s linear infinite"/>
<circle cx="34" cy="46" r="18" fill="{col}" opacity=".18"/><text x="34" y="52" text-anchor="middle" font-family="{FONT}" font-weight="800" font-size="15" fill="{col}">{ic}</text>
<text x="62" y="51" font-family="{SANS}" font-weight="600" font-size="15" fill="{t["fg"]}">{name}</text></g></g>''')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="230" viewBox="0 0 900 230">
<style>@keyframes pop{{from{{opacity:0;transform:scale(.8)}}to{{opacity:1;transform:none}}}}
@keyframes fl{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-4px)}}}}
@keyframes run{{to{{stroke-dashoffset:-500}}}}</style>{''.join(out)}</svg>'''

def divider(t,m):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="24" viewBox="0 0 900 24">
<style>@keyframes mv{{to{{stroke-dashoffset:-40}}}}</style>
<defs><linearGradient id="d" x1="0" x2="1"><stop offset="0" stop-color="{t["a"]}" stop-opacity="0"/><stop offset=".5" stop-color="{t["b"]}"/><stop offset="1" stop-color="{t["c"]}" stop-opacity="0"/></linearGradient></defs>
<path d="M0 12 Q 112 0 225 12 T 450 12 T 675 12 T 900 12" fill="none" stroke="url(#d)" stroke-width="2" stroke-dasharray="10 10" style="animation:mv 1s linear infinite"/>
<circle cx="450" cy="12" r="4" fill="{t["b"]}"><animate attributeName="r" values="3;6;3" dur="2s" repeatCount="indefinite"/></circle></svg>'''

for m,t in T.items():
    for n,f in [('hero',hero),('terminal',term),('stack',cards),('divider',divider)]:
        w(f'{n}-{m}.svg',f(t,m))
print('ok')
