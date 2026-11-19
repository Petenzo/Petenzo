// Builds the guide PDF and preview images for the landing page.
// Usage: node tools/build.js   (run from gta6-guide/)
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const root = path.resolve(__dirname, '..');
const src = 'file://' + path.join(root, 'guide', 'guide.html');
const pdfOut = path.join(root, 'dist', 'Leonida-Playbook-GTA-VI-Guide.pdf');
const prevDir = path.join(root, 'site', 'img');

(async () => {
  fs.mkdirSync(path.dirname(pdfOut), { recursive: true });
  fs.mkdirSync(prevDir, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 816, height: 1056 } });
  await page.goto(src, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);

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
  const pick = { cover: 1, money: 5, heat: 8 };
  const scale = process.argv.includes('--all') ? null : pick;
  const hi = await browser.newPage({ viewport: { width: 816, height: 1056 }, deviceScaleFactor: 1.5 });
  await hi.goto(src, { waitUntil: 'networkidle' });
  await hi.evaluate(() => document.fonts.ready);
  const pages = await hi.$$('.page');
  const targets = scale ? Object.entries(pick) : pages.map((_, i) => ['p' + String(i + 1).padStart(2, '0'), i + 1]);
  for (const [name, n] of targets) {
    await pages[n - 1].screenshot({ path: path.join(scale ? prevDir : path.join(root, 'dist', 'pages'), `${name}.jpg`), type: 'jpeg', quality: 82 });
  }
  console.log('Previews done.');
  await browser.close();
})();
