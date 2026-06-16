# Evaluation Strategy

## Direct Checks

- verify that input file contains at least 2 columns: m/z and assigned molecular formula (field_present)
- verify that the standalone script accepts a peak list file as command-line argument or config parameter (script_runs)
- verify that the script computes pairwise mass differences and outputs a numeric matrix or edge list (output_matches_reference: check against Example transformation network data in bacterium-phage dataset OSF deposit https://doi.org/10.17605/OSF.IO/XFHZ9)
- verify that output node/edge list file is in Cytoscape-compatible format (.sif, .gml, or edge-attribute table; format_is)
- verify that file_exists for output node list and edge list artifacts
- verify that transformation matching correctly retrieves entries from reference transformation table (no canonical answer—multiple valid transformation databases may apply; expert_review required for chemistry accuracy)
- verify that script completes without error on bacterium-phage dataset (40 samples, average 495 peaks with assigned formula per sample) in parameter-sensitive runtime (expected sub-minute based on reported ~36 s for main pipeline steps without KEGG mapping)
- verify that rows in output edge list contain at minimum: source_mass, target_mass, mass_difference, transformation_name fields (row_count_equals and field_present)

## Expert Review

- Assess whether mass-difference matching algorithm correctly resolves ambiguous transformations (multiple biochemically valid transformations at same Δm/z)
- Evaluate whether the standalone implementation preserves the transformation network generation logic reported for bacterium-phage results (Fig. 3B shows lignin–protein interaction clusters; expert should verify those patterns reproduce from script output)
- Review whether edge weights (if present) accurately reflect transformation abundance or frequency across samples, consistent with Fig. 3A heatmap methodology
- Confirm that script output is suitable for direct import into Cytoscape without manual curation or format conversion
