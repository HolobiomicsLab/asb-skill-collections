# Evaluation Strategy

## Direct Checks

- verify that github:constantino-garcia/cmmrt repository is accessible and contains source code for the CMM-RT system
- verify that the repository contains implementation of DNN-based retention time prediction model
- verify that the repository contains implementation of Bayesian meta-learning projection module
- verify that the repository contains a working example or script that accepts a query mass spectrum and outputs a ranked candidate list
- verify that expected_outputs[0] (ranked candidate list with RT probability scores) is a structured file (JSON, CSV, or TSV format) with at least three columns: candidate_identifier, RT_probability_score, and rank
- verify that RT probability scores in expected_outputs[0] are numeric values in range [0.0, 1.0]
- verify script_runs: that a computational agent can execute the CMM-RT annotation pipeline with the example query spectrum without errors
- verify that output_matches_reference: the number and order of candidate annotations in the ranked list are consistent with the meta-learned projection methodology (no canonical answer for exact ordering, but output must be deterministic and defensible)

## Expert Review

- assess whether the RT probability scores assigned to each candidate metabolite annotation are mathematically sound and properly calibrated from the DNN predictions and meta-learned projections
- assess whether the ranked candidate list reflects appropriate integration of DNN-predicted retention times with meta-learned chromatographic method projections
- assess whether the RT probability scores are meaningful for discriminating true metabolite identities from incorrect candidates in the example query spectrum
- assess whether the example query spectrum and its ranked results are representative of typical metabolomics use cases
