# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Do the 200-dimensional spectral embeddings learned by MS2DeepScore encode chemically meaningful information that enables molecules of the same chemical class to cluster together in low-dimensional space?: 'we used the MS2DeepScore base network (Fig. 1) to compute the 200-dimensional spectral embeddings for all 3601 spectra in the test set. Using the t-SNE [28] implementation from scikit-learn [29] we'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Molecules of the same chemical superclass consistently cluster together in t-SNE visualizations of MS2DeepScore embeddings, and this pattern holds at finer resolution for chemical subclasses, confirming that embeddings contain chemically meaningful molecular features.: 'Molecules of the same chemical class tend to cluster together in the resulting t-SNE plot, confirming that the MS2DeepScore embeddings represent chemically meaningful molecular features.'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Trained MS2DeepScore model weights and architecture: 'The fully trained model used to create Fig. 2, 4, 5, 7, 8 can be downloaded from zenodo: https:// zenodo. org/ record/ 46993 56'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Test-set MS/MS spectra (3,601 spectra with 500 unique InChIKeys in positive ionisation mode): 'test set (3601 spectra of 500 unique InChIKeys)'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Chemical structure annotations (InChIKey, SMILES, InChI) for test-set molecules: 'The full cleaned dataset (210,407 spectra, 184,698 annotated with InChIKey and SMILES and/or InChI) can be found on zenodo'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Comma-separated or tab-separated table with columns: spectrum_id, t-SNE_x, t-SNE_y, InChIKey, ClassyFire_superclass: 'we used the MS2DeepScore base network (Fig. 1) to compute the 200-dimensional spectral embeddings for all 3601 spectra in the test set'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Scatter plot visualization (PNG or PDF) showing t-SNE 2D coordinates coloured by ClassyFire chemical superclass: 'For Fig. 8, we used the MS2DeepScore base network (Fig. 1) to compute the 200-dimensional spectral embeddings for all 3601 spectra in the test set. Using the t-SNE [28] implementation from'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] MS2DeepScore: 'we used the MS2DeepScore base network (Fig. 1) to compute the 200-dimensional spectral embeddings'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] scikit-learn: 'Using the t-SNE [28] implementation from scikit-learn [29] we computed two-dimensional coordinates'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Python: 'Our MS2DeepScore Python library offers two types of data generators'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] RDKit: 'we used Tanimoto scores on RDKit [23] Daylight fingerprints (2048 bits) to compute structural similarities'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No explicit statement of which t-SNE hyperparameters (perplexity, learning rate, number of iterations) were used or recommended for reproduction: 'Using the t-SNE [28] implementation from scikit-learn [29] we computed two-dimensional coordinates'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No specification of how ClassyFire chemical superclass labels were assigned or retrieved for the 3601 test-set spectra: 'MS2DeepScore can infer structural similarities between fragmentation mass spectral pairs'

## ev_014

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No quantitative metric (e.g., silhouette coefficient, Davies-Bouldin index, or clustering purity) reported to formally evaluate the degree of chemical class clustering in the t-SNE embedding: 'MS2DeepScore is very fast and scalable. We conclude that this makes MS2DeepScore a powerful novel tool for running large scale comparisons and analyses'

## ev_015

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No information on runtime or computational cost to extract embeddings and perform t-SNE reduction on the 3601 test spectra: 'MS2DeepScore is very fast and scalable.'
