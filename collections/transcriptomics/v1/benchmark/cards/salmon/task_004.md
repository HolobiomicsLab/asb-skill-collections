# SciTask Card: Analyze the effect of seed representation variants on mapping rate and NumReads Pearson

- Task ID: `task_004`
- Schema version: `0.18.0`
- Created at: `2026-06-15T18:27:16.217915+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_transcriptomics/coll_salmon/synthesized_package`
- Domain: `bioinformatics`
- Subtask categories: `benchmark-evaluation`, `data-analysis`
- DOI: `10.1038/nmeth.4197`
- GitHub: `COMBINE-lab/salmon`
- Input from: `task_001`

## Classification

- Task kind: `analysis`
- Article type: `research-article`
- Primary domain: `transcriptomics`
- Subdomains: `rna-seq`, `differential-expression`
- Techniques: `quantitative-structure-activity`, `statistical-analysis`

## Research Question
Does the mapping rate and NumReads Pearson correlation remain stable when the Rust mapper uses alternative seed representations (sparse fixed-k anchors, reference k-mer variants) instead of the default unitig-constrained approach?

## Connected Finding
On byte-identical index, NumReads Pearson correlation between C++ and Rust is 0.99854, demonstrating high quantitative agreement across implementations and seed strategies.

## Task Description
Re-run the Rust salmon mapper on the GEUVADIS ERR188044 dataset using three alternative seed representations (sparse fixed-k anchors, reference-extended MEMs, and true unitig-constrained uni-MEMs), measure mapping rate and NumReads Pearson correlation under each variant, and verify that Pearson r remains ≥0.99999995 across all variants to confirm seed granularity was not the cause of prior mapping discrepancies.

## Inputs
- GEUVADIS ERR188044 paired-end 76 bp reads (36.35M reads)
- Byte-identical GRCh38 cDNA reference index (193,759 transcripts)

## Expected Outputs
- Mapping rate (%) for default seed representation
- Mapping rate and NumReads Pearson r for sparse fixed-k anchor variant
- Mapping rate and NumReads Pearson r for reference-extended MEM variant
- Mapping rate and NumReads Pearson r for unitig-constrained uni-MEM variant
- Summary table with per-variant mapping rate and Pearson r values

## Expected Output File

- `seed_variant_comparison.csv`

## Landmark Outputs

- `default_baseline_quant.sf`
- `sparse_k_quant.sf`
- `refmem_quant.sf`
- `unimem_quant.sf`
- `pearson_correlation_matrix.csv`

## Tools
- salmon 2.0
- piscem-rs

## Skills
- read-mapping-rate-calculation
- pearson-correlation-analysis-genomics
- seed-representation-variant-comparison
- selective-alignment-parameter-configuration
- transcript-abundance-correlation-validation

## Workflow Description
1. Download or retrieve the GEUVADIS ERR188044 paired-end 76 bp reads (36.35M) and byte-identical reference index (GRCh38 cDNA, 193,759 transcripts). 2. Run salmon 2.0 Rust mapper in selective-alignment mode with default seed representation (-l A, no bias correction, -p for multi-threading) and record mapping rate and per-transcript NumReads output. 3. Re-run salmon mapper with sparse fixed-k anchor representation, capturing mapping rate and NumReads correlation (Pearson r) against baseline. 4. Re-run salmon mapper with reference-extended MEM representation, recording mapping rate and NumReads Pearson r. 5. Re-run salmon mapper with true unitig-constrained uni-MEM representation, capturing mapping rate and NumReads Pearson r. 6. Calculate Pearson correlation coefficient (r) between NumReads counts from each variant and the default baseline using correlation analysis, verifying r ≥ 0.99999995 for all variants. 7. Validation: confirm mapping rate remains within ≤0.01% of baseline and Pearson r for all three variants meets or exceeds 0.99999995 threshold, establishing that seed representation granularity does not explain prior C++ vs. Rust mapping differences.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `paper.md` | main_article | True |

## Data Deposits

| Kind | Accession | URL | Evidence |
|---|---|---|---|
| sra_run | `ERR458493` | https://www.ncbi.nlm.nih.gov/sra/?term=ERR458493 | tion correctly) was right all along.  ## Dataset  - Reads: `ERR458493` (Gierliński/Schurch *S. cerevisiae* benchmark),   1,093,95 |
| sra_run | `ERR188044` | https://www.ncbi.nlm.nih.gov/sra/?term=ERR188044 | set), so the only variable is the mapper. Reads: GEUVADIS `ERR188044` (36.35M 76bp PE); default selective alignment, `-l A`, no |

## Missing Information
- No quantitative mapping rate or NumReads Pearson results are reported for alternative seed representations (sparse fixed-k anchors, reference k-mer variants) on ERR188044.
- The discussion reports per-transcript Pearson ≈ 0.999 but does not specify the NumReads Pearson correlation or mapping rate achieved under the tested seed variants.
- No methodological details are provided on how alternative seed representations (sparse fixed-k anchors, reference k-mer variants) were generated or parameterized for the experiment.

## Domain Knowledge
- Seed granularity (k-mer anchor density and MEM coverage) affects chaining heuristics and alignment chain selection, but per-transcript read-count quantification (NumReads) should remain stable if the underlying seed landscape supports the same true alignments.
- Pearson correlation coefficient r ≥ 0.99999995 is a stringent threshold (five 9's after the decimal) used to establish near-perfect agreement in read-assignment counts across algorithmic variants, ruling out granularity as a confound.
- Unitig-constrained uni-MEMs represent reference-anchored maximal-exact-matches whose endpoints are bounded by de Bruijn graph unitig boundaries; reference-extended MEMs extend into mismatches or lower-complexity regions; sparse fixed-k anchors are pre-defined k-mer positions — each represents a different seeding strategy with different computational trade-offs.
- Byte-identical index construction ensures that both algorithm variants operate on the same k-mer hash landscape and reference sequence representation, isolating the effect of seed-collection strategy alone and excluding index randomization or non-ACGT base replacement as confounds.
- Mapping rate is the percentage of input reads achieving at least one confident alignment; it is sensitive to both seed support (seed discovery) and alignment scoring thresholds, so identical mapping rates across seed variants suggest that all strategies discover sufficiently dense seed support for true alignments.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: salmon 2.0, piscem-rs, Mapping rate (%) for default seed representation, Mapping rate and NumReads Pearson r for sparse fixed-k anchor variant, Mapping rate and NumReads Pearson r for reference-extended MEM variant, Mapping rate and NumReads Pearson r for unitig-constrained uni-MEM variant, Summary table with per-variant mapping rate and Pearson r values.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [methods] Does the mapping rate and NumReads Pearson correlation remain stable when the Rust mapper uses alternative seed representations (sparse fixed-k anchors, reference k-mer variants) instead of the default unitig-constrained approach?: 're-running the Rust mapper with sparse fixed-k anchors, reference-extended MEMs, and true unitig-constrained uni-MEMs'
- `ev_002` from `agent2_synthesis` (agent2_traced): [methods] On byte-identical index, NumReads Pearson correlation between C++ and Rust is 0.99854, demonstrating high quantitative agreement across implementations and seed strategies.: 'NumReads Pearson | 0.99854'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] GEUVADIS ERR188044 paired-end 76 bp reads (36.35M reads): 'Reads: GEUVADIS ERR188044 (36.35M 76bp PE)'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] Byte-identical GRCh38 cDNA reference index (193,759 transcripts): 'byte-identical index — both tools' indices built from the same clean.fa (deterministic non-ACGT replacement, identical 193,759-transcript set)'
- `ev_005` from `agent2_synthesis` (agent2_traced): [methods] Mapping rate (%) for default seed representation: 're-running the Rust mapper with sparse fixed-k anchors, reference-extended MEMs, and true unitig-constrained uni-MEMs gave identical results (85.55%, NumReads r ≥ 0.99999995)'
- `ev_006` from `agent2_synthesis` (agent2_traced): [methods] Mapping rate and NumReads Pearson r for sparse fixed-k anchor variant: 'sparse fixed-k anchors, reference-extended MEMs, and true unitig-constrained uni-MEMs gave identical results (85.55%, NumReads r ≥ 0.99999995)'
- `ev_007` from `agent2_synthesis` (agent2_traced): [methods] Mapping rate and NumReads Pearson r for reference-extended MEM variant: 'sparse fixed-k anchors, reference-extended MEMs, and true unitig-constrained uni-MEMs gave identical results (85.55%, NumReads r ≥ 0.99999995)'
- `ev_008` from `agent2_synthesis` (agent2_traced): [methods] Mapping rate and NumReads Pearson r for unitig-constrained uni-MEM variant: 'sparse fixed-k anchors, reference-extended MEMs, and true unitig-constrained uni-MEMs gave identical results (85.55%, NumReads r ≥ 0.99999995)'
- `ev_009` from `agent2_synthesis` (agent2_traced): [methods] Summary table with per-variant mapping rate and Pearson r values: 'identical results (85.55%, NumReads r ≥ 0.99999995)'
- `ev_010` from `agent2_synthesis` (agent2_traced): [methods] salmon 2.0: 're-running the Rust mapper with sparse fixed-k anchors, reference-extended MEMs, and true unitig-constrained uni-MEMs'
- `ev_011` from `agent2_synthesis` (agent2_traced): [methods] piscem-rs: 'The Rust port (built on piscem-rs, which derives orientation correctly) was right all along'
- `ev_012` from `agent2_synthesis` (agent2_traced): [discussion] No quantitative mapping rate or NumReads Pearson results are reported for alternative seed representations (sparse fixed-k anchors, reference k-mer variants) on ERR188044.: 'On our benchmarks (human GEUVADIS `ERR188044` against a GRCh38 cDNA index, and yeast `ERR458493`), selective-alignment quantification reproduces C++ salmon to per-transcript Pearson ≈ 0.999'
- `ev_013` from `agent2_synthesis` (agent2_traced): [discussion] The discussion reports per-transcript Pearson ≈ 0.999 but does not specify the NumReads Pearson correlation or mapping rate achieved under the tested seed variants.: 'SA quantification agrees at Pearson 0.999 and the entire mapping-rate delta is explained by (1) one describable orphan/post-merge pruning default that is off-by-default in Rust, and (2) benign'
- `ev_014` from `agent2_synthesis` (agent2_traced): [methods] No methodological details are provided on how alternative seed representations (sparse fixed-k anchors, reference k-mer variants) were generated or parameterized for the experiment.: 're-running the Rust mapper with sparse fixed-k anchors, reference-extended MEMs, and true unitig-constrained uni-MEMs'

## Evaluation Strategy
### Direct Checks
- verify file outputs/ERR188044_sparse_anchors.mapping_rates.txt exists and contains numeric mapping rate and NumReads Pearson values; robust to parameter choices in seed representation
- verify file outputs/ERR188044_fixed_k_anchors.mapping_rates.txt exists and contains numeric mapping rate and NumReads Pearson values; robust to parameter choices in seed representation
- verify file outputs/ERR188044_reference_kmers.mapping_rates.txt exists and contains numeric mapping rate and NumReads Pearson values; robust to parameter choices in seed representation
- value of NumReads Pearson field in outputs/ERR188044_sparse_anchors.mapping_rates.txt is >= 0.99999995
- value of NumReads Pearson field in outputs/ERR188044_fixed_k_anchors.mapping_rates.txt is >= 0.99999995
- value of NumReads Pearson field in outputs/ERR188044_reference_kmers.mapping_rates.txt is >= 0.99999995
- verify that mapping rate (percentage of reads mapped) across all three seed variants differs by < 1% absolute; parameter-sensitive to index and read set

### Expert Review
- assess whether the reported NumReads Pearson values (≥0.99999995) across seed variants are statistically consistent with the claim that seed granularity was not the root cause of mapping discrepancy
- evaluate whether the choice of sparse fixed-k anchors, reference k-mer variants, and unitig-constrained MEMs constitutes a sufficiently comprehensive variant space to establish robustness to seed representation
- review the experimental design to confirm that the alternative seed representations were applied to the same ERR188044 reads and GRCh38 cDNA index used in the reported baseline (36.35M 76bp PE)

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** heavy

## Methodology Summary
1. Load GEUVADIS ERR188044 (36.35M paired-end 76 bp reads) and byte-identical GRCh38 cDNA reference index (193,759 transcripts).
2. Execute salmon 2.0 Rust mapper in selective-alignment mode with default seed representation (libType A, no bias, multi-threaded) and record mapping rate and NumReads per transcript.
3. Re-run salmon mapper three times, each with an alternative seed representation (sparse fixed-k anchors, reference-extended MEMs, unitig-constrained uni-MEMs), recording mapping rate and per-transcript NumReads.
4. Calculate Pearson correlation coefficient between NumReads vectors from each variant and the baseline default.
5. Validation: confirm all variants achieve mapping rate within ≤0.01% of baseline and Pearson r ≥ 0.99999995 for NumReads, establishing seed granularity was not the root cause of prior C++ vs. Rust mapping discrepancies.
6. References: source article (DOI: 10.1038/nmeth.4197); ERR458493 (https://www.ncbi.nlm.nih.gov/sra/?term=ERR458493); ERR188044 (https://www.ncbi.nlm.nih.gov/sra/?term=ERR188044)

## Workflow Ports

**Inputs:**

- `reads_err188044` — GEUVADIS ERR188044 paired-end 76bp reads (36.35M) ← `task_001/numreads_pearson`
- `ref_index` — Byte-identical GRCh38 cDNA reference index (193,759 transcripts)

**Outputs:**

- `default_mapping_rate` — Mapping rate (%) for default seed representation
- `sparse_k_variant` — Mapping rate and NumReads Pearson r for sparse fixed-k anchor variant
- `refmem_variant` — Mapping rate and NumReads Pearson r for reference-extended MEM variant
- `unimem_variant` — Mapping rate and NumReads Pearson r for unitig-constrained uni-MEM variant
- `variant_comparison_table` — Summary table with per-variant mapping rate and Pearson r values

**Used:** `urn:asb:port:task_001/numreads_pearson`

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:COMBINE-lab__salmon`
- **Synthesized at:** 2026-06-15T18:38:25+00:00

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
