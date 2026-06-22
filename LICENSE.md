# License

This repository is **dual-licensed by layer**.

## Code (scripts, tooling, pipeline glue)

Licensed under the **Apache License 2.0** — see [`LICENSE`](LICENSE) for the full
text. This covers everything under `scripts/`, `tools/`, and other executable
code in the repository.

## Collection content (skill descriptions, tool records, structured metadata)

Licensed under **Creative Commons Attribution 4.0 International (CC-BY-4.0)**.
This covers the `SKILL.md` bodies + frontmatter, `tools/*.yaml`, the JSON indexes,
and the collection metadata — i.e. the curated, evidence-grounded knowledge. Each
`SKILL.md`, `collection.yaml`, and `CITATION.cff` carries `license: CC-BY-4.0`.

You are free to share and adapt this content for any purpose, including
commercially, **provided you give appropriate credit** — cite the collection
(see `CITATION.cff`) **and** the original source paper of each skill
(`attribution.original_doi`).

## Verbatim quotations from scientific papers

Short verbatim quotes from the source papers are included as `evidence_spans` in
skill frontmatter solely for scientific attribution. They are reproduced under
**fair use / quotation right** (UK copyright §30; EU Copyright Directive
Art. 5.3(d); US Copyright 17 U.S.C. §107):

- Quotes are minimal (typically one sentence), non-substitutive.
- Attribution is provided via DOI + author list in `derived_from` / `attribution`.
- No commercial use of the verbatim quotes themselves is intended.

If a rights holder objects to a specific quote, please open an issue and it will
be removed promptly.

## Benchmark tasks and workflows (when released)

Benchmark task descriptions, evaluation manifests, and workflows will be released
under Apache-2.0. Raw paper content is not reproduced in benchmark files.
