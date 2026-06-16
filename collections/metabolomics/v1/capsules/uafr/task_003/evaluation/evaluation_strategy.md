# Evaluation Strategy

## Direct Checks

- verify file exists at github:castratton__uafR containing categorate() function implementation
- verify categorate() function accepts structural-match condition parameter (COND-categorate-structural-match)
- verify 4-set restricted chemical library file exists and is loadable in R (format: CSV or RData)
- script_runs: execute categorate() with structural-match condition on 4-set library; verify output is a dataframe with no errors
- output includes rows for Ethyl hexanoate and isobutyl hexanoate
- output dataframe contains a column indicating structural similarity or classification type (e.g., 'Type', 'structural_class', 'match_type')
- value in dataframe row for Ethyl hexanoate matches value in row for isobutyl hexanoate in the structural similarity/type column
- output dataframe row(s) contain 'Type D' or equivalent classification label as specified in METRIC-structural-match-ethylhex-typeD

## Expert Review

- expert_review: assess whether the structural similarity metric and Type D classification are chemically defensible for the Ethyl hexanoate–isobutyl hexanoate pair (both are aliphatic esters; isobutyl vs. ethyl ester groups differ only in branching of the alcohol moiety)
- expert_review: confirm that the 4-set restricted chemical library composition and molecular structure definitions are appropriate for testing structural-match functionality and consistent with METRIC-structural-match-ethylhex-typeD
