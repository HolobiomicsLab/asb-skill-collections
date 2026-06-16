# Evaluation Strategy

## Direct Checks

- verify that the task queue implementation exists in the iomega/paired-data-form repository
- verify that project JSON documents can be loaded and contain a genome identifier field
- verify that the enrichment function accepts a project JSON document with a genome identifier as input
- verify that the enrichment function returns a project JSON document with an organism name field added or populated
- verify that the organism name lookup calls an external registry API (e.g., NCBI, ENA, or similar) with the genome identifier
- verify that the returned organism name matches the external registry record for the given genome identifier — requires manual spot-check against at least 3 distinct genome identifiers
- verify that the enriched JSON output file format is valid JSON and preserves all input fields from the original project document
- script_runs: test the enrichment function on a sample project JSON with known genome identifier and verify it produces output without errors

## Expert Review

- confirm that the external registry queried for organism name lookup is appropriate and current for the target genome domain
- confirm that the mapping between genome identifier field name(s) in project JSON and the registry query parameter is correct and complete
- confirm that error handling is appropriate when a genome identifier does not resolve in the external registry
