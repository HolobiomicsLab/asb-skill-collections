---
name: fragment-ion-peak-annotation
description: Use when you have experimental MS/MS spectra matched against a reference library (via cosine similarity or dot-product scoring) and need to map individual fragment peaks in the experimental spectrum to their corresponding m/z and intensity values in the matched library entry.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3647
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - TandemMatch
  - Mirador
  - IonToolPack
derived_from:
- doi: 10.1021/jasms.4c00146
  title: PeakQC
evidence_spans:
- 'TandemMatch: MS/MS spectral library matching with support for MSP and CSV library formats.'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_peakqc_cq
    doi: 10.1021/jasms.4c00146
    title: PeakQC
  dedup_kept_from: coll_peakqc_cq
schema_version: 0.2.0
---

# fragment-ion-peak-annotation

## Summary

Assign fragment m/z values and intensities from experimental MS/MS spectra to matched reference library entries, establishing peak-to-ion correspondence for compound identification and structural elucidation. This skill bridges spectral matching scores to actionable fragment ion assignments that support metabolite structure confirmation.

## When to use

You have experimental MS/MS spectra matched against a reference library (via cosine similarity or dot-product scoring) and need to map individual fragment peaks in the experimental spectrum to their corresponding m/z and intensity values in the matched library entry. Use this when your goal is to report which specific fragment ions were observed, validate fragmentation patterns against known standards, or prepare annotated spectra for publication or downstream structure elucidation.

## When NOT to use

- You only need to identify the best-matching compound name and are not concerned with fragment-level structural validation or publication-quality annotated spectra.
- Your experimental spectra lack sufficient peak resolution or signal intensity to reliably align with reference library fragments (e.g., low-quality DIA data or direct infusion with poor baseline).
- The reference library format does not include fragment m/z and intensity values (e.g., peak retention time tables only, without MS/MS spectral data).

## Inputs

- Experimental MS/MS spectra (from mzML, mzXML, or raw instrument formats) with precursor m/z, retention time, and fragment peak lists
- Matched reference library entries (MSP or CSV format) with fragment m/z values, intensities, and spectrum metadata
- Match scores (cosine similarity or dot-product values) from TandemMatch ranking
- User-defined mass tolerance and score threshold parameters

## Outputs

- Annotated match records (CSV or JSON) containing spectrum metadata, library accession, match score, and fragment ion assignments
- Fragment ion assignment table with columns: experimental m/z, library reference m/z, intensity, mass error (ppm), fragment annotation/ion type
- Optionally: MS/MS mirror plots or tabular comparison of experimental vs. library fragmentation patterns

## How to apply

After TandemMatch ranks library candidates by match score and applies similarity thresholds and mass tolerance filters on precursor m/z, iterate through each matched library spectrum. For the top-ranked match (or all matches above a configurable score threshold), extract the reference spectrum's fragment m/z array and intensity array. Align experimental peaks to library fragments using a mass tolerance window (typically ±5–10 ppm, user-configurable) and intensity rank concordance. Output matched records including spectrum metadata, library accession, match score, and an explicit fragment ion assignment table mapping each observed experimental m/z to its library reference m/z, intensity, and annotation (e.g., loss of water, neutral loss, characteristic fragment). This assignment list is written to structured output (CSV or JSON) alongside the match score for traceability and quality review.

## Related tools

- **TandemMatch** (Performs MS/MS spectral library matching, ranks candidates by cosine similarity or dot-product score, and filters by precursor m/z tolerance; output feeds into fragment ion assignment.) — https://github.com/pnnl/IonToolPack
- **Mirador** (Visualizes and exports raw MS data including MS/MS mirror plots and extracted ion chromatograms; supports manual inspection and PDF/CSV export of annotated spectra.) — https://github.com/pnnl/IonToolPack
- **IonToolPack** (Host software suite that integrates TandemMatch and Mirador; reads multiple instrument formats and provides GUI for unified workflow.) — https://github.com/pnnl/IonToolPack

## Evaluation signals

- All experimental peaks above a user-defined signal-to-noise threshold are assigned to library fragments or explicitly marked as unassigned, with no duplicate or contradictory assignments.
- Mass error (in ppm) between experimental and library fragment m/z values remains within the specified tolerance window (typically ≤5–10 ppm) for ≥80% of assigned peaks.
- Intensity rank correlation between experimental and library fragments is monotonic or near-monotonic (Spearman ρ > 0.6) for matched entries, indicating consistent fragmentation patterns.
- Output records include all required fields (library accession, match score, fragment m/z, experimental m/z, mass error, intensity) with no null or malformed values.
- Fragment annotations (e.g., 'neutral loss of H₂O', 'characteristic m/z 147') align with known chemical structures and published fragmentation rules for the identified compound class (metabolite, lipid, peptide).

## Limitations

- Fragment ion assignment relies on accurate precursor m/z matching and assumes the reference library entries are correctly annotated; errors in library data propagate to output.
- Mass tolerance thresholds must be tuned per instrument type and resolution (e.g., Orbitrap vs. quadrupole); insufficient tolerance misses true assignments, excessive tolerance introduces false positives.
- Isomeric compounds may produce highly similar or identical MS/MS spectra, making fragment-level discrimination ambiguous; annotation alone cannot resolve isomeric ambiguity.
- DIA (data-independent acquisition) mode may produce chimeric spectra with overlapping fragments from multiple precursor m/z values; standard point-to-point alignment may fail under these conditions.
- No explicit changelog or versioning information is documented, limiting reproducibility and tracking of method updates across IonToolPack releases.

## Evidence

- [other] Apply cosine similarity or dot-product scoring to compare each experimental MS/MS spectrum against all library entries, then filter by similarity threshold and mass tolerance on precursor m/z.: "Apply cosine similarity or dot-product scoring to compare each experimental MS/MS spectrum against all library entries. 4. Filter candidate matches using a similarity threshold and mass tolerance"
- [other] Output matched records with spectrum metadata, library accession, match score, and fragment ion assignments to structured results file.: "Rank matched library spectra by score and output matched records with spectrum metadata, library accession, match score, and fragment ion assignments to a structured results file (CSV or JSON)."
- [readme] TandemMatch supports MSP and CSV library formats with fragment m/z and intensity values extracted from reference spectra.: "TandemMatch: MS/MS spectral library matching with support for MSP and CSV library formats."
- [readme] Mirador enables raw MS data visualization and export including MS/MS mirror plots for comparison of experimental and reference spectra.: "Mirador: Raw MS data visualization and export (PDF, CSV) including extracted ion chromatograms (XIC), extracted ion mobility (XIM) heatmaps, and MS/MS mirror plots"
- [readme] IonToolPack reads data from multiple instrument formats and provides omics-agnostic functionalities for metabolomics, lipidomics, and proteomics.: "It reads data from multiple instrument formats, requires no installation and provides omics agnostic functionalities (metabolomics, lipidomics, proteomics, etc.)"
