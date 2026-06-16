# Evaluation Strategy

## Direct Checks

- verify file standard_data.csv exists in github:castratton__uafR repository
- verify mzExacto() function is defined and callable in the uafR R package from github:castratton__uafR
- verify output of mzExacto(standard_data.csv, query_chemicals=COND-known-chemicals-explicit) is a single dataframe
- verify dataframe contains columns for m/z, retention time, match factor, and area (exact column names must be confirmed against article/code)
- verify dataframe row for Ethyl hexanoate contains m/z value matching article-reported value
- verify dataframe row for Methyl salicylate contains retention time value matching article-reported value
- verify dataframe row for Octanal contains match factor value matching article-reported value
- verify dataframe row for Undecane contains area value matching article-reported value

## Expert Review

- confirm that the four compounds (Ethyl hexanoate, Methyl salicylate, Octanal, Undecane) are present in COND-known-chemicals-explicit input list and are chemically appropriate test cases for mzExacto()
- confirm that reported m/z, retention time, match factor, and area values in article represent the correct expected outputs for these compounds under the stated input conditions
- assess whether mzExacto() function behavior and return structure align with the documented intent in the methods section
