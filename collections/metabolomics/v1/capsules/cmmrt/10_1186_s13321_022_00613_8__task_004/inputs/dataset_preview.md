### `paper.md`
```
# constantino-garcia__cmmrt

## Introduction

# CMM-RT
This code implements methods for the accurate prediction of Retention Times 
(RTs) for a given Chromatographic Method (CM) using machine learning, as 
described in:

> García, C.A., Gil-de-la-Fuente, A., Barbas, C. et al. Probabilistic metabolite annotation using retention time prediction and meta-learned projections. J Cheminform 14, 33 (2022). https://doi.org/10.1186/s13321-022-00613-8. 



Highlights: 
* We have trained state-of-the-art machine learning regressors using the 80,038 
experimental RTs from the METLIN small molecule dataset (SMRT); both retained 
and unretained molecules were considered.
* 5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with
 the alvaDesc software. The models were trained using only the descriptors, 
 only the fingerprints, and both types of features simultaneously. Results suggest
 that fingerprints tend to perform better.
* The best results were obtained by a heavily regularized DNN trained with 
cosine annealing warm restarts and stochastic weight averaging, achieving a 
mean and median absolute errors of 39.2±1.2 s and 17.2 ± 0.9 s, respectively.
* A novel Bayesian meta-learning approach is proposed for RT projection between
 CMs from as few as 10 molecules while still obtaining competitive error rates 
 compared with previous approaches.
* We illustrate how the proposed DNN+meta-learned projections can be integrated into a 
metabolite annotati

## Methods

_No usage/docs found._

## Results

_No examples found._

## Discussion

_No changelog found._

## References

- Source: github:constantino-garcia__cmmrt
- Synthesized at: 2026-06-15T12:49:28+00:00
```
