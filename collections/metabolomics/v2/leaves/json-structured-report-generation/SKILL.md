---
name: json-structured-report-generation
description: Use when after Mass2Motif annotation candidates have been ranked and
  filtered by similarity score (using Spec2Vec embeddings queried against MotifDB),
  you need to serialize the ranked results into a standardized, hierarchical format
  that preserves confidence metadata and enables programmatic access.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - MS2LDA
  - MAG
  - Python
  - MAG (Automated Mass2Motif Annotation Guidance)
  - Spec2Vec
  - MotifDB
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1073/pnas.1608041113
  title: MS2LDA
evidence_spans:
- '**MS2LDA** applies *probabilistic topic modeling*, originally developed for natural
  language processing (NLP), to **tandem mass spectrometry (MS/MS)** data.'
- Invoke the main script `ms2lda_runfull.py` with your arguments
- Automated annotation of **M2M** using **MAG**
- configure the Python environment (set `PYTHONPATH`, activate conda, etc.)
- Configure the Python environment (set `PYTHONPATH`, activate conda, etc.)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2lda_cq
    doi: 10.1073/pnas.1608041113
    title: MS2LDA
  dedup_kept_from: coll_ms2lda_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1073/pnas.1608041113
  all_source_dois:
  - 10.1073/pnas.1608041113
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# json-structured-report-generation

## Summary

Generate machine-readable JSON reports that map discovered Mass2Motifs to candidate substructures, confidence scores, and structural classes. This skill bridges automated annotation inference with structured output suitable for downstream computational integration and human review.

## When to use

After Mass2Motif annotation candidates have been ranked and filtered by similarity score (using Spec2Vec embeddings queried against MotifDB), you need to serialize the ranked results into a standardized, hierarchical format that preserves confidence metadata and enables programmatic access to substructure assignments for each motif.

## When NOT to use

- Mass2Motif discovery has not yet been completed; report generation requires ranked annotation candidates as input.
- Annotation candidates have not been ranked or filtered by similarity threshold; unranked candidates should not be serialized without explicit score stratification.
- The analysis goal is exploratory visualization only; use MS2LDAViz interactive interface instead of generating static JSON reports.

## Inputs

- Ranked annotation candidates (from MotifDB query results filtered by similarity threshold)
- Mass2Motif identifiers and fragmentation patterns
- Spec2Vec similarity scores for each candidate annotation
- Structural class labels from reference database

## Outputs

- JSON report file mapping Mass2Motifs to candidate substructures, confidence scores, and structural classes
- Structured annotation metadata suitable for programmatic access and downstream integration

## How to apply

The MAG module computes Spec2Vec embeddings for each discovered Mass2Motif pseudo-spectrum (fragments and neutral losses weighted by LDA probabilities), queries MotifDB via those embeddings to retrieve structurally related reference motifs, ranks candidates by similarity score using default MAG heuristics or explicit thresholds, and then serializes the ranked candidates into a JSON report. Each motif entry in the report includes its identifier, candidate annotations with associated confidence scores, structural class labels, and any auxiliary metadata (e.g., motif composition statistics). The JSON structure should be flat or hierarchical enough to enable both human readability and programmatic parsing by annotation validation pipelines or structure elucidation workflows.

## Related tools

- **MAG (Automated Mass2Motif Annotation Guidance)** (Generates ranked annotation candidates by querying MotifDB with Spec2Vec embeddings and filtering by similarity score; orchestrates serialization into JSON format) — https://github.com/vdhooftcompmet/MS2LDA
- **Spec2Vec** (Computes embeddings for Mass2Motif pseudo-spectra; enables similarity-based retrieval and ranking of reference motifs from MotifDB) — https://zenodo.org/records/15688609
- **MotifDB** (Serves as query target and source of reference motif metadata (structural classes, candidate annotations); results are filtered and ranked before JSON serialization)
- **MS2LDA** (Parent workflow that orchestrates preprocessing, LDA modeling, and invocation of MAG for annotation guidance and JSON report generation) — https://github.com/vdhooftcompmet/MS2LDA

## Evaluation signals

- JSON schema is valid and parseable by standard JSON libraries; no serialization errors or truncation artifacts.
- Each Mass2Motif entry includes at least one ranked candidate annotation with non-null confidence score and structural class label.
- Similarity scores are monotonically decreasing across ranked candidates for each motif (or explicitly tied); no out-of-order ranks.
- All Mass2Motif identifiers in the report correspond to motifs discovered in the preceding LDA modeling step.
- JSON file size and record count are consistent with the number of discovered motifs and candidate annotations; spot-check a sample of motif entries for metadata completeness.

## Limitations

- Report quality depends on MotifDB coverage and the appropriateness of the Spec2Vec model for the user's spectral domain; low-scoring candidates may indicate sparse reference data or model domain mismatch.
- Default MAG heuristics and similarity thresholds are applied; users unfamiliar with the threshold rationale may generate reports with either inflated false positives or suppressed true candidates.
- JSON serialization does not include confidence interval or Bayesian posterior estimates; scores are point estimates from the MAG ranking heuristic.
- The report is a snapshot of annotations at the time of generation; it does not track how annotations change if MotifDB or the Spec2Vec model are updated.

## Evidence

- [other] Generate and return an annotation report mapping each Mass2Motif to candidate substructures, confidence scores, and structural classes in JSON format.: "Generate and return an annotation report mapping each Mass2Motif to candidate substructures, confidence scores, and structural classes in JSON format."
- [other] Rank and filter candidate annotations by similarity score (default threshold applied by MAG heuristics).: "Rank and filter candidate annotations by similarity score (default threshold applied by MAG heuristics)."
- [methods] Automated Mass2Motif Annotation Guidance (MAG) with Spec2Vec: "Automated Mass2Motif Annotation Guidance (MAG) with Spec2Vec"
- [other] Query MotifDB via the loaded embeddings to retrieve structurally related reference motifs and candidate annotations.: "Query MotifDB via the loaded embeddings to retrieve structurally related reference motifs and candidate annotations."
- [other] Compute Spec2Vec embeddings for each Mass2Motif pseudo-spectrum using the loaded model.: "Compute Spec2Vec embeddings for each Mass2Motif pseudo-spectrum using the loaded model."
