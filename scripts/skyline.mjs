// "Commit City": renders the last 52 weeks of contributions as an isometric
// night skyline. One building per week; height = commits; lit windows = active days.
// Usage: GITHUB_TOKEN=... GH_USER=roni0028 node scripts/skyline.mjs  (no token -> demo data)
import { writeFileSync } from 'node:fs';
const user = process.env.GH_USER || 'roni0028';
const token = process.env.GITHUB_TOKEN;
let weeks, total, streak = 0, best = 0, demo = false;
if (token) {
  const q = `query($l:String!){user(login:$l){contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{contributionCount date}}}}}}`;
  const r = await fetch('https://api.github.com/graphql', { method: 'POST',
    headers: { Authorization: `bearer ${token}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ query: q, variables: { l: user } }) });
  const j = await r.json();
  const cal = j.data.user.contributionsCollection.contributionCalendar;
  total = cal.totalContributions;
  weeks = cal.weeks.map(w => w.contributionDays.map(d => d.contributionCount));
} else {
  demo = true; let s = 7; const rnd = () => (s = (s * 9301 + 49297) % 233280) / 233280;
  weeks = Array.from({ length: 53 }, () => Array.from({ length: 7 }, () => (rnd() < .65 ? Math.floor(rnd() * 9) : 0)));
  total = weeks.flat().reduce((a, b) => a + b, 0);
}
for (const c of weeks.flat()) { streak = c ? streak + 1 : 0; best = Math.max(best, streak); }
const max = Math.max(1, ...weeks.map(w => w.reduce((a, b) => a + b, 0)));
const themes = {
  dark: { sky1: '#0b1020', sky2: '#1e1b4b', b1: '#1f2937', b2: '#111827', b3: '#374151', win: '#fde68a', fg: '#e6edf3', mut: '#94a3b8', acc: '#22d3ee', moon: '#f8fafc' },
  light: { sky1: '#fde68a', sky2: '#fbcfe8', b1: '#6366f1', b2: '#4338ca', b3: '#818cf8', win: '#fef9c3', fg: '#1f2328', mut: '#475569', acc: '#0891b2', moon: '#fb923c' },
};
const W = 900, H = 320, G = 250;
for (const [mode, t] of Object.entries(themes)) {
  let b = '';
  weeks.forEach((days, i) => {
    const sum = days.reduce((a, c) => a + c, 0);
    const h = 8 + Math.round((sum / max) * 150), x = 40 + i * 15.5, w = 11, d = 5, y = G - h;
    const delay = (i * 0.03).toFixed(2);
    let win = '';
    days.forEach((c, k) => { for (let r = 0; r < Math.floor(h / 14); r++) if (c && (r + k) % 7 === k % 7)
      win += `<rect x="${x + 2 + (k % 2) * 5}" y="${y + 6 + r * 14}" width="3" height="4" fill="${t.win}" style="animation:fl ${2 + (k + r) % 5}s ${(r * .3).toFixed(1)}s infinite"/>`; });
    b += `<g style="transform-origin:${x}px ${G}px;animation:rise .9s ${delay}s cubic-bezier(.2,.8,.2,1) both"><title>week ${i + 1}: ${sum}</title>
<polygon points="${x},${y} ${x + d},${y - d} ${x + w + d},${y - d} ${x + w},${y}" fill="${t.b3}"/>
<polygon points="${x + w},${y} ${x + w + d},${y - d} ${x + w + d},${G - d} ${x + w},${G}" fill="${t.b2}"/>
<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${t.b1}"/>${win}</g>`;
  });
  const stars = mode === 'dark' ? Array.from({ length: 50 }, (_, i) => `<circle cx="${(i * 173) % W}" cy="${(i * 37) % 120}" r="${(i % 3) * .4 + .5}" fill="#fff" style="animation:fl ${2 + i % 4}s ${(i % 7) * .3}s infinite"/>`).join('') : '';
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
<style>@keyframes rise{from{transform:scaleY(0)}to{transform:scaleY(1)}}@keyframes fl{0%,100%{opacity:1}50%{opacity:.35}}
@keyframes car{from{transform:translateX(-40px)}to{transform:translateX(${W + 40}px)}}
text{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}</style>
<defs><linearGradient id="s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${t.sky1}"/><stop offset="1" stop-color="${t.sky2}"/></linearGradient><clipPath id="c"><rect width="${W}" height="${H}" rx="14"/></clipPath></defs>
<g clip-path="url(#c)"><rect width="${W}" height="${H}" fill="url(#s)"/>${stars}
<circle cx="820" cy="60" r="24" fill="${t.moon}" opacity=".9"/>
${b}<rect y="${G}" width="${W}" height="${H - G}" fill="${t.b2}"/>
<line x1="0" y1="${G + 14}" x2="${W}" y2="${G + 14}" stroke="${t.win}" stroke-dasharray="14 10" opacity=".5"/>
<g style="animation:car 9s linear infinite"><rect y="${G + 4}" width="22" height="7" rx="3" fill="${t.acc}"/><circle cx="24" cy="${G + 7}" r="2" fill="${t.win}"/></g>
<text x="24" y="34" font-size="18" font-weight="700" fill="${t.fg}">COMMIT CITY · @${user}</text>
<text x="24" y="54" font-size="12" fill="${t.mut}">1 building = 1 week · lights = active days${demo ? ' · (demo data)' : ''}</text>
<text x="24" y="${H - 22}" font-size="13" fill="${t.fg}">▲ ${total} contributions / last year   ⚡ longest daily streak: ${best}d   🕒 updated ${new Date().toISOString().slice(0, 10)}</text>
</g></svg>`;
  writeFileSync(new URL(`../assets/skyline-${mode}.svg`, import.meta.url), svg);
}
console.log('skyline ok', { total, best, demo });
