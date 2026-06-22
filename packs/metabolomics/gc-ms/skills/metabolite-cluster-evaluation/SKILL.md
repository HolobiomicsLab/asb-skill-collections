---
name: metabolite-cluster-evaluation
description: Use when after running RAMClustR clustering on XCMS-detected LC-MS features in positive ionization mode, when you need to assign molecular weights to compound clusters and want to cross-validate the two available scoring methods (findMain and RAMClustR internal scoring) to identify cases where they.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_0599
  - http://edamontology.org/topic_3370
  tools:
  - RAMClustR
  - InterpretMSSpectrum
  - R
  - XCMS
  techniques:
  - LC-MS
  - GC-MS
derived_from:
- doi: 10.1021/ac501530d
  title: RAMClust
evidence_spans:
- ramclustR function is built to use xcms data
- RC <- ramclustR(xcmsObj = xset, ExpDes=experiment)
- We have adapted the 'findMain' function from the 'InterpretMSSpectrum' CRAN package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ramclust_cq
    doi: 10.1021/ac501530d
    title: RAMClust
  dedup_kept_from: coll_ramclust_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/ac501530d
  all_source_dois:
  - 10.1021/ac501530d
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-cluster-evaluation

## Summary

Validate and compare molecular weight inference methods (findMain vs. RAMClustR scoring) on clustered LC-MS metabolomics features to assess agreement rates and resolve discordant predictions. This skill ensures that compound clusters are assigned reliable consensus molecular weights before downstream annotation.

## When to use

After running RAMClustR clustering on XCMS-detected LC-MS features in positive ionization mode, when you need to assign molecular weights to compound clusters and want to cross-validate the two available scoring methods (findMain and RAMClustR internal scoring) to identify cases where they agree versus diverge, especially to flag potential compound misassignment or ambiguous mass regions.

## When NOT to use

- Input data is from negative ionization mode or alternative ionization methods (findMain parameters are tuned for positive mode; mode parameter must be explicitly set to 'negative' or other value, changing behavior)
- XCMS feature detection has not been completed or RC object is not properly initialized with ramclustR output
- Cluster assignments are already independently validated or consensus molecular weights are pre-assigned from orthogonal methods (e.g., reference standards)

## Inputs

- RC object (RAMClustR object post-clustering from XCMS feature detection and RAMClustR ramclustR function)
- positive ionization mode LC-MS data (implicit in RC object)

## Outputs

- RC object with do.findmain results (findMain-derived molecular weight predictions per cluster)
- Comparison table: cluster ID × findMain_MW × RAMClustR_MW × agreement_flag × consensus_MW
- Agreement rate (%) and distribution of discordant mass differences

## How to apply

Execute the do.findmain function on an RC (RAMClustR) object with mode='positive', mzabs.error=0.02, and ppm.error=10 to infer molecular weights using the findMain scoring approach. Extract and compare the molecular weight predictions from do.findmain against the RAMClustR internal scoring results for each compound cluster. Calculate the fraction of clusters where the two methods agree within acceptable tolerance (essentially identical masses). Report the agreement fraction and expect approximately 90% concordance. For the ~10% of clusters where methods disagree, implement a decision rule (e.g., use the higher of the two molecular weights) to generate a final consensus molecular weight table. Validate the resulting agreement rate against the published ~90% benchmark; substantial deviation (>5 percentage points) warrants investigation into feature detection artifacts or clustering boundary effects.

## Related tools

- **RAMClustR** (Provides the RC object, cluster definitions, and internal molecular weight scoring; do.findmain is called as a method on RC) — github.com/cbroeckl/RAMClustR
- **InterpretMSSpectrum** (Source of the findMain function, adapted into RAMClustR for independent molecular weight scoring)
- **XCMS** (Upstream feature detection and alignment; produces the input data fed to RAMClustR clustering)

## Examples

```
RC <- do.findmain(RC, mode = "positive", mzabs.error = 0.02, ppm.error = 10); agreement_rate <- mean(RC$findmain_mw == RC$ramclustr_mw) * 100
```

## Evaluation signals

- Agreement rate is approximately 90% (within ~5 percentage points); rates >95% or <85% suggest potential issues in feature detection or clustering parameters
- Comparison table includes all clusters; no missing values for findMain_MW or RAMClustR_MW scores
- Discordant pairs (where methods disagree) have mass differences explainable by instrument tolerance (typically < 0.02 Da absolute or < 10 ppm relative error)
- Consensus molecular weight rule (e.g., 'use higher value') is applied consistently and generates a single MW per cluster
- RC object post-do.findmain contains populated MW annotation field (ramclustobj$ann with molecular weight entries)

## Limitations

- Agreement rate is empirical and specific to positive ionization mode LC-MS; results may differ substantially in negative mode or GC-MS
- The ~90% benchmark is reported from published data; individual datasets may deviate depending on feature quality, adduct complexity, and mass range coverage
- When the two methods disagree, the decision rule (e.g., select higher MW) is heuristic and may not be optimal for all compounds; difficult-to-ionize or low-abundance compounds may receive low confidence scores from both methods
- No changelog or version history is documented in the repository, making it unclear whether the ~90% rate holds across different versions of RAMClustR

## Evidence

- [intro] agreement_rate_benchmark: "In practice we find that the two scoring methods agree about 90% of the time."
- [intro] do_findmain_parameters: "Execute do.findmain function on the RC object with mode='positive', mzabs.error=0.02, and ppm.error=10"
- [intro] comparison_workflow: "Extract and compare the molecular weight predictions from do.findmain against the RAMClustR internal scoring results for each compound cluster."
- [intro] calculation_and_validation: "Calculate the fraction of compounds (cluster centroids) where the two methods agree within acceptable tolerance (essentially identical masses). Report the agreement fraction as a percentage and"
- [readme] findMain_source: "We have adapted the 'findMain' function from the 'InterpretMSSpectrum' CRAN package"
- [readme] stepwise_workflow_example: "ramclustObj <- do.findmain(ramclustObj = ramclustObj)"
