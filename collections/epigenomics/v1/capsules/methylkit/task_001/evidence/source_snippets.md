# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] When differentially methylated bases are extracted from a methylDiff object using getMethylDiff() with q-value < 0.01 and 25% methylation difference thresholds, what are the counts of hyper-methylated versus hypo-methylated bases?: 'After q-value calculation, we can select the differentially methylated regions/bases based on q-value and percent methylation difference cutoffs. Following bit selects the bases that have'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Using getMethylDiff() with q-value < 0.01 and 25% methylation difference cutoffs on example methylKit data yields separate hyper-methylated and hypo-methylated base objects, which can be extracted by specifying type="hyper" or type="hypo" parameters.: 'myDiff25p.hyper=getMethylDiff(myDiff,difference=25,qvalue=0.01,type="hyper")
#
# get hypo methylated bases
myDiff25p.hypo=getMethylDiff(myDiff,difference=25,qvalue=0.01,type="hypo")'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] methylKit example CpG text files (methylation call format from bisulfite sequencing): 'Starting from the methylKit example CpG text files'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] methylDiff object containing differentially methylated bases with hyper- and hypo-methylated base counts: 'methylDiff object with hyper- and hypo-methylated base counts matching those reported in the vignette'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] methylKit: 'title: "methylKit: User Guide v`r packageVersion('methylKit')`"'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] R: 'packageVersion('methylKit')'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog found: '_No changelog found._'
