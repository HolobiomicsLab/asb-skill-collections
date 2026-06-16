# Evaluation Strategy

## Direct Checks

- Verify that Zenodo deposit 10.5281/zenodo.363932874 is accessible and contains COMMIT source code or executable
- Verify that deposit contains documentation or README describing the consensus reconstruction step
- Verify that at least one example input file (draft metabolic reconstruction in standard format: SBML, JSON, or TSV) is present in the deposit
- Verify that at least one example output file (consensus reconstruction) is present in the deposit
- Script runs: execute COMMIT consensus step on provided example draft reconstructions and verify script completes without error
- Verify output file format matches input format (same file extension and schema structure)
- Verify output file contains metabolic reactions, metabolites, and genes fields expected in a consensus reconstruction (robust to field naming conventions)
- Row count or content comparison: verify that consensus output contains reactions that are present in the majority or all input draft reconstructions (parameter-sensitive: depends on consensus threshold definition)

## Expert Review

- Assess whether the consensus reconstruction correctly implements the consensus algorithm as described in the article (e.g., majority rule, intersection, or weighted voting) by comparing example input–output pairs
- Review whether the consensus reconstruction preserves metabolic network properties (connectivity, stoichiometric validity) that would be expected in a well-formed model
- Evaluate whether the consensus step produces biologically plausible metabolic coverage for the target organism(s) sampled from Arabidopsis thaliana communities
