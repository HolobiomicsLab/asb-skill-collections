---
name: post-translational-modification-pattern-recognition
description: Use when you have centroided LC-MS/MS spectra (in MGF, mzXML, mzML, or mzData format) and genomically-predicted precursor peptide sequences, and you need to identify which predicted RiPPs are actually expressed and modified in the sample.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3645
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0080
  tools:
  - NPDtools 2.5.0
  - MetaMiner
  - antiSMASH
  - Dereplicator
  - BOA
  - ProteoWizard msconvert
derived_from:
- doi: 10.1038/s41467-018-06082-8
  title: dereplicator
evidence_spans:
- The latest version is available in the Natural Product Discovery toolkit (NPDtools) at https://github.com/ablab/npdtools
- MetaMiner is a metabologenomic pipeline which integrates metabolomic (tandem mass spectra) and genomic data to identify novel RiPPs
- MetaMiner is a metabologenomic pipeline which integrates metabolomic (tandem mass spectra) and genomic data to identify novel Ribosmally synthesized and Post-translationally modified Peptides (RiPPs)
- 'MetaMiner uses either raw nucleotide sequences or specific genome mining tools'' output: raw nucleotide sequences `.fasta` format or *antiSMASH*''s `.final.gbk` or `.gbk` file'
- matches tandem mass spectra against the constructed post-translationally modified RiPPs structure database using Dereplicator
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_dereplicator
    doi: 10.1038/s41467-018-06082-8
    title: dereplicator
  dedup_kept_from: coll_dereplicator
schema_version: 0.2.0
---

# post-translational-modification-pattern-recognition

## Summary

Identify and validate post-translationally modified peptide structures by matching tandem mass spectra against constructed RiPP structure databases that encode known and predicted PTM variants. This skill is essential for discovering ribosomally synthesized and post-translationally modified peptides (RiPPs) where spectral signatures reflect specific chemical modifications like cyclization, oxidation, and epimerization.

## When to use

Apply this skill when you have centroided LC-MS/MS spectra (in MGF, mzXML, mzML, or mzData format) and genomically-predicted precursor peptide sequences, and you need to identify which predicted RiPPs are actually expressed and modified in the sample. Specifically useful when screening for known RiPP families (e.g., lantibiotics, lasso peptides) where PTM patterns are conserved but sequence context varies.

## When NOT to use

- Input is uncentroided or profile-mode mass spectrometry data; convert or recalibrate first.
- No corresponding genomic data or BGCs are available; the skill requires sequence context to propose PTM patterns.
- RiPP class has no established biosynthetic pathway or PTM rules; the database construction step will fail without a defined modification grammar.

## Inputs

- centroided tandem mass spectrometry data (MGF, mzXML, mzML, or mzData format)
- genome sequence files (FASTA) or antiSMASH .final.gbk / .gbk genome mining tool output
- BGC annotations identifying precursor peptides and their biosynthetic genes

## Outputs

- matched RiPP identifications with inferred PTM patterns (significant_matches.tsv format)
- scored spectral matches annotated with PTM site assignments and modification types
- spectral networks (text or graphical) showing cosine similarity relationships between spectra of PTM variants

## How to apply

First, construct a database of putative RiPP structures by identifying biosynthetic gene clusters (BGCs) from assembled genomes (using tools like antiSMASH or BOA) and extracting precursor peptide sequences; this database must encode plausible post-translational modifications (cyclization, dehydration, oxidation, epimerization, etc.) for the RiPP class being investigated. Second, convert all input spectra to MGF format if needed using ProteoWizard's msconvert. Third, run Dereplicator to match the experimental tandem mass spectra against the PTM-encoded RiPP structure database, which scores each match based on how well the observed fragmentation pattern aligns with the theoretical spectrum of a modified peptide. Finally, inspect the ranked matches (typically reported in significant_matches.tsv) and validate the top candidates by confirming that the inferred PTM pattern (e.g., specific cyclization sites, oxidized residues) is consistent with the biosynthetic pathway predicted from the corresponding BGC.

## Related tools

- **MetaMiner** (Core metabologenomics pipeline integrating genomic and mass spectrometric data to identify RiPPs by matching spectra against PTM-encoded precursor databases) — https://github.com/mohimanilab/MetaMiner
- **Dereplicator** (Performs spectral database matching of tandem MS data against constructed RiPP structure database; scores PTM pattern consistency with observed fragmentation) — https://github.com/ablab/npdtools
- **antiSMASH** (Identifies biosynthetic gene clusters and predicts precursor peptides from genome sequences; output (.final.gbk) serves as input for PTM-aware RiPP database construction)
- **BOA** (Alternative BGC mining tool for genome-based identification of bacteriocin and other RiPP gene clusters; generates annotated region predictions for precursor extraction) — https://github.com/idoerg/BOA
- **ProteoWizard msconvert** (Converts mass spectrometry data in formats other than MGF/mzXML/mzML/mzData to MGF for compatibility with Dereplicator and MetaMiner)

## Examples

```
python metaminer.py test_data/metaminer/msms/ -s test_data/metaminer/fasta/ -o metaminer_outdir
```

## Evaluation signals

- Matched RiPP peptide sequence appears in significant_matches.tsv with a score / E-value consistent with high-confidence identifications reported in the literature for the same RiPP family.
- Inferred PTM pattern (e.g., cyclization sites, dehydrated residues, oxidations) aligns with the known modification motif of the predicted RiPP class and the biosynthetic pathway genes present in the corresponding BGC.
- Spectral network analysis shows cosine similarity clustering: the identified RiPP spectrum clusters with related PTM variants at expected similarity thresholds, indicating the match is robust to minor modifications.
- Cross-validation: the same RiPP is detected when the same genome sequence is provided in alternative formats (e.g., contigs.fasta vs. antiSMASH .gbk) to rule out input-format parsing artifacts.
- Manual inspection of fragment ion assignment confirms that major peaks in the experimental spectrum correspond to theoretical b-ions and y-ions predicted from the PTM-annotated RiPP sequence.

## Limitations

- Input format sensitivity: MetaMiner successfully detects RiPPs with FASTA sequence input but may fail with antiSMASH .final.gbk output for the same organism and spectra, indicating that genome mining tool output parsing is error-prone and format-dependent validation is required.
- Database completeness: the skill depends on accurate prediction of precursor peptides and PTM rules from BGCs; missing or mis-annotated biosynthetic genes will generate incomplete or incorrect RiPP structure databases, reducing detection sensitivity.
- Spectral quality: low-resolution or noisy tandem MS spectra may not provide sufficient fragmentation detail to distinguish between isomeric PTM patterns (e.g., different cyclization sites), leading to ambiguous or false-positive matches.
- No changelog or versioning metadata available for the NPDtools toolkit, making it difficult to trace which specific PTM patterns or scoring functions are active in a given release.

## Evidence

- [readme] MetaMiner (i) identifies putative BGCs and the corresponding precursor peptides, (ii) constructs putative RiPP structure databases, (iii) matches tandem mass spectra against the constructed post-translationally modified RiPPs structure database using Dereplicator: "MetaMiner (i) identifies putative BGCs and the corresponding precursor peptides, (ii) constructs putative RiPP structure databases, (iii) matches tandem mass spectra against the constructed"
- [methods] MetaMiner successfully detects AmfS using contigs.fasta input but fails when antiSMASH output is used as input, demonstrating input format-dependent detection differences.: "While `MetaMiner` successfully detect AmfS using the `contigs.fasta` file, it fails with antiSMASH result as input"
- [readme] spectra files must be centroided and be in an open spectrum format (MGF, mzXML, mzML or mzData): "Spectra files must be centroided and be in an open spectrum format (**MGF**, **mzXML**, **mzML** or **mzData**)"
- [readme] MetaMiner uses either raw nucleotide sequences or specific genome mining tools' output: raw nucleotide sequences `.fasta` format or *antiSMASH*'s `.final.gbk` or `.gbk` file: "MetaMiner uses either raw nucleotide sequences or specific genome mining tools' output: raw nucleotide sequences `.fasta` format or *antiSMASH*'s `.final.gbk` or `.gbk` file"
