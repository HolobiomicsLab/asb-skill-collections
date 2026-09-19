---
name: 16s-amplicon-alignment-to-reference
description: "Aligns full-length (~1500 bp) 16S rRNA amplicon reads (e.g., PacBio CCS from human stool) to a reference 16S gene with Cross_match to tabulate per-position nucleotide substitution profiles that resolve intragenomic 16S gene copy variants at species/strain level."
when_to_use_negative:
  - "The goal is to resolve insertions/deletions between intragenomic 16S copies — PacBio CCS deletion errors coincident with homopolymer runs make indel calls unreliable"
  - "Only short-read sequencing of 16S variable regions (e.g., V4) is available, since it cannot achieve the taxonomic resolution of the full ~1500 bp gene"
  - "The OTU clustering threshold of 99% identity is known not to separate intragenomic from inter-genomic variation for the species of interest"
edam_operation: "http://edamontology.org/operation_0292"
edam_topics:
  - "http://edamontology.org/topic_0632"
  - "http://edamontology.org/topic_3174"
tools:
  - name: "PacBio"
    role: "Long-read sequencing platform generating full-length 16S amplicon reads accurate enough to resolve nucleotide substitutions between intragenomic 16S copies"
  - name: "Cross_match"
    role: "Aligner used to align B. vulgatus OTU amplicons from both samples to the reference 16S gene for substitution tabulation"
  - name: "ruffus"
    role: "Python pipeline framework used to organize the figure-specific analysis pipelines in the source repository"
    repo: "https://github.com/cgat-developers/ruffus"
provenance:
  source_task_ids:
    - task_007
  source_papers:
    - doi: "10.1038/s41467-019-13036-1"
      title: "Evaluation of 16S rRNA gene sequencing for species and strain-level microbiome analysis"
schema_version: "0.2.0"
content_hash: sha256:54fb2e046e95e56c2373028eee82dc2d35e4ed685513abcb07037847471b8299
---

# 16s-amplicon-alignment-to-reference

## Summary

Aligns full-length (~1500 bp) 16S rRNA amplicon reads (e.g., PacBio CCS from human stool) to a reference 16S gene with Cross_match to tabulate per-position nucleotide substitution profiles that resolve intragenomic 16S gene copy variants at species/strain level.

## When to use

Use when full-length 16S amplicon reads from a long-read platform (PacBio/Nanopore) must be aligned to a reference 16S gene to detect intragenomic polymorphisms or derive strain-level substitution profiles in a microbiome sample.

## When NOT to use

- The goal is to resolve insertions/deletions between intragenomic 16S copies — PacBio CCS deletion errors coincident with homopolymer runs make indel calls unreliable
- Only short-read sequencing of 16S variable regions (e.g., V4) is available, since it cannot achieve the taxonomic resolution of the full ~1500 bp gene
- The OTU clustering threshold of 99% identity is known not to separate intragenomic from inter-genomic variation for the species of interest

## Inputs

- Full-length PacBio CCS 16S amplicon reads (e.g., Scott and IronHorse stool samples)
- Reads assigned to a 99% identity 16S OTU for the target taxon
- Reference 16S gene sequence for the target species (single copy)
- RefSeq 16S sequences for related strains (e.g., B. vulgatus ATCC 8482 and mpk40)

## Outputs

- Per-position nucleotide substitution profiles by sample and reference strain (substitution_profiles.csv)
- Fraction of reads carrying each polymorphism (e.g., V5 polymorphism frequency per sample)

## How to apply

Retrieve full-length PacBio 16S amplicon reads (e.g., Scott and IronHorse stool samples from github.com/TheJacksonLaboratory/weinstock_full_length_16s) and select reads assigned to the target 99%-identity OTU (e.g., B. vulgatus). Load the single-species reference 16S gene plus RefSeq 16S sequences for known strains (e.g., ATCC 8482 and mpk40). Align the OTU amplicons to the reference gene with Cross_match. Tabulate nucleotide substitutions per aligned position, deliberately ignoring insertions and deletions because systematic PacBio CCS deletion errors coincide with homopolymer runs and make indel calls unreliable. Compute per-position substitution frequencies and compare against RefSeq-predicted profiles (e.g., a polymorphism in three of seven 16S copies of ATCC 8482 detected at 84% in Scott and 69% in IronHorse, matching six and five of seven copies), writing results organized by sample and reference strain to substitution_profiles.csv.

## Related tools

- **PacBio** (Long-read sequencing platform generating full-length 16S amplicon reads accurate enough to resolve nucleotide substitutions between intragenomic 16S copies)
- **Cross_match** (Aligner used to align B. vulgatus OTU amplicons from both samples to the reference 16S gene for substitution tabulation)
- **ruffus** (Python pipeline framework used to organize the figure-specific analysis pipelines in the source repository) — https://github.com/cgat-developers/ruffus

## Evaluation signals

- Computed V5 polymorphism frequencies match reported values: 84% in the Scott sample and 69% in the IronHorse sample
- Per-position substitution profiles reproduce the patterns shown in Fig. 3c and 3d of Johnson et al. 2019
- Substitution profiles are consistent with RefSeq-predicted copy-number expectations (e.g., 6/7 and 5/7 of seven 16S gene copies)
- Insertions and deletions are excluded from the tabulation, with only substitutions contributing to the profiles

## Limitations

- Systematic PacBio CCS deletion errors coincident with homopolymer runs limit the ability to resolve highly similar sequences and force indels to be ignored
- Ignoring insertions/deletions is imperfect: a single deletion in one of the seven E. coli K-12 MG1655 16S genes demonstrates this
- Systematic errors may occur at a fixed frequency and may not be improved by greater sequencing effort
- The 99% identity OTU threshold was not validated for separating intragenomic vs. inter-genomic variation across all bacterial species

## Evidence

- [discussion] focusing on substitutions and ignoring the contribution of insertions and deletions: "we chose to overcome such platform-specific errors by focusing on substitutions and ignoring the contribution of insertions and deletions to intragenomic 16S gene copy polymorphisms"
- [results] a polymorphism present in three 16S copies (43%) of strain ATCC 8482 was detected at 84% frequency in the Scott sample and 69% in the IronHorse sample: [evidence span withheld — anchor status: not_found]
- [readme] Code is organised into a set of ruffus pipelines pertaining to different figures.: "Code is organised into a set of [ruffus](http://www.ruffus.org.uk/) pipelines pertaining to different figures."
- [discussion] full-length 16S gene sequences clustered at 99% identity provided reasonable estimates of Bacteroides species relative abundance: "full-length 16S gene sequences clustered at 99% identity provided reasonable estimates of Bacteroides species relative abundance"
