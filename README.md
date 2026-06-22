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
/plugin marketplace add HolobiomicsLab/asb-skill-collections
/plugin install metabolomics@asb-skill-collections
```

The first public release is the **metabolomics** collection
([`collections/metabolomics/v2`](collections/metabolomics/v2), tag
`metabolomics-v0.1.0`): 5,865 evidence-grounded skills over 909 tools. See its
[USAGE.md](collections/metabolomics/v2/USAGE.md) for search → install → use →
Perspicacité grounding. Other domains in `collections/` are staged/internal and
not part of this release.

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

---

## Distribution

### Badges

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.PLACEHOLDER.svg)](https://doi.org/10.5281/zenodo.PLACEHOLDER)
[![HuggingFace Datasets](https://img.shields.io/badge/HuggingFace-Datasets-yellow?logo=huggingface)](https://huggingface.co/HolobiomicsLab)
[![HuggingFace Spaces](https://img.shields.io/badge/HuggingFace-Spaces-orange?logo=huggingface)](https://huggingface.co/spaces/HolobiomicsLab)
[![w3id IRI](https://img.shields.io/badge/IRI-w3id.org%2Fholobiomicslab-blue)](https://w3id.org/holobiomicslab)

### How to install a collection (Claude Code)

```bash
# Install latest metabolomics collection
/plugin install metabolomics-v1@HolobiomicsLab/asb-skill-collections

# Or point directly to the marketplace.json
/plugin install https://raw.githubusercontent.com/HolobiomicsLab/asb-skill-collections/main/.claude-plugin/marketplace.json
```

Collections are listed in [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json).

### HuggingFace mirror

Each tagged release (`<slug>-v<N>`) is automatically mirrored to a HuggingFace Dataset repo:

```
HolobiomicsLab/asb-<slug>-v<N>
```

Programmatic access:

```python
from datasets import load_dataset
ds = load_dataset("HolobiomicsLab/asb-metabolomics-v1", "benchmark")
```

A live leaderboard HF Space is created at:

```
https://huggingface.co/spaces/HolobiomicsLab/asb-<slug>-v<N>-leaderboard
```

### Zenodo

Each collection release will mint a Zenodo DOI. See `CITATION.cff` at the collection root for the full citation. **The metabolomics v0.1.0 Zenodo DOI is not minted yet** (`doi: TODO-zenodo`); the Zenodo badge above is a placeholder until then.

### w3id.org IRIs

> **Note:** these `w3id.org/holobiomicslab/` IRIs are **reserved identifiers and
> do not resolve yet** — the redirect is not live. Treat them as stable names
> for now, not as working links. The same applies to the w3id badges above and
> the `@id` / `iri` fields in `collection.yaml`.

Skills and tools are *intended* to be addressable via stable IRIs under
`w3id.org/holobiomicslab/` (once the redirect is configured):

```
https://w3id.org/holobiomicslab/asb-skill/<slug>
https://w3id.org/holobiomicslab/asb-tool/<slug>
https://w3id.org/holobiomicslab/asb-benchmark/<slug>/v<N>
```
