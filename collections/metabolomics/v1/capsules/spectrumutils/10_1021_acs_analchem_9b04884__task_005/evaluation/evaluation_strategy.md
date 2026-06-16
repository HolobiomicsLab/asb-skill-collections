# Evaluation Strategy

## Direct Checks

- verify file exists: output PNG or SVG artifact from spectrum_utils.plot
- file_format_is: output artifact is valid PNG or SVG (byte-for-byte magic number check)
- script_runs: Python script successfully loads USI mzspec:PXD000561:Adult_Frontalcortex_bRP_Elite_85_f09:scan:1 using spectrum_utils
- script_runs: annotate_proforma method executes without exception when called with ion_types parameter including b and y ions
- output_matches_reference: rendered figure contains annotated b and y ion labels in the output artifact (robust to rendering engine variation in exact pixel placement)

## Expert Review

- visual inspection of rendered spectrum confirms b/y ion annotations are chemically plausible and positioned at correct m/z values
- expert assessment that annotated fragment ions follow ProForma 2.0 specification as claimed in package documentation
