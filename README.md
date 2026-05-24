# ASB-Skill-Collections

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.PLACEHOLDER.svg)](https://doi.org/10.5281/zenodo.PLACEHOLDER)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-HolobiomicsLab-yellow)](https://huggingface.co/HolobiomicsLab)
[![w3id](https://img.shields.io/badge/IRI-w3id.org%2Fholobiomicslab-blue)](https://w3id.org/holobiomicslab)
[![License](https://img.shields.io/badge/license-Apache--2.0-green)](LICENSE)

Curated, evidence-grounded scientific-agent skill + tool + benchmark collections
produced by the [AgenticScienceBuilder](https://github.com/HolobiomicsLab/AgenticScienceBuilder)
pipeline, maintained by [Holobiomics Lab](https://github.com/HolobiomicsLab).

## What is in here

| Artifact | Description |
|---|---|
| **ASB-Skills** | Curated, deduplicated procedural knowledge for scientific AI agents |
| **ASB-Benchmark** | Per-paper tasks with workflows + claim-retrieval test sets for evaluation |
| **ASB-Tools** | Globally-deduplicated software-tool records with EDAM annotations |
| **ASB-Capsules** | Raw per-paper ASB pipeline outputs (v1.1, deferred) |

## Quick install (Claude Code)

```bash
/plugin install metabolomics-v1@HolobiomicsLab/asb-skill-collections
```

## Browse collections

- [`collections/`](collections/) — released, tagged collections
- [`staged-collections/`](staged-collections/) — in-progress, under review

## For agents: how skills are structured

Each skill is a `SKILL.md` file with YAML frontmatter containing:
- EDAM operation/topic IRIs (for pre-filtered retrieval)
- `derived_from` DOIs (source papers)
- `evidence_spans` (verbatim quotes from papers)
- `tools` (linked ASB-Tool records)
- `claims` (indicium claim IRIs, or empty list)

The collection `_router/SKILL.md` is loaded by default and routes to specific skills
via Perspicacite KB search.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the curator workflow.
COI policy: [COI_POLICY.md](COI_POLICY.md).

## Citation

If you use these collections in research, please cite the per-collection `CITATION.cff`
(automatically generated at release). The Zenodo DOI above is a placeholder; it will be
minted on first release tag.

## License

Apache-2.0 for synthesis layer; fair-use for verbatim paper quotes.
See [LICENSE.md](LICENSE.md) for details.
