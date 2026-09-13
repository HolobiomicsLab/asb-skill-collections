# paired-omics-bgc-metabolite-linking-workflow

**Status:** published as an **outline** — the structure is validated, the execution is not.
**Kind:** composite-workflow (P1 canonical set).
**Bound by:** perspicacite-semantic (text-embedding-3-large retrieval + EDAM-aware primary selection).

> Automatic grading of `workflow.yaml` (`asb solve-workflow`, checkpoint mode) is **not part of
> this release**: no released ASB version loads these files. Follow the stages yourself. The stage
> structure is validated by `validate_workflows.py` through `release_gate.py`.

## Stages

1. **bgc_mine** — assembled genomes -> detected BGCs (antiSMASH genome mining)  →  `biosynthetic-gene-cluster-detection-and-annotation`, `genomic-bgc-extraction-antismash`, `biosynthetic-gene-cluster-annotation`
2. **bgc_tokenize** — GenBank BGC records -> Pfam-domain tokens and sub-cluster motifs (iPRESTO)  →  `biosynthetic-gene-cluster-tokenization`, `bgc-tokenization-with-pfam-domains`, `gene-tokenization-representation`, `pfam-domain-pattern-recognition`, `statistical-sub-cluster-detection`
3. **gcf_cluster** — BGCs -> gene cluster families (BiG-SCAPE similarity clustering)  →  `gcf-assignment-from-distance-matrix`, `gene-cluster-family-formation-and-similarity-clustering`, `big-slice-workflow-execution`, `bgc-sequence-domain-scanning`
4. **mf_network** — paired LC-MS/MS spectra -> molecular families (GNPS feature-based molecular networking)  →  `spectral-similarity-network-generation`, `metabolomic-spectral-annotation-and-molecular-family-clustering`, `metabolomic-molecular-family-networking-gnps`, `spectral-similarity-network-building`
5. **link_score** — GCFs + MFs + strain co-occurrence -> ranked GCF-MF links (NPLinker Metcalf/hypergeometric scoring)  →  `bgc-mf-link-scoring`, `link-scoring-metcalf-algorithm`, `gcf-mf-link-scoring`, `gcf-mf-link-scoring-computation`, `strain-correlation-hypergeometric-adjustment`
6. **report** — consolidate scored links + provenance into a ranked BGC-metabolite link table  →  `genomic-metabolomic-link-ranking`, `statistical-enrichment-analysis`, `gcf-mf-hierarchical-aggregation`

`derived_from_workflows` in the frontmatter is a provenance record — the ASB per-paper workflows
whose structure corroborated this pipeline. No ablation experiment consuming it is released.
