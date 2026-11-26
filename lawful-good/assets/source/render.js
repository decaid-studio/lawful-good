const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const [dir, outdir] = process.argv.slice(2);
  fs.mkdirSync(outdir, { recursive: true });
  const b = await chromium.launch();
  for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.svg'))) {
    const svg = fs.readFileSync(path.join(dir, f), 'utf8');
    const m = svg.match(/width="(\d+)" height="(\d+)"/);
    const w = +m[1], h = +m[2];
    const scale = f.startsWith('social-preview') ? 1 : 2;
    const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: scale });
    await p.goto('file://' + path.join(dir, f));
    await p.waitForTimeout(400);
    const name = f.replace('.svg', scale === 2 ? '@2x.png' : '.png');
    await p.screenshot({ path: path.join(outdir, name), clip: { x: 0, y: 0, width: w, height: h } });
    await p.close();
  }
  await b.close();
})();
