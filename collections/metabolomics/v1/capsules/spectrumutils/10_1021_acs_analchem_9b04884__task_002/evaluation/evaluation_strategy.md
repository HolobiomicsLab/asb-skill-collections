# Evaluation Strategy

## Direct Checks

- verify file exists at public accession mzspec:MSV000079960:DY_HS_Exp7-Ad1:scan:30372
- script_runs: Python script that imports spectrum_utils.fragment_annotation, loads the spectrum via USI, calls annotate_proforma() with a valid ProForma 2.0 peptidoform string (default ion_types='by'), and returns annotated peaks
- output_matches_reference: annotated peak m/z values and ion type assignments (b or y) are consistent with theoretical fragment masses calculated from the ProForma peptidoform string, within specified fragment tolerance (no canonical answer — tolerance depends on instrument calibration and user specification)
- field_present: each annotated peak record contains at least 'mz', 'intensity', and 'ion_type' fields
- value_in_range: all annotated peak m/z values fall within the valid mass range for the given precursor and peptide sequence

## Expert Review

- verify that ProForma 2.0 specification parsing correctly handles any post-translational modifications (PTMs) present in the input peptidoform string, including Unimod references
- verify that b and y ion peak assignments are chemically plausible given the peptide sequence and spectrum properties (e.g., no spurious assignments at impossible neutral losses)
