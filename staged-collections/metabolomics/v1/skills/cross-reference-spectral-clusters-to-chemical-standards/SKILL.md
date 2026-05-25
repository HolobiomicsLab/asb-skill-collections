---
name: cross-reference-spectral-clusters-to-chemical-standards
description: Match molecular network spectral nodes to known chemical standards and reference libraries by comparing MS/MS fragmentation patterns and neutral loss signatures. This skill bridges untargeted spectral clustering with targeted compound identification, enabling annotation of metabolite structures and enzymatic products in complex biotransformation datasets.
when_to_use_negative:
- Input is already a fully annotated feature table (e.g., from targeted metabolomics with internal standards) — skip clustering and reference matching.
- Reference library coverage is <50% for your compound class — annotation confidence will be too low without supplementary NMR or MS/MS fragmentation validation.
- Spectral quality is poor (low S/N ratio, fragmented peaks, <10 significant MS/MS peaks per spectrum) — cosine similarity matching will be unreliable.
edam_operation: http://edamontology.org/operation_3860
edam_topics:
- http://edamontology.org/topic_0121
- http://edamontology.org/topic_0602
- http://edamontology.org/topic_3375
tools:
- name: GNPS (Global Natural Products Social Molecular Networking)
  role: Generates feature-based molecular networks, provides MS/MS reference library, hosts MassQL query engine for spectral filtering
  repo: https://gnps.ucsd.edu/
- name: MassQL
  role: Queries MS/MS spectra for diagnostic neutral losses (132.0423 Da pentose, 162.0528 Da hexose) to filter nodes prior to reference matching
- name: LC-MS/MS instrumentation
  role: Generates raw fragmentation spectra for molecular network and library reference comparison
- name: NMR (Nuclear Magnetic Resonance)
  role: Orthogonal validation of chemical structure and regioselectivity for selected annotated nodes (e.g., O-β-D-xylosylation vs. O-glucuronidation)
provenance:
  source_task_ids:
  - task_001
  source_papers:
  - doi: 10.1073/pnas
    title: Proceedings of the National Academy of Sciences
schema_version: 0.2.0
metadata:
  merge_audit:
    n_source_runs: 2
    source_files:
    - outputs/audit_jeong_full/skills/cross-reference-spectral-clusters-to-chemical-standards/SKILL.md
    - outputs/audit_jeong_full/skills/cross-reference-spectral-clusters-to-chemical-standards/skill.md
    merged_at: '2026-05-25T07:15:30.924716+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/cross-reference-spectral-clusters-to-chemical-standards@sha256:9c4a255f87cba9fde503c0300cc06cdd5dccb231a8d15d3f776679c35b6481fe
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1073/pnas
---

# cross-reference-spectral-clusters-to-chemical-standards

## Summary

Match molecular network spectral nodes to known chemical standards and reference libraries by comparing MS/MS fragmentation patterns and neutral loss signatures. This skill bridges untargeted spectral clustering with targeted compound identification, enabling annotation of metabolite structures and enzymatic products in complex biotransformation datasets.

## When to use

You have feature-based molecular networking output (spectral nodes clustered by cosine similarity) and need to assign chemical identities to nodes. Use this skill when you have access to reference MS/MS spectra (e.g., GNPS library, commercial standards, or NMR-confirmed isolates) and want to validate that spectral clusters correspond to specific compounds with known biotransformation products or regioisomers.

## When NOT to use

- Input is already a fully annotated feature table (e.g., from targeted metabolomics with internal standards) — skip clustering and reference matching.
- Reference library coverage is <50% for your compound class — annotation confidence will be too low without supplementary NMR or MS/MS fragmentation validation.
- Spectral quality is poor (low S/N ratio, fragmented peaks, <10 significant MS/MS peaks per spectrum) — cosine similarity matching will be unreliable.

## Inputs

- FBMN-generated molecular network node table (node IDs, consensus MS/MS spectra)
- FBMN spectral edges file (cosine similarity scores between nodes)
- MS/MS reference library spectra (GNPS public library or local .mgf/.mzML format)
- Peak detection thresholds (amplitude cutoff, e.g., >10,000 counts)
- MassQL query parameters (neutral loss m/z values with 0.01 Da tolerance)

## Outputs

- Annotated spectral node table with compound identities, reference match scores, and neutral loss signatures
- Molecular network clusters labeled by chemical compound name or structural class (e.g., xylosylated baicalein isomers 2a–2g)
- Regioisomer assignments mapped to specific network nodes with confidence scores
- Filtered MS/MS spectra subset enriched for target biotransformation products

## How to apply

After generating a feature-based molecular network with GNPS (using default MS/MS peak detection and cosine similarity scoring with ≥0.7 threshold), retrieve the molecular network nodes and their constituent MS/MS spectra. Apply targeted filtering via MassQL to identify spectra containing diagnostic neutral losses (e.g., 132.0423 Da for pentosylation, 162.0528 Da for hexosylation) that match the expected fragmentation signature of your target compound class. Cross-reference the filtered spectral nodes against both the GNPS public MS/MS reference library and your experimentally validated standards (e.g., purified compounds characterized by NMR and acidic hydrolysis). Cluster matching nodes spatially within the molecular network graph and compare their retention times, accurate masses, and fragmentation patterns against known congeners. The strength of annotation depends on cosine similarity score, neutral loss specificity, and agreement with reference spectra; compounds with multiple regioisomeric positions (detected as separate nodes within the same network cluster) should be confirmed by orthogonal methods (NMR, HPLC-MS/MS co-elution, or in vitro enzyme assays).

## Related tools

- **GNPS (Global Natural Products Social Molecular Networking)** (Generates feature-based molecular networks, provides MS/MS reference library, hosts MassQL query engine for spectral filtering) — https://gnps.ucsd.edu/
- **MassQL** (Queries MS/MS spectra for diagnostic neutral losses (132.0423 Da pentose, 162.0528 Da hexose) to filter nodes prior to reference matching)
- **LC-MS/MS instrumentation** (Generates raw fragmentation spectra for molecular network and library reference comparison)
- **NMR (Nuclear Magnetic Resonance)** (Orthogonal validation of chemical structure and regioselectivity for selected annotated nodes (e.g., O-β-D-xylosylation vs. O-glucuronidation))

## Examples

```
On GNPS, after FBMN job completion, open the molecular network result, navigate to the MassQL query interface, enter the query 'FILTER @MS/MS [Loss(132.0423±0.01)] OR @MS/MS [Loss(162.0528±0.01)]', execute to retrieve spectral nodes with pentose/hexose neutral losses, then manually inspect the top 20 nodes against the GNPS library matches and cross-tabulate node IDs with compound identities (e.g., 2a, 2e) from your reference standards.
```

## Evaluation signals

- Cosine similarity score ≥0.7 between query spectrum and reference spectrum, with ≥6 common m/z peaks in the matching region
- Neutral loss signatures (e.g., −132.04 Da, −162.05 Da) present in query spectrum and consistent with reference standard fragmentation
- Annotated nodes cluster spatially in the molecular network (Euclidean distance in network layout <0.5 normalized units) when they correspond to regioisomers or congeners
- Retention time agreement (±0.5 min on reversed-phase C18) between query feature and reference standard, when standards are available
- Orthogonal confirmation by NMR, acidic hydrolysis (sugar identity), or in vitro enzyme assay validates structure for ≥2 representative nodes per compound class

## Limitations

- GNPS library coverage is incomplete for minor metabolites and biosynthetic variants — spectral nodes may lack reference matches even if chemically valid.
- Regioisomers and stereoisomers produce near-identical MS/MS spectra and cannot be distinguished by cosine similarity alone; NMR or 2D-HPLC is required to resolve positional isomers.
- Neutral loss-based filtering is sensitive to peak detection threshold (set at >10,000 amplitudes in this study) — low-abundance metabolites may be filtered out as noise.
- Cross-reference confidence depends critically on reference library quality; GNPS library spectra generated under differing collision energies and ionization conditions may show reduced cosine similarity even for true matches.
- Unknown enzymatic activities (e.g., O-methylation, hydroxylation) detected in the molecular network cannot be confidently annotated without reference spectra or targeted synthesis.

## Evidence

- [results] MassQL-annotated spectral nodes with the molecular network to identify clusters corresponding to pentosylated and hexosylated metabolites: "Cross-reference MassQL-annotated spectral nodes with the molecular network to identify clusters corresponding to pentosylated and hexosylated metabolites."
- [results] Many spectral nodes could be structurally annotated due to high coverage of the GNPS MS/MS reference library: "Many spectral nodes could be structurally annotated due to high coverage of the GNPS MS/MS reference library"
- [results] MassQL was helpful for the annotation of sugar conjugation, as it rapidly annotated hexosylation and pentosylation of the flavonoids: "MassQL was helpful for the annotation of sugar conjugation, as it rapidly annotated hexosylation and pentosylation of the flavonoids"
- [results] Seven metabolites (2a–2g) were purified, and we identified the structures of these metabolites as O-β-D-xylosylated products of 2: "Seven metabolites (2a–2g) were purified, and we identified the structures of these metabolites as O-β-D-xylosylated products of 2"
- [discussion] MS/MS spectra containing neutral losses of 132.0423 or 162.0528 Da were searched via MassQL: "MS/MS spectra containing neutral losses of 132.0423 or 162.0528 Da were searched via MassQL"
