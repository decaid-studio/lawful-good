# Banner sources

- `social-preview.png` (1280 × 640) and the README header are built on DECAID Prismatic renders
  (`hd_a.jpg`, `sp_b.jpg`, AI-generated). Both images carry the label "KI ✦" and the IPTC value
  `trainedAlgorithmicMedia`.
- README header: `readme-header.html` (1280 × 320), rendered at 2x with
  `node render-header.js readme-header.html ../../readme-header@2x.png` (Playwright).
  Needs Satoshi 500/700/900 as `satoshi-<weight>.woff2` next to the HTML (fontshare.com,
  not included here).
- The diagrams are built by `../build.py` and `../render.js`.
