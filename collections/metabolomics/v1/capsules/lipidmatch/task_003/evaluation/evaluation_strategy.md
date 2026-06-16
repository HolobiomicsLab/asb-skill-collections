# Evaluation Strategy

## Direct Checks

- file_exists: verify that the GitHub repository github:GarrettLab-UF__LipidMatch is accessible and contains documentation or source code listing instrument/vendor and acquisition mode support
- contains_substring: in repository documentation or README, verify presence of explicit mentions of each of the four validated instrument/vendor types (Q-Exactive, Agilent Q-TOF, Bruker Q-TOF, SCIEX Q-TOF)
- contains_substring: in repository documentation, verify presence of explicit mention of at least three acquisition mode types from the set {targeted, ddMS2-topN, AIF, direct infusion, imaging}
- contains_substring: in repository documentation, verify presence of explicit statement that Waters is unsupported or not currently supported
- output_matches_reference: constructed table row count equals number of valid instrument/vendor and acquisition mode combinations documented in source material (no canonical answer — dependent on what combinations are explicitly documented as tested/validated vs. inferred)

## Expert Review

- assess whether the source documentation provides sufficient detail to distinguish between 'tested and validated,' 'applied,' and 'potentially supported but not documented' for each instrument/vendor × acquisition mode pair
- determine whether direct infusion and imaging modes should be attributed to specific instrument/vendor combinations or listed as general capabilities across vendors
- verify that the single documented unsupported case (Waters) is correctly identified and that no other vendor/instrument combinations are negated in the source material
