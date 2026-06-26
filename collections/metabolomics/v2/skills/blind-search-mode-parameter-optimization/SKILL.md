---
name: blind-search-mode-parameter-optimization
description: Use when when you have tandem mass spectra from ribosomally synthesized
  peptides (RiPPs) and suspect the presence of unknown or non-standard post-translational
  modifications that would be missed by standard database search modes constrained
  to known modification classes.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - NPDtools 2.5.0
  - MetaMiner
  - Dereplicator
  - ProteoWizard
  - Python
  - ProteoWizard msconvert
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41467-018-06082-8
  title: dereplicator
evidence_spans:
- The latest version is available in the Natural Product Discovery toolkit (NPDtools)
  at https://github.com/ablab/npdtools
- MetaMiner is a metabologenomic pipeline which integrates metabolomic (tandem mass
  spectra) and genomic data to identify novel RiPPs
- MetaMiner is a metabologenomic pipeline which integrates metabolomic (tandem mass
  spectra) and genomic data to identify novel Ribosmally synthesized and Post-translationally
  modified Peptides (RiPPs)
- matches tandem mass spectra against the constructed post-translationally modified
  RiPPs structure database using Dereplicator
- MetaMiner natively supports MGF, mzXML, mzData and uses msconvert utility from the
  ProteoWizard package to convert spectra in other formats to MGF
- uses msconvert utility from the ProteoWizard package to convert spectra in other
  formats to MGF
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# blind-search-mode-parameter-optimization

## Summary

A mode of natural product database search that relaxes structural constraints to identify peptides with arbitrary post-translational modifications (PTMs) without prior knowledge of modification types. This skill is essential when screening for novel RiPP variants that fall outside the scope of curated PTM databases.

## When to use

When you have tandem mass spectra from ribosomally synthesized peptides (RiPPs) and suspect the presence of unknown or non-standard post-translational modifications that would be missed by standard database search modes constrained to known modification classes. Apply this when initial targeted searches (e.g., MetaMiner with default lantibiotic class) yield incomplete hit coverage or when exploring spectral regions with unidentified high-confidence peaks.

## When NOT to use

- Input spectra are from non-peptidic natural products or metabolites outside the RiPP class — use Dereplicator+ instead for general metabolite identification.
- The modification landscape is well-characterized and constrained to known PTM types (e.g., standard lanthipeptides) — standard (non-blind) mode is more computationally efficient and has better statistical calibration.
- Spectral data quality is poor (low signal-to-noise, insufficient fragmentation) — blind mode will amplify false positives without targeted constraints.

## Inputs

- tandem mass spectra in MGF or mzML format (centroided)
- RiPP precursor sequence file (FASTA format)
- RiPP structure database

## Outputs

- significant_matches.tsv (scan identifiers, match scores, p-values, false discovery rates)
- cross-comparison table of blind vs. standard mode hits
- differential detection summary (blind-mode-only, standard-mode-only, common identifications)

## How to apply

Execute the database search pipeline (e.g., MetaMiner) twice: first with standard parameters to establish a baseline of known PTM hits, then re-execute with the `--blind` flag enabled to search for arbitrary modifications without constraining to predefined PTM types. Parse and cross-compare the significant_matches.tsv outputs from both runs, recording scan identifiers, match scores, p-values, and false discovery rates. Tabulate tool-specific detections and common identifications between modes to identify modifications and hit patterns unique to blind mode, using this differential analysis to distinguish genuine novel modifications from noise and assess mode-dependent sensitivity.

## Related tools

- **MetaMiner** (Primary pipeline for blind-mode PTM-agnostic RiPP database search; accepts --blind flag to relax structural constraints) — https://github.com/mohimanilab/MetaMiner
- **ProteoWizard msconvert** (Converts spectra in non-native formats (mzXML, mzData, mzML) to MGF for compatibility with blind search) — http://proteowizard.sourceforge.net/
- **NPDtools 2.5.0** (Toolkit containing MetaMiner and related database search pipelines (Dereplicator, VarQuest, Dereplicator+); version 2.5.0 includes blind-mode support) — https://github.com/ablab/npdtools

## Examples

```
python metaminer.py test_data/metaminer/msms/ -s test_data/metaminer/fasta/ -o metaminer_outdir && python metaminer.py test_data/metaminer/msms/ -s test_data/metaminer/fasta/ --blind -o metaminer_blind_outdir
```

## Evaluation signals

- Blind mode outputs additional valid matches (non-zero rows in significant_matches.tsv) not present in standard mode, with p-values and FDR consistent with statistical significance thresholds
- Scan identifiers and match scores from blind mode are reproducible across independent executions
- Cross-comparison reveals distinct modification patterns in blind-mode-only hits (e.g., mass shifts not in the standard PTM dictionary) with fragmentation patterns consistent with real PTMs
- False discovery rate (FDR) in blind mode remains below acceptable threshold (e.g., < 0.05 or < 0.10 depending on downstream validation), assessed via spectral quality and chemical plausibility of identified modifications
- Blind mode hits can be validated by independent spectral networking or metabologenomic integration (e.g., presence of corresponding biosynthetic gene clusters) where available

## Limitations

- Blind mode substantially increases computational cost and runtime compared to standard (constrained) mode, as it searches over a vastly larger space of possible modifications.
- False positive rate increases in blind mode due to relaxed constraints; results require post-hoc filtering by FDR, manual inspection of fragmentation patterns, or orthogonal validation (e.g., genomic evidence).
- Blind mode is most effective on high-quality, well-fragmented spectra; poor spectral data or weak ionization will amplify spurious matches.
- No changelog or version-specific documentation of blind-mode algorithm changes was found; reproducibility across NPDtools versions may vary.
- Blind mode assumes the reference RiPP structure database is sufficiently comprehensive; if the true parent structure is absent, blind mode cannot recover it.

## Evidence

- [methods] Execute MetaMiner again with --blind flag enabled to search for arbitrary post-translational modifications.: "Execute MetaMiner again with --blind flag enabled to search for arbitrary post-translational modifications."
- [methods] MetaMiner is a metabologenomic pipeline which integrates metabolomic (tandem mass spectra) and genomic data to identify novel RiPPs: "MetaMiner is a metabologenomic pipeline which integrates metabolomic (tandem mass spectra) and genomic data to identify novel RiPPs"
- [methods] Parse and tabulate significant_matches.tsv outputs from all three tools, recording scan identifiers, match scores, p-values, and false discovery rates.: "Parse and tabulate significant_matches.tsv outputs from all three tools, recording scan identifiers, match scores, p-values, and false discovery rates."
- [methods] Cross-compare hit sets to identify tool-specific detections, common identifications, and mode-dependent sensitivity differences.: "Cross-compare hit sets to identify tool-specific detections, common identifications, and mode-dependent sensitivity differences."
- [readme] **VarQuest** — a tool for modification-tolerant identification of novel variants of PNPs: "**VarQuest** — a tool for modification-tolerant identification of novel variants of PNPs"
