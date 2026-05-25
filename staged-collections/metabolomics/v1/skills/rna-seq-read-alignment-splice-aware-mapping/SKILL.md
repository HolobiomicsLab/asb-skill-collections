---
name: rna-seq-read-alignment-splice-aware-mapping
description: Align paired-end RNA-seq reads to a reference genome using a splice-aware aligner (HISAT2) to generate sorted BAM files that preserve exon–intron boundaries. This is essential for accurately quantifying gene expression in organisms where spliced transcripts dominate.
when_to_use_negative:
- Input reads are single-end or already aligned (BAM/SAM files exist).
- The organism has no introns or a very simple, unspliced transcriptome (e.g., many prokaryotes).
- You only need to quantify pre-existing features and do not need to discover novel isoforms or splice variants.
edam_operation: http://edamontology.org/operation_3198
edam_topics:
- http://edamontology.org/topic_0203
- http://edamontology.org/topic_3170
tools:
- name: HISAT2
  role: Splice-aware short-read aligner; maps paired-end RNA-seq reads to reference genome with automatic exon–intron junction detection
- name: SRA Toolkit (fastq-dump or fasterq-dump)
  role: Download raw paired-end RNA-seq reads from NCBI Sequence Read Archive (e.g., BioProject PRJNA906931)
- name: HTSeq
  role: Counts reads mapping to annotated genes from BAM files; downstream step to generate raw count matrices for normalization
- name: Samtools
  role: Sorting and indexing BAM files for efficient random access and quality control
provenance:
  source_task_ids:
  - task_003
  source_papers:
  - doi: 10.1073/pnas
    title: Proceedings of the National Academy of Sciences
schema_version: 0.2.0
metadata:
  merge_audit:
    n_source_runs: 2
    source_files:
    - outputs/audit_jeong_full/skills/rna-seq-read-alignment-splice-aware-mapping/SKILL.md
    - outputs/audit_jeong_full/skills/rna-seq-read-alignment-splice-aware-mapping/skill.md
    merged_at: '2026-05-25T07:15:30.912142+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/rna-seq-read-alignment-splice-aware-mapping@sha256:642839479498337d59e061602e8f3a2251884eb146753b4cb57478961247f3af
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1073/pnas
---

# RNA-seq read alignment with splice-aware mapping

## Summary

Align paired-end RNA-seq reads to a reference genome using a splice-aware aligner (HISAT2) to generate sorted BAM files that preserve exon–intron boundaries. This is essential for accurately quantifying gene expression in organisms where spliced transcripts dominate.

## When to use

You have raw paired-end RNA-seq FASTQ reads from cultured organisms (e.g., fungi, plants) and a reference genome assembly with gene annotations, and you need to map reads to genes while respecting splice sites to prepare for downstream read counting and expression normalization (e.g., RPKM or TMM).

## When NOT to use

- Input reads are single-end or already aligned (BAM/SAM files exist).
- The organism has no introns or a very simple, unspliced transcriptome (e.g., many prokaryotes).
- You only need to quantify pre-existing features and do not need to discover novel isoforms or splice variants.

## Inputs

- Paired-end RNA-seq FASTQ files (raw reads from NCBI SRA or equivalent)
- Reference genome sequence (FASTA)
- Gene annotation file (GTF or GFF, optional but recommended for index construction)

## Outputs

- HISAT2 reference index (directory of .ht2 files)
- Coordinate-sorted BAM files (one per sample, e.g., baicalin-treated and control)
- Alignment summary statistics (number of mapped/unmapped reads)

## How to apply

First, build a HISAT2 reference index from the target organism's genome sequence. Then align the paired-end FASTQ reads to this index using HISAT2 with default splice-aware parameters, which automatically detects and correctly maps reads spanning exon–intron junctions. The output BAM files should be coordinate-sorted to facilitate downstream read counting. HISAT2's splice-aware approach is critical for fungal and plant transcriptomes where alternative splicing and complex gene structures are common; this ensures that reads mapping across splice junctions are not discarded as unmapped. The resulting sorted BAM files serve as input to read-counting tools (e.g., HTSeq) and are validated by checking alignment rates and coverage metrics.

## Related tools

- **HISAT2** (Splice-aware short-read aligner; maps paired-end RNA-seq reads to reference genome with automatic exon–intron junction detection)
- **SRA Toolkit (fastq-dump or fasterq-dump)** (Download raw paired-end RNA-seq reads from NCBI Sequence Read Archive (e.g., BioProject PRJNA906931))
- **HTSeq** (Counts reads mapping to annotated genes from BAM files; downstream step to generate raw count matrices for normalization)
- **Samtools** (Sorting and indexing BAM files for efficient random access and quality control)

## Examples

```
hisat2-build L_brumalis_genome.fasta L_brumalis_index && hisat2 -x L_brumalis_index -1 baicalin_R1.fastq -2 baicalin_R2.fastq | samtools sort -o baicalin_sorted.bam
```

## Evaluation signals

- Alignment rate ≥80% of reads mapped to the reference genome (reported in HISAT2 summary statistics).
- BAM files are coordinate-sorted and indexed; samtools view and samtools idxstats run without error.
- Coverage and read count per gene are consistent with expected biology (e.g., highly expressed genes show higher read counts; baicalin-treatment should increase expression of target genes like LbUGT3).
- Splice junction metrics: verify that HISAT2 reports ≥50% of reads mapping across introns in known splice sites (expected for eukaryotic RNA-seq).
- BAM header and @PG tags correctly document the HISAT2 version and command parameters used.

## Limitations

- HISAT2 requires a reference genome and gene annotation; performance degrades for organisms with highly fragmented assemblies or incomplete annotations.
- Default splice-aware parameters may over-correct for organisms with unusual codon usage or RNA secondary structures; custom parameters may be needed.
- Paired-end read length and insert size distribution affect mapping; very short reads (<50 bp) or highly variable insert sizes can reduce splice-junction recovery.
- Multimapped reads (e.g., reads mapping equally well to multiple genomic loci or paralogs) are reported but typically discarded in downstream counting; this can undercount genes in highly duplicated regions (e.g., gene families).
- HISAT2 does not assign reads to isoforms; isoform-level quantification requires additional tools (e.g., Salmon, RSEM) or manual transcript assembly.

## Evidence

- [methods] Build HISAT2 reference index and align reads: "Build HISAT2 reference index from the L. brumalis genome sequence. 3. Align reads to reference genome using HISAT2 with default splice-aware parameters, generating sorted BAM files for"
- [methods] Download raw paired-end reads from SRA: "Download raw paired-end RNA-seq reads from NCBI Sequence Read Archive under BioProject PRJNA906931 using SRA Toolkit (fastq-dump or fasterq-dump)."
- [methods] HTSeq downstream quantification: "Count reads mapping to annotated genes using HTSeq (mode=union, stranded=reverse) to produce raw count matrices."
- [results] Verification by expression increase: "the expression level of LbUGT3 showed two-fold increase in the growth media containing 1"
- [discussion] Availability of code and data: "Raw sequence reads acquired from the RNAseq analysis have been deposited at NCBI Sequence Read Archive under BioProject PRJNA906931"
