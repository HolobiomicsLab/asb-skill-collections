# Evaluation Strategy

## Direct Checks

- verify file S.griseus_fragment.fasta exists in package
- verify file significant_matches.tsv exists in MetaMiner output directory after execution
- verify significant_matches.tsv contains substring 'AmfS'
- verify significant_matches.tsv contains substring 'TGSQVSLLVCEYSSLSVVLCTP' (AmfS core peptide)
- script_runs: MetaMiner command executes without fatal errors on bundled inputs with lantibiotic class search mode
- verify output file format_is TSV (tab-separated values) with header row present

## Expert Review

- AmfS entry in significant_matches.tsv has statistically significant score threshold appropriate for lantibiotic RiPP detection
- reported AmfS match quality and e-value are consistent with true positive RiPP identification
