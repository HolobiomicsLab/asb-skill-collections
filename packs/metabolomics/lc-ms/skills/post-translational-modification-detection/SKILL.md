---
name: post-translational-modification-detection
description: Use when when you have tandem mass spectrometry data (LC-MS/MS in MGF, mzML, mzXML, or mzData format) paired with either genome sequences or precursor peptide predictions, and you want to confirm the presence and identity of modified ribosomally synthesized and post-translationally modified.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3365
  tools:
  - NPDtools 2.5.0
  - MetaMiner
  - Dereplicator
  - ProteoWizard
  - NPDtools
  - joblib
  - Python
  - antiSMASH
  - BOA
  techniques:
  - LC-MS
derived_from:
- doi: 10.1038/s41467-018-06082-8
  title: dereplicator
evidence_spans:
- The latest version is available in the Natural Product Discovery toolkit (NPDtools) at https://github.com/ablab/npdtools
- MetaMiner is a metabologenomic pipeline which integrates metabolomic (tandem mass spectra) and genomic data to identify novel RiPPs
- MetaMiner is a metabologenomic pipeline which integrates metabolomic (tandem mass spectra) and genomic data to identify novel Ribosmally synthesized and Post-translationally modified Peptides (RiPPs)
- matches tandem mass spectra against the constructed post-translationally modified RiPPs structure database using Dereplicator
- MetaMiner natively supports MGF, mzXML, mzData and uses msconvert utility from the ProteoWizard package to convert spectra in other formats to MGF
- uses msconvert utility from the ProteoWizard package to convert spectra in other formats to MGF
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-018-06082-8
  all_source_dois:
  - 10.1038/s41467-018-06082-8
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# post-translational-modification-detection

## Summary

Identifies and validates post-translational modifications (PTMs) on peptides by matching experimental tandem mass spectra against databases of putative modified RiPP structures, with class-specific modification rules applied during database construction. This skill bridges metabologenomic data (genome-predicted precursor peptides with enumerated PTM variants) and mass spectrometry evidence (fragmentation patterns).

## When to use

When you have tandem mass spectrometry data (LC-MS/MS in MGF, mzML, mzXML, or mzData format) paired with either genome sequences or precursor peptide predictions, and you want to confirm the presence and identity of modified ribosomally synthesized and post-translationally modified peptides (RiPPs) such as lantibiotics, lassopeptides, or cyanobactins. Specifically apply this skill after genome-based BGC identification has generated candidate precursor peptide sequences and their putative PTM variants.

## When NOT to use

- Input spectra are in profile (non-centroided) mode—centroiding is a preprocessing requirement not handled by MetaMiner/Dereplicator
- Searching non-peptidic natural products or metabolites without ribosomally synthesized origins—use Dereplicator+ instead for general metabolite identification
- Genome input is from antiSMASH .final.gbk or .gbk output files without fallback to raw contigs.fasta, as documented failures show antiSMASH format does not reliably produce PTM detections for known compounds like AmfS

## Inputs

- Tandem mass spectrometry files (MGF, mzML, mzXML, or mzData format)
- Genome FASTA nucleotide sequences or extracted precursor peptide sequences
- RiPP class specification (lantibiotic, lassopeptide, cyanobactin, or other)
- Optional: antiSMASH genome mining output or BOA annotated gene files

## Outputs

- Tab-separated significant_matches.tsv file with columns: scan identifier, match score, p-value, false discovery rate, FragmentSeq (core peptide), ModifiedSeq (with PTM mass shifts)
- RiPP structure database (intermediate TSV or FASTA format with enumerated PTM variants)
- Identified RiPP compound list with confirmed PTM patterns

## How to apply

First, construct a RiPP structure database by applying class-specific modification rules (e.g., dehydrobutyrine and dehydroalanine T-18 and S-18 mass shifts for lantibiotics) to enumerate all putative post-translationally modified variants of identified precursor peptides. Convert spectral input files to MGF format if needed using ProteoWizard msconvert. Then execute Dereplicator to match experimental spectra against the constructed database, scoring matches and recording significant identifications. Parse the output tab-separated results file (significant_matches.tsv) to extract compound identifications and verify presence of target modified peptides by checking the ModifiedSeq column for expected mass shifts and the FragmentSeq column for the core peptide sequence. The rational relies on the observation that raw nucleotide FASTA input enables PTM detection better than pre-processed genome mining tool output (e.g., antiSMASH .gbk files), likely because sequence parsing and precursor extraction is more reliable from unformatted contigs.

## Related tools

- **MetaMiner** (Metabologenomic pipeline that identifies putative BGCs and precursor peptides from genome FASTA, constructs RiPP structure databases with class-specific PTM enumeration, and coordinates spectral matching) — https://github.com/mohimanilab/MetaMiner
- **Dereplicator** (Matches tandem mass spectra against the constructed post-translationally modified RiPPs structure database and scores significant matches) — https://github.com/ablab/npdtools
- **ProteoWizard** (Converts mass spectrometry data in non-native formats (e.g., raw instrument formats) to MGF via msconvert utility for compatibility with NPDtools pipelines)
- **antiSMASH** (Alternative genome mining tool for BGC annotation; produces .final.gbk or .gbk output that can be input to MetaMiner, though raw FASTA sequences are preferred for PTM detection)
- **BOA** (Alternative bacterial gene cluster annotation tool producing .annotated.txt files as optional input to MetaMiner) — https://github.com/idoerg/BOA

## Examples

```
python metaminer.py test_data/metaminer/msms/ -s test_data/metaminer/fasta/ -c lantibiotic -o metaminer_outdir
```

## Evaluation signals

- Presence of expected core peptide sequence in FragmentSeq column (e.g., 'TGSQVSLLVCEYSSLSVVLCTP' for AmfS lantibiotic)
- ModifiedSeq column shows class-appropriate PTM mass shifts (e.g., T-18 and S-18 for dehydrobutyrine and dehydroalanine in lantibiotics)
- Significant match p-value or score threshold is met (tool-dependent; Dereplicator reports p-values and false discovery rates)
- Match is reported in significant_matches.tsv (not filtered out as below threshold)
- Input format consistency: raw nucleotide FASTA (not antiSMASH .gbk) yields higher detection sensitivity for known RiPPs

## Limitations

- MetaMiner fails to detect known RiPPs when antiSMASH .final.gbk or .gbk files are used as input; raw nucleotide contigs.fasta must be supplied instead
- PTM enumeration is class-specific; the pipeline must know the target RiPP class (lantibiotic, lassopeptide, cyanobactin) a priori to apply correct modification rules
- Requires Python 2.6–2.7 or 3.3+ and joblib for parallel processing; older or missing dependencies may degrade performance
- Spectral input files must be centroided; profile-mode spectra will not be processed correctly
- Spectral networking and visualization require optional matplotlib and networkx libraries; without them, propagation graphs are generated in plain text only

## Evidence

- [methods] MetaMiner successfully detects AmfS using contigs.fasta genome files, though it fails when using antiSMASH results as input, indicating that raw nucleotide sequence format supports lantibiotic discovery.: "While `MetaMiner` successfully detect AmfS using the `contigs.fasta` file, it fails with antiSMASH result as input"
- [methods] MetaMiner constructs putative RiPP structure databases by applying class-specific modification rules to enumerate post-translationally modified variants.: "For each identified precursor peptide, apply the RiPP Structure Database Builder to enumerate putative post-translationally modified variants according to class-specific modification rules."
- [methods] Verification of PTM detection relies on checking the ModifiedSeq column for expected mass shifts (T-18 and S-18) and the FragmentSeq column for the core peptide sequence.: "verifying presence of AmfS by FragmentSeq column matching 'TGSQVSLLVCEYSSLSVVLCTP' and ModifiedSeq showing dehydrobutyrine/dehydroalanine modifications (T-18 and S-18 mass shifts)"
- [readme] NPDtools natively supports MGF, mzXML, mzData and uses msconvert utility from the ProteoWizard package to convert spectra in other formats to MGF.: "MetaMiner natively supports MGF, mzXML, mzData and uses msconvert utility from the ProteoWizard package to convert spectra in other formats to MGF"
- [readme] Dereplicator matches tandem mass spectra against the constructed post-translationally modified RiPPs structure database.: "matches tandem mass spectra against the constructed post-translationally modified RiPPs structure database using Dereplicator"
