// Builds the guide PDF and preview images for the landing page.
// Usage: node tools/build.js   (run from gta6-guide/)
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const root = path.resolve(__dirname, '..');
const src = 'file://' + path.join(root, 'guide', 'guide.html');
const pdfOut = path.join(root, 'dist', 'Leonida-Playbook-GTA-VI-Guide.pdf');
const prevDir = path.join(root, 'site', 'img');


// Spread leftover space evenly between blocks so every page looks full.
const fillPages = () => {
  document.querySelectorAll('.page:not(.cover2)').forEach(pg => {
    const kids = [...pg.querySelectorAll(':scope > *')].filter(e => !e.matches('.foot,.run,svg,.meta'));
    if (kids.length < 3) return;
    const R = pg.getBoundingClientRect();
    const bottom = Math.max(...kids.map(e => e.getBoundingClientRect().bottom));
    const gap = R.bottom - 0.62 * 96 - 12 - bottom;
    if (gap <= 4) return;
    const movable = kids.slice(3); // keep kicker, title, rule tight
    if (!movable.length) return;
    const each = Math.min(gap / movable.length, 40);
    movable.forEach(e => { const cs = getComputedStyle(e); e.style.marginTop = (parseFloat(cs.marginTop) + each) + 'px'; });
  });
};

(async () => {
  fs.mkdirSync(path.dirname(pdfOut), { recursive: true });
  fs.mkdirSync(prevDir, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 816, height: 1056 } });
  await page.goto(src, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.evaluate(fillPages);

  // Overflow check: any element whose bottom extends past its page's content area.
  const problems = await page.evaluate(() => {
    const out = [];
    document.querySelectorAll('.page').forEach((pg, i) => {
      const r = pg.getBoundingClientRect();
      const limit = r.bottom - 0.62 * 96; // keep clear of footer
      pg.querySelectorAll(':scope > *:not(.foot):not(.run):not(svg):not(.meta)').forEach(el => {
        const b = el.getBoundingClientRect().bottom;
        if (b > limit) out.push(`page ${i + 1}: <${el.tagName.toLowerCase()} class="${el.className}"> overflows by ${Math.round(b - limit)}px`);
      });
    });
    return out;
  });
  if (problems.length) console.log('OVERFLOW:\n' + problems.join('\n')); else console.log('No overflow.');

  await page.pdf({ path: pdfOut, width: '8.5in', height: '11in', printBackground: true, preferCSSPageSize: true });
  console.log('PDF ->', pdfOut);

  // Preview images of selected pages for the landing page.
  const pick = { cover: 1, whatsnew: 3, rob: 6 };
  const scale = process.argv.includes('--all') ? null : pick;
  const hi = await browser.newPage({ viewport: { width: 816, height: 1056 }, deviceScaleFactor: 1.5 });
  await hi.goto(src, { waitUntil: 'networkidle' });
  await hi.evaluate(() => document.fonts.ready);
  await hi.evaluate(fillPages);
  const pages = await hi.$$('.page');
  const targets = scale ? Object.entries(pick) : pages.map((_, i) => ['p' + String(i + 1).padStart(2, '0'), i + 1]);
  for (const [name, n] of targets) {
    await pages[n - 1].screenshot({ path: path.join(scale ? prevDir : path.join(root, 'dist', 'pages'), `${name}.jpg`), type: 'jpeg', quality: 82 });
  }
  console.log('Previews done.');
  await browser.close();
})();
