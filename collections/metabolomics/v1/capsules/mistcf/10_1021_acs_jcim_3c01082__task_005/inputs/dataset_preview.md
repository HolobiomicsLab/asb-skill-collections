### `figures/mist_cf_graphic.png`
_binary file, 54396 bytes_

### `paper.md`
```
# samgoldman97__mist-cf

## Introduction

#  MIST-CF: Metabolite Inference with Spectrum Transformers (Chemical Formula)

[![DOI](https://zenodo.org/badge/666904485.svg)](https://zenodo.org/badge/latestdoi/666904485)



This repository provides implementations and code examples for
[MIST-CF](https://www.nature.com/articles/s42256-023-00708-3), an extension of
[MIST](https://www.nature.com/articles/s42256-023-00708-3) for annotating MS1
precursor masses from MS/MS data in a _de novo_ setting. MIST-CF ranks chemical
formula and adduct assignments for an unknown mass spectrum using an end-to-end
energy based modeling approach, without referencing any spectrum databases.
Instead of computing fragmentation trees, MIST-CF adopts a formula transformer
neural network architecture and learns in a data dependent fashion.


Paper: [https://pubs.acs.org/doi/full/10.1021/acs.jcim.3c01082](https://pubs.acs.org/doi/full/10.1021/acs.jcim.3c01082)  

![Model  graphic](mist_cf_graphic.png)

We note several advances to the MIST-CF chemical formula transformer architecture over the original MIST chemical formula transformer that we plan to add back into the MIST model architecture used for fingerprint prediction in future work: 

1. Utilizing an internal chemical subformula assignment protocol (rather than SIRIUS fragmentation trees) 
2. Considering multiple adduct types beyond [M+H]+ (still only positive mode)
3. Utilizing sinusoidal *formula* embeddings as developed in our previous work [SCARF](https://arxiv.org/abs/2303.06470)
4. Emb

## Methods

_No usage/docs found._

## Results

_No examples found._

## Discussion

_No changelog found._

## References

- Source: github:samgoldman97__mist-cf
- Synthesized at: 2026-06-16T07:03:43+00:00
```
