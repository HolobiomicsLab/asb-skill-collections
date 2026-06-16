# Evaluation Strategy

## Direct Checks

- verify that the adduct computation module accepts a derivatizing matrix identifier (e.g., 'FMP-10') and a metabolite SMILES string as inputs
- verify that the module returns a structured list or table of predicted adduct ions with their m/z values
- verify that output includes adducts beyond [M+H]+ and [M-H]- (e.g., [M+Na]+, [M+K]+, or matrix-specific adducts)
- verify script runs without errors on a test case with FMP-10 and a standard metabolite SMILES
- output matches reference adduct masses for FMP-10 reported in Nature Methods paper — robust to minor mass tolerance (±0.01 Da or ±10 ppm, multiple defensible tolerances acceptable)

## Expert Review

- verify that predicted adduct ions are chemically plausible for the given derivatizing matrix FMP-10
- verify that fragmentation or ionization logic follows established mass spectrometry principles for the matrix type
- assess whether adduct coverage is complete relative to known FMP-10 ionization pathways in the referenced Nature Methods study
