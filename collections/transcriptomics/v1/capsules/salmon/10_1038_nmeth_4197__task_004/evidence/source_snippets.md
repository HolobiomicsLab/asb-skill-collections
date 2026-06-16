# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Does the mapping rate and NumReads Pearson correlation remain stable when the Rust mapper uses alternative seed representations (sparse fixed-k anchors, reference k-mer variants) instead of the default unitig-constrained approach?: 're-running the Rust mapper with sparse fixed-k anchors, reference-extended MEMs, and true unitig-constrained uni-MEMs'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] On byte-identical index, NumReads Pearson correlation between C++ and Rust is 0.99854, demonstrating high quantitative agreement across implementations and seed strategies.: 'NumReads Pearson | 0.99854'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] GEUVADIS ERR188044 paired-end 76 bp reads (36.35M reads): 'Reads: GEUVADIS ERR188044 (36.35M 76bp PE)'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Byte-identical GRCh38 cDNA reference index (193,759 transcripts): 'byte-identical index — both tools' indices built from the same clean.fa (deterministic non-ACGT replacement, identical 193,759-transcript set)'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Mapping rate (%) for default seed representation: 're-running the Rust mapper with sparse fixed-k anchors, reference-extended MEMs, and true unitig-constrained uni-MEMs gave identical results (85.55%, NumReads r ≥ 0.99999995)'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Mapping rate and NumReads Pearson r for sparse fixed-k anchor variant: 'sparse fixed-k anchors, reference-extended MEMs, and true unitig-constrained uni-MEMs gave identical results (85.55%, NumReads r ≥ 0.99999995)'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Mapping rate and NumReads Pearson r for reference-extended MEM variant: 'sparse fixed-k anchors, reference-extended MEMs, and true unitig-constrained uni-MEMs gave identical results (85.55%, NumReads r ≥ 0.99999995)'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Mapping rate and NumReads Pearson r for unitig-constrained uni-MEM variant: 'sparse fixed-k anchors, reference-extended MEMs, and true unitig-constrained uni-MEMs gave identical results (85.55%, NumReads r ≥ 0.99999995)'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Summary table with per-variant mapping rate and Pearson r values: 'identical results (85.55%, NumReads r ≥ 0.99999995)'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] salmon 2.0: 're-running the Rust mapper with sparse fixed-k anchors, reference-extended MEMs, and true unitig-constrained uni-MEMs'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] piscem-rs: 'The Rust port (built on piscem-rs, which derives orientation correctly) was right all along'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No quantitative mapping rate or NumReads Pearson results are reported for alternative seed representations (sparse fixed-k anchors, reference k-mer variants) on ERR188044.: 'On our benchmarks (human GEUVADIS `ERR188044` against a GRCh38 cDNA index, and yeast `ERR458493`), selective-alignment quantification reproduces C++ salmon to per-transcript Pearson ≈ 0.999'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] The discussion reports per-transcript Pearson ≈ 0.999 but does not specify the NumReads Pearson correlation or mapping rate achieved under the tested seed variants.: 'SA quantification agrees at Pearson 0.999 and the entire mapping-rate delta is explained by (1) one describable orphan/post-merge pruning default that is off-by-default in Rust, and (2) benign'

## ev_014

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] No methodological details are provided on how alternative seed representations (sparse fixed-k anchors, reference k-mer variants) were generated or parameterized for the experiment.: 're-running the Rust mapper with sparse fixed-k anchors, reference-extended MEMs, and true unitig-constrained uni-MEMs'
