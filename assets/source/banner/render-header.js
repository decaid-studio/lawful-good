const { chromium } = require('playwright'); const path = require('path');
(async () => { const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1280, height: 320 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.resolve(process.argv[2])); await p.waitForTimeout(500);
  await p.screenshot({ path: process.argv[3], clip: { x: 0, y: 0, width: 1280, height: 320 } }); await b.close(); })();
