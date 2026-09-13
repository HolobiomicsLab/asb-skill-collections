---
name: mass-spectrum-database-matching
description: Use when you have centroided LC-MS/MS spectral data (in MGF, mzXML, mzML,
  or mzData format) and want to identify known or predicted natural product structures
  present in your sample.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - NPDtools 2.5.0
  - MetaMiner
  - antiSMASH
  - Dereplicator
  - ProteoWizard
  - NPDtools
  - joblib
  - VarQuest
  - RapidMass
  - DI-MS
  - ASAP-MS
  techniques:
  - LC-MS
  - direct-infusion-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41467-018-06082-8
  title: dereplicator
- doi: 10.1021/acs.analchem.4c05062
  title: ''
evidence_spans:
- The latest version is available in the Natural Product Discovery toolkit (NPDtools)
  at https://github.com/ablab/npdtools
- MetaMiner is a metabologenomic pipeline which integrates metabolomic (tandem mass
  spectra) and genomic data to identify novel RiPPs
- MetaMiner is a metabologenomic pipeline which integrates metabolomic (tandem mass
  spectra) and genomic data to identify novel Ribosmally synthesized and Post-translationally
  modified Peptides (RiPPs)
- 'MetaMiner uses either raw nucleotide sequences or specific genome mining tools''
  output: raw nucleotide sequences `.fasta` format or *antiSMASH*''s `.final.gbk`
  or `.gbk` file'
- matches tandem mass spectra against the constructed post-translationally modified
  RiPPs structure database using Dereplicator
- MetaMiner natively supports MGF, mzXML, mzData and uses msconvert utility from the
  ProteoWizard package to convert spectra in other formats to MGF
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_dereplicator
    doi: 10.1038/s41467-018-06082-8
    title: dereplicator
  - build: coll_rapidmass_cq
    doi: 10.1021/acs.analchem.4c05062
    title: RapidMass
  dedup_kept_from: coll_dereplicator
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-018-06082-8
  all_source_dois:
  - 10.1038/s41467-018-06082-8
  - 10.1021/acs.analchem.4c05062
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrum-database-matching

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Match tandem mass spectra against structure databases of known natural products to identify peptidic natural products (PNPs) and ribosomally synthesized post-translationally modified peptides (RiPPs). This skill uses database search pipelines like Dereplicator to return scored identifications with annotated modifications.

## When to use

You have centroided LC-MS/MS spectral data (in MGF, mzXML, mzML, or mzData format) and want to identify known or predicted natural product structures present in your sample. Apply this skill when you need to match observed fragmentation patterns against a reference database of peptidic natural products or RiPP structures to obtain compound identifications with modification annotations.

## When NOT to use

- Your input spectra are not centroided (Dereplicator requires centroided data)
- You are performing de novo peptide sequencing without a reference database — use modification-tolerant search tools (e.g., VarQuest) instead
- Your input sequences are already genome-mined biosynthetic gene clusters in GenBank format — use MetaMiner with raw nucleotide FASTA sequences or antiSMASH .final.gbk output for metabologenomic integration

## Inputs

- Centroided LC-MS/MS spectral files (MGF, mzXML, mzML, or mzData format)
- RiPP class specification (e.g., 'lantibiotic')
- Optional: reference chemical structure database of known natural products

## Outputs

- significant_matches.tsv file containing compound identifications
- FragmentSeq and ModifiedSeq annotations for matched RiPPs
- Scoring metrics for each match

## How to apply

Prepare centroided spectra in MGF format (or use msconvert from ProteoWizard to convert mzML/mzXML/mzData to MGF if needed). Run the Dereplicator pipeline from NPDtools, specifying the spectral directory or files and the target RiPP class (e.g., lantibiotic). Dereplicator constructs a post-translationally modified RiPP structure database and matches observed spectra against it using scoring. Parse the resulting significant_matches.tsv output file, examining the FragmentSeq column for core peptide sequence matches and ModifiedSeq column for post-translational modifications (indicated by mass shifts such as T-18 or S-18 for dehydrobutyrine/dehydroalanine). Verify identifications by checking that matched compounds appear in the output table with appropriate scoring thresholds applied by the tool.

## Related tools

- **Dereplicator** (Primary database search pipeline that matches tandem mass spectra against post-translationally modified RiPP structure databases) — https://github.com/ablab/npdtools
- **ProteoWizard** (Spectral format conversion utility (msconvert) used to convert mzML, mzXML, mzData to MGF format for Dereplicator input)
- **VarQuest** (Modification-tolerant variant database search tool for identifying novel RiPP variants when reference structures are incomplete) — https://github.com/ablab/npdtools
- **MetaMiner** (Metabologenomic pipeline that constructs RiPP structure databases from genomic input and integrates with Dereplicator for matching) — https://github.com/mohimanilab/MetaMiner

## Examples

```
python dereplicator.py test_data/metaminer/msms/ -c lantibiotic -o dereplicator_outdir
```

## Evaluation signals

- Output file significant_matches.tsv is generated and contains rows corresponding to identified compounds
- FragmentSeq column contains matched core peptide sequences (e.g., 'TGSQVSLLVCEYSSLSVVLCTP' for AmfS) that align with expected RiPP structures
- ModifiedSeq column shows post-translational modifications with appropriate mass shifts (e.g., T-18, S-18 for dehydration products)
- Scoring metrics for matches meet tool-specific significance thresholds (tool applies default scoring automatically)
- Identified compounds can be cross-referenced against known natural product databases or biosynthetic gene clusters from input organisms

## Limitations

- Dereplicator requires centroided spectra; high-resolution profile-mode data must be centroided before input, or msconvert must be run with centroiding enabled
- Database search only identifies compounds present in or similar to the reference RiPP structure database; novel structures or highly divergent variants may not be detected
- Spectral data must be in supported formats (MGF, mzXML, mzML, mzData); other formats require preprocessing via ProteoWizard msconvert
- MetaMiner successfully detects RiPPs using raw nucleotide sequence FASTA input but fails when antiSMASH .final.gbk output is used as input, indicating format-dependent detection differences that can lead to missed identifications

## Evidence

- [methods] matches tandem mass spectra against the constructed post-translationally modified RiPPs structure database using Dereplicator: "matches tandem mass spectra against the constructed post-translationally modified RiPPs structure database using Dereplicator"
- [readme] NPDtools natively supports MGF, mzXML, mzData and uses msconvert utility from the ProteoWizard package to convert spectra in other formats to MGF: "NPDtools natively supports MGF, mzXML, mzData and uses msconvert utility from the ProteoWizard package to convert spectra in other formats to MGF"
- [methods] Parse the tab-separated significant_matches.tsv output file to extract compound identifications, verifying presence of AmfS by FragmentSeq column matching 'TGSQVSLLVCEYSSLSVVLCTP' and ModifiedSeq showing dehydrobutyrine/dehydroalanine modifications (T-18 and S-18 mass shifts).: "Parse the tab-separated significant_matches.tsv output file to extract compound identifications, verifying presence of AmfS by FragmentSeq column matching 'TGSQVSLLVCEYSSLSVVLCTP' and ModifiedSeq"
- [readme] All pipelines in NPDtools work with liquid chromatography–tandem mass spectrometry data (LS-MS/MS). Spectra files must be centroided and be in an open spectrum format (**MGF**, **mzXML**, **mzML** or **mzData**).: "All pipelines in NPDtools work with liquid chromatography–tandem mass spectrometry data (LS-MS/MS). Spectra files must be centroided and be in an open spectrum format (**MGF**, **mzXML**, **mzML** or"
- [methods] While `MetaMiner` successfully detect AmfS using the `contigs.fasta` file, it fails with antiSMASH result as input: "While `MetaMiner` successfully detect AmfS using the `contigs.fasta` file, it fails with antiSMASH result as input"
