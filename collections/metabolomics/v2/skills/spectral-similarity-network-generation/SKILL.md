---
name: spectral-similarity-network-generation
description: Use when after feature detection and alignment across LC-MS/MS runs (via MZmine2 or Optimus) have produced a feature quantification table and MGF file with MS/MS spectra, and you need to discover molecular relationships and detect unknown compounds through spectral clustering and library matching.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - MZmine2
  - Optimus
  - GNPS
  - Cytoscape
derived_from:
- doi: 10.1021/acs.jnatprod.7b00737
  title: Bioactivity-Based Molecular Networking
evidence_spans:
- open bioinformatic tools, such [MZmine2](http://mzmine.github.io/)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_bioactivity_based_molecular_networking_cq
    doi: 10.1021/acs.jnatprod.7b00737
    title: Bioactivity-Based Molecular Networking
  dedup_kept_from: coll_bioactivity_based_molecular_networking_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jnatprod.7b00737
  all_source_dois:
  - 10.1021/acs.jnatprod.7b00737
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-similarity-network-generation

## Summary

Generate a spectral similarity graph by uploading processed MS/MS feature tables and spectral data to the GNPS web-platform, configuring molecular networking parameters, and retrieving node and edge tables that represent compounds/spectra and their spectral similarity relationships.

## When to use

After feature detection and alignment across LC-MS/MS runs (via MZmine2 or Optimus) have produced a feature quantification table and MGF file with MS/MS spectra, and you need to discover molecular relationships and detect unknown compounds through spectral clustering and library matching.

## When NOT to use

- Input MS/MS data lacks proper precursor m/z or retention time annotation — GNPS requires complete spectral metadata.
- Feature table has not undergone quality filtering (e.g., blank/control exclusion, reproducibility checks in QC replicates) — unfiltered features will produce noisy network topology.
- The goal is targeted compound identification rather than untargeted molecular relationship discovery — consider MS/MS library matching workflows instead.

## Inputs

- feature quantification table (CSV format with aligned features and intensities across samples)
- MS/MS spectral data (MGF or mzML format with precursor m/z, retention time, and MS/MS fragmentation spectra)

## Outputs

- node table (list of compounds/spectra with metadata)
- edge table (spectral similarity links with similarity scores and edge filtering information)
- spectral similarity network graph (for import into Cytoscape or other visualization tools)

## How to apply

Prepare your feature table and MS/MS data in formats accepted by GNPS (typically mzML or MGF containing precursor m/z, retention time, and MS/MS spectra). Access the GNPS web-platform at http://gnps.ucsd.edu and upload the processed data. Configure molecular networking parameters including spectral similarity scoring (typically cosine similarity) and edge filtering thresholds to define when two spectra are considered connected. Submit the job to the GNPS platform to compute the spectral similarity graph. Retrieve the resulting node table containing compounds/spectra identifiers and the edge table containing spectral similarity links and scores between pairs of spectra. The edge table defines the network topology for downstream visualization and analysis.

## Related tools

- **MZmine2** (Feature detection, alignment, and quantification to produce feature table and MGF spectral file for GNPS submission) — http://mzmine.github.io/
- **Optimus** (Alternative LC-MS feature detection and quantification using OpenMS algorithms to generate feature table and MS/MS data for GNPS networking) — https://github.com/MolecularCartography/Optimus
- **GNPS** (Web-platform for spectral similarity graph computation, molecular networking, and spectral library matching) — http://gnps.ucsd.edu
- **Cytoscape** (Visualization and interactive exploration of the spectral similarity network graph (node and edge tables from GNPS)) — http://www.cytoscape.org/

## Evaluation signals

- Node table contains all input spectra with unique identifiers and includes metadata fields (precursor m/z, retention time, sample origin).
- Edge table contains pairs of node IDs with spectral similarity scores and respects the configured edge filtering threshold (e.g., cosine similarity > 0.7).
- Network connectivity is meaningful: isolated nodes indicate spectra with low similarity to library or other samples; dense clusters indicate co-eluting or chemically related compounds.
- Node and edge tables can be successfully imported into Cytoscape without schema errors or missing required fields.
- GNPS output includes quality metrics such as number of connected components, average node degree, and number of library matches (MS/MS validation).

## Limitations

- GNPS spectral similarity relies on cosine similarity scoring of fragmentation patterns; structural isomers or compounds with similar MS/MS spectra may be incorrectly linked.
- Edge thresholds must be tuned per compound class and ionization method; too stringent filtering may disconnect true analogues, too permissive filtering introduces false edges.
- Molecular networking does not validate spectral annotations; MS/MS library matches require manual inspection or secondary validation (e.g., by Sirius or MS-FINDER in-silico prediction).
- Large datasets (hundreds of LC-MS runs) may require parameter optimization and extended computation time on GNPS servers.
- Spectra lacking MS/MS data or with very few fragment ions may not form network edges and will appear as isolated nodes.

## Evidence

- [other] Prepare feature table and MS/MS data in the format required by GNPS (typically mzML or MGF with precursor m/z, retention time, and MS/MS spectra).: "Prepare feature table and MS/MS data in the format required by GNPS (typically mzML or MGF with precursor m/z, retention time, and MS/MS spectra)."
- [other] Access the GNPS web-platform at http://gnps.ucsd.edu and upload the processed data. Configure molecular networking parameters including spectral similarity scoring and edge filtering thresholds. Submit the job to the GNPS platform to compute the spectral similarity graph.: "Access the GNPS web-platform at http://gnps.ucsd.edu and upload the processed data. Configure molecular networking parameters including spectral similarity scoring and edge filtering thresholds."
- [other] Retrieve the resulting node table (compounds/spectra) and edge table (spectral similarity links) from GNPS output.: "Retrieve the resulting node table (compounds/spectra) and edge table (spectral similarity links) from GNPS output."
- [readme] The workflow relies on open bioinformatic tools, such MZmine2 or Optimus (using OpenMS), a Jupyter notebook, and the GNPS web-platform: "The workflow relies on open bioinformatic tools, such MZmine2 or Optimus (using OpenMS), a Jupyter notebook, and the GNPS web-platform"
- [readme] Process your data following instructions described in the GNPS feature-based molecular networking workflow (FBMN) documentation.: "Process your data following instructions described in the GNPS feature-based molecular networking workflow (FBMN) documentation."
