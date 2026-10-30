---
name: amplicon-sequence-denoising
description: "Comparative amplicon sequence denoising versus clustering: infer representative sequence variants (ASVs) from trimmed COI paired-end reads with error-model denoisers (DADA2, Deblur) or VSEARCH OTU clustering, then benchmark unexpected-sequence (error) rates against a biological mock community to judge which pipeline and low-abundance filtering regime best controls spurious ASVs."
when_to_use_negative:
  - "Input is already a denoised feature table (this skill operates on raw/trimmed paired-end FASTQ reads)"
  - "Data are amino-acid sequences or require local alignment — VSEARCH supports only nucleotide global alignments"
  - "The goal is taxonomic classifier benchmarking rather than representative-sequence inference and error-rate assessment"
edam_operation: "http://edamontology.org/operation_0291"
edam_topics:
  - "http://edamontology.org/topic_3697"
tools:
  - name: "QIIME 2"
    role: "Framework (v2018.11) for importing reads, running denoising/clustering plugins, and applying feature-table filters"
  - name: "DADA2"
    role: "Default error-model denoiser inferring ASVs from trimmed reads; produced the fewest unexpected mock ASVs under basic filtering"
  - name: "Deblur"
    role: "Error-model denoiser run with --p-min-reads 2 and --p-min-size 1 so only singleton reads are discarded"
  - name: "VSEARCH"
    role: "OTU-clustering comparison pipeline: merge paired ends, dereplicate, cluster at 98% identity, de novo chimera filtering, final 97% clustering"
    repo: "https://github.com/torognes/vsearch"
  - name: "Cutadapt"
    role: "Trims primers/adapters from raw paired-end reads before denoising or clustering"
merged_aliases:
  - "amplicon-sequence-denoising-asv-inference"
  - "amplicon-denoising-pipeline-execution"
merged_alias_records:
  - {alias: "amplicon-sequence-denoising-asv-inference", slug: "amplicon-sequence-denoising-asv-inference", jaccard_score: 0.6, method: "token-set-jaccard", decision: "needs_review"}
  - {alias: "amplicon-denoising-pipeline-execution", slug: "amplicon-denoising-pipeline-execution", cosine_score: 0.8479, method: "embedding-cosine", decision: "needs_review"}
provenance:
  source_task_ids:
    - task_003
    - task_001
    - task_004
  source_papers:
    - doi: "10.1002/ece3.6594"
      title: "A total crapshoot? Evaluating bioinformatic decisions in animal diet metabarcoding analyses"
schema_version: "0.2.0"
content_hash: sha256:d7b0c2d7d358941372d2bea82c46c108c1d6f6cea00993aba31d53a22b2a8ec7
---

# amplicon-sequence-denoising

## Summary

Comparative amplicon sequence denoising versus clustering: infer representative sequence variants (ASVs) from trimmed COI paired-end reads with error-model denoisers (DADA2, Deblur) or VSEARCH OTU clustering, then benchmark unexpected-sequence (error) rates against a biological mock community to judge which pipeline and low-abundance filtering regime best controls spurious ASVs.

## When to use

Use when comparing DADA2/Deblur denoising against VSEARCH clustering on amplicon paired-end reads, or when deciding whether low-abundance filtering mitigates error-rate differences between ASV and OTU inference.

## When NOT to use

- Input is already a denoised feature table (this skill operates on raw/trimmed paired-end FASTQ reads)
- Data are amino-acid sequences or require local alignment — VSEARCH supports only nucleotide global alignments
- The goal is taxonomic classifier benchmarking rather than representative-sequence inference and error-rate assessment

## Inputs

- Raw paired-end amplicon FASTQ reads (COI metabarcoding, e.g. SRA PRJNA518082 mock community libraries A-D and bat guano samples)
- Expected mock community reference FASTA (from the tidybug GitHub repo)
- Trimmed reads retaining unmerged pairs with minimum length 175 bp (post-Cutadapt)

## Outputs

- Feature table and representative-sequence artifacts from DADA2, Deblur, and VSEARCH runs
- Per-library table of exact/partial/miss counts for each processing method (e.g. mock_error_rates.csv)
- Filtered feature tables under basic, standard, and extra filtering regimes

## How to apply

Import raw paired-end reads into QIIME 2 (v2018.11), trim primers/adapters with Cutadapt, and retain unmerged pairs with a minimum length of 175 bp. Run three representative-sequence pipelines on the same input: DADA2 with its default error-model denoising; Deblur with non-default parameters '--p-min-reads 2' and '--p-min-size 1' so only singleton reads are discarded; and VSEARCH OTU clustering (merge paired ends, dereplicate, cluster at 98% identity, de novo chimera filtering, then final clustering at 97% identity, mirroring the VSEARCH Wiki pipeline). Assess accuracy by aligning each mock-community representative sequence to the expected references with at least 97% coverage, labeling 100% identity matches 'exact', 97-99% matches 'partial', and <97% matches 'miss'. Apply a standard filter (drop sequence variants observed in only one sample; retain samples with >=5,000 filtered reads) and an extra filter (standard plus subtraction of the per-library maximum 'miss' variant count from every feature-table element) to test whether filtering mitigates method differences. The rationale, grounded in the article's finding, is that denoising methods have lower error rates than clustering under basic filtering, but removing low-abundance sequence variants largely mitigates those differences.

## Related tools

- **QIIME 2** (Framework (v2018.11) for importing reads, running denoising/clustering plugins, and applying feature-table filters)
- **DADA2** (Default error-model denoiser inferring ASVs from trimmed reads; produced the fewest unexpected mock ASVs under basic filtering)
- **Deblur** (Error-model denoiser run with --p-min-reads 2 and --p-min-size 1 so only singleton reads are discarded)
- **VSEARCH** (OTU-clustering comparison pipeline: merge paired ends, dereplicate, cluster at 98% identity, de novo chimera filtering, final 97% clustering) — https://github.com/torognes/vsearch
- **Cutadapt** (Trims primers/adapters from raw paired-end reads before denoising or clustering)

## Examples

```
qiime deblur denoise-16S --i-demultiplexed-seqs trimmed.qza --p-min-reads 2 --p-min-size 1 --o-table deblur_table.qza --o-representative-sequences deblur_reps.qza
```

## Evaluation signals

- Under the basic filter, DADA2 yields fewer partial mock ASVs (9) than Deblur (146) and VSEARCH (295), and fewer miss ASVs (40) than Deblur (576) and VSEARCH (753)
- DADA2 and Deblur recover all 24 expected mock sequences, while the VSEARCH clustering route misses between 1 and 4 of them
- Sequence matches to mock references require a minimum of 97% coverage, with 'exact' at 100% identity, 'partial' at 97-99%, and 'miss' below 97%
- After the standard filter (drop variants seen in one sample; >=5,000 filtered reads per sample) and the extra filter, error-rate differences among methods are largely mitigated
- On real (bat guano) data, VSEARCH-processed samples repeatedly contain 2-3x more ASVs per sample than DADA2 or Deblur, with significant Kruskal-Wallis differences in Hill-number alpha diversity across filtering regimes

## Limitations

- Software versions for the denoising programs are not reported in the results section, complicating exact reproduction
- VSEARCH does not support amino acid sequences or local alignments, so the clustering route is restricted to nucleotide global alignment workflows
- The article's aim is not to present a single best pathway but to illustrate how processes are affected by program or parameter choices; results depend on the 175 bp minimum-length retention and the specific filtering thresholds chosen

## Evidence

- [intro] Denoising programs like DADA2 (Callahan et al., 2016) or Deblur (Amir et al., 2017) generate error models to address potential sequence errors: "Denoising programs like DADA2 (Callahan et al., 2016) or Deblur (Amir et al., 2017) generate error models to address potential sequence errors"
- [methods] a standard filter required (a) dropping any sequence variant observed in just one sample across the entire dataset and (b) retaining only samples with ≥5,000 total filtered reads: "a standard filter required (a) dropping any sequence variant observed in just one sample across the entire dataset and (b) retaining only samples with ≥5,000 total filtered reads"
- [results] The choice of both denoising program and filtering can influence the number of mock ASVs observed in dataset: "The choice of both denoising program and filtering can influence the number of mock ASVs observed in dataset"
- [methods] mirrored the parameters outlined at the VSEARCH Wiki GitHub page (https://github.com/torognes/vsearch/wiki/VSEARCH-pipeline): [evidence span withheld — anchor status: not_found]
- [readme] VSEARCH does not support amino acid sequences or local alignments.: [evidence span withheld — anchor status: external_doc]
