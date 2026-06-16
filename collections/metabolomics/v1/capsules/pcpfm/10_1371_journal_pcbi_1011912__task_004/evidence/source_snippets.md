# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] How does the build_empCpds command construct empirical compound groups from a feature table using khipu with configurable mz and retention time tolerances?: 'EmpCpds are groups of associated features, typically isotopes and adducts, that belong to the same tentative compound and co-elute if there is chromatography. The set of adducts and isotopes can be'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] The build_empCpds command groups features into empirical compounds by matching isotopes and adducts with configurable mz tolerance (default 5 ppm) and rt tolerance (default 2 seconds), producing a JSON file containing grouped features with their mz and rt values.: 'An example command for building the empCpds is: `pcpfm build_empCpds --table_moniker preferred --empCpd_moniker preferred -i ./my_experiment` ... Options can be provided including:'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] preferred feature table (TSV from asari processing): 'EmpCpds are groups of associated features, typically isotopes and adducts, that belong to the same tentative compound and co-elute if there is chromatography.'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] ionization mode (positive or negative) inferred from experiment metadata: 'This command will infer the correct ionization mode for the experiment which will persist through out processing'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] optional adduct configuration files (JSON) for positive and negative modes: 'khipu_adducts_pos: a path to .json file containing adduct information for positive mode / khipu_adducts_neg: a path to .json file containing adduct information for negative mode'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] empCpd.json file containing empirical compound groups with fields: list_of_features, mz, rt, adduct annotations, and isotopologue assignments: 'EmpCpds are saved to moniker similar to feature tables.'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] experiment.json updated with empCpd moniker and metadata: 'The experiment object will be used throught the processing and store intermediates.'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] khipu: 'pre-annotation to group featues to empirical compounds (khipu)'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Python: 'Python-Centric Pipeline for Metabolomics'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog or version history found: '_No changelog found._'
