# Evaluation Strategy

## Direct Checks

- verify file exists: squidpy package contains squidpy.gr.sepal function
- verify squidpy can be imported and sepal function is callable
- script_runs: load bundled dataset (dataset_slideseqv2 or dataset_merfish) from squidpy.datasets, call squidpy.gr.sepal on the AnnData object, and confirm execution completes without error
- field_present: verify the AnnData object .var or .obs contains gene ranking or score field(s) after sepal execution (exact field names require expert review)
- file_format_is: output is an AnnData-compatible object (.h5ad or in-memory AnnData instance) with sepal results attached

## Expert Review

- confirm the field names and data structure of gene rankings or scores match squidpy.gr.sepal documented output schema
- validate that score values are in expected range and represent meaningful gene importance rankings for the spatial dataset
