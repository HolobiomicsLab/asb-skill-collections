# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] How does Met-ID compute expected adduct ions for metabolites when using derivatizing matrices like FMP-10, beyond the standard [M+H]+ and [M-H]- ions?: 'Met-ID has a particular focus on derivatizing matrices leading to other ions than the common [M+H]+ in positive mode and [M-H]- in negative mode.'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Met-ID is designed to handle derivatizing matrices such as FMP-10, which produce ions other than the common [M+H]+ in positive mode and [M-H]- in negative mode, and the software is extendable to use any derivatizing matrix.: 'As [FMP-10](https://www.nature.com/articles/s41592-019-0551-3) was developed in house, it features heavily in the software, however, this is mostly to show the point at which to start as Met-ID is'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Metabolite SMILES string and derivatizing matrix identifier (e.g., FMP-10): 'given a derivatizing matrix (e.g. FMP-10) and a metabolite SMILES'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Reference FMP-10 adduct mass dataset from Nature Methods paper: 'Evaluation is against known FMP-10 adduct masses published in the referenced Nature Methods paper'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Predicted adduct ions table with adduct formula, mass shift, m/z value, and ionization state: 'computes the expected adduct ions beyond [M+H]+ and [M-H]-'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Validation report comparing predicted adduct masses to reference FMP-10 values: 'Evaluation is against known FMP-10 adduct masses published in the referenced Nature Methods paper'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] RDKit: 'Powered by RDKit'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog provided; cannot trace evolution of adduct computation component or verify stability of the implementation.: '_No changelog found._'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] The specific Nature Methods paper containing reference FMP-10 adduct masses is not cited or linked in the provided section text.: 'References — Source: github:pbjarterot__Met-ID'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No explicit description of the adduct computation algorithm, matrix-specific ionization rules, or expected output format is present in the provided section text.: '_No changelog found._'
