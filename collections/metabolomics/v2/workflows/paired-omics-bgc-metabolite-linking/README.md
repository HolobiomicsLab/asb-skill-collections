# paired-omics-bgc-metabolite-linking-workflow — STAGING

**Status:** STAGING ONLY — promote via `release_gate.py` after human review.
**Kind:** composite-workflow (P1 canonical set).
**Bound by:** perspicacite-semantic (text-embedding-3-large retrieval + EDAM-aware primary selection).

## Stages

1. **bgc_mine** — assembled genomes -> detected BGCs (antiSMASH genome mining)  →  `biosynthetic-gene-cluster-detection-and-annotation`, `genomic-bgc-extraction-antismash`, `biosynthetic-gene-cluster-annotation`
2. **bgc_tokenize** — GenBank BGC records -> Pfam-domain tokens and sub-cluster motifs (iPRESTO)  →  `biosynthetic-gene-cluster-tokenization`, `bgc-tokenization-with-pfam-domains`, `gene-tokenization-representation`, `pfam-domain-pattern-recognition`, `statistical-sub-cluster-detection`
3. **gcf_cluster** — BGCs -> gene cluster families (BiG-SCAPE similarity clustering)  →  `gcf-assignment-from-distance-matrix`, `gene-cluster-family-formation-and-similarity-clustering`, `big-slice-workflow-execution`, `bgc-sequence-domain-scanning`
4. **mf_network** — paired LC-MS/MS spectra -> molecular families (GNPS feature-based molecular networking)  →  `spectral-similarity-network-generation`, `metabolomic-spectral-annotation-and-molecular-family-clustering`, `metabolomic-molecular-family-networking-gnps`, `spectral-similarity-network-building`
5. **link_score** — GCFs + MFs + strain co-occurrence -> ranked GCF-MF links (NPLinker Metcalf/hypergeometric scoring)  →  `bgc-mf-link-scoring`, `link-scoring-metcalf-algorithm`, `gcf-mf-link-scoring`, `gcf-mf-link-scoring-computation`, `strain-correlation-hypergeometric-adjustment`
6. **report** — consolidate scored links + provenance into a ranked BGC-metabolite link table  →  `genomic-metabolomic-link-ranking`, `statistical-enrichment-analysis`, `gcf-mf-hierarchical-aggregation`

`derived_from_workflows` in the frontmatter is the eval-ablation set (SPEC §8).
