# Contributing

Thanks for helping. lawful-good is maintained by DECAID.

## How it works

1. Open an issue first for anything larger than a fix, so we can agree on the direction.
2. One change per pull request. Run `python tools/lg.py validate` before pushing; the
   GitHub Action runs it too.
3. Every text field needs `de` and `en`.
4. A DECAID maintainer reviews and merges. Changes to the meaning of a control or
   threshold need approval from a DECAID maintainer.

## Rules for content

- **No text, tables, structure or mappings from purchased standards** (CEN/CENELEC,
  ISO/IEC, DIN or others), not even paraphrased.
- References only to openly available sources (laws, NIST publications, OWASP and similar).
- Recommendations, not legal statements: never claim conformity.
- Decision trees reference articles and do not interpret them. On critical questions,
  "unclear" must lead to a stop (`tools/lg.py validate` checks this).

## Sign-off

Sign off every commit (`git commit -s`). By doing so you confirm the
[Developer Certificate of Origin](https://developercertificate.org/) and agree that code
is licensed under MIT and content under CC BY 4.0.
