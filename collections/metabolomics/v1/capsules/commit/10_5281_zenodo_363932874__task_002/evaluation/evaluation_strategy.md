# Evaluation Strategy

## Direct Checks

- verify that Zenodo deposit 10.5281/zenodo.363932874 is accessible and contains source code or documentation for the COMMIT gap-filling module
- verify that the COMMIT repository contains a gap-filling implementation with documented inputs (consensus metabolic reconstructions) and outputs (gap-filled models)
- script_runs: execute the gap-filling workflow on provided consensus reconstructions and verify it completes without error
- verify that gap-filled metabolic reconstructions are produced in a standard format (SBML, JSON, or tabular) with named output file(s)
- verify output_matches_reference: compare gap-filled reconstructions against any reference outputs or validation sets provided in the deposit

## Expert Review

- assess whether the gap-filling procedure correctly leverages community context (metabolic overlap, complementary pathways, or shared gene annotations among community members) as intended by COMMIT
- evaluate whether gaps filled are biochemically plausible and represent genuine missing reactions in the consensus model rather than artifacts of the algorithm
- review gap-filling decisions for metabolic consistency: do filled reactions maintain stoichiometric balance and thermodynamic feasibility across the community model
