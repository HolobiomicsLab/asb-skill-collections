# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] How does the nn_handler.create_batches() method operate when invoked with normalise_class=True versus normalise_class=False, and what are the structural differences in the resulting batch artifacts?: 'The `normalise_class` argument allows you to make sure every class has the same number of peaks for the training, when set to `True`, the number of peaks for each class will be equal to the smallest'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] When normalise_class is set to True, the create_batches() method ensures that every class has an equal number of peaks in the resulting training batches, with the total number of peaks per class equal to the smallest class count; when set to False, class counts remain unequal, reflecting the original distribution in the dataset.: 'The `normalise_class` argument allows you to make sure every class has the same number of peaks for the training, when set to `True`, the number of peaks for each class will be equal to the smallest'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Labeled LC-MS experiment object with raw mzML files and feature table (CSV format from mzMine or XCMS) containing 10–20 representative pooled samples and manually annotated peak labels (High_quality, Low_quality, Noise): 'create our experiment object and load the data, we can do that the exact same way as we have done before'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Training batch artifact (80% of peaks, class-imbalanced distribution): 'By default, the split between training:test:validation batches is 80:10:10'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Test batch artifact (10% of peaks, class-imbalanced distribution): 'By default, the split between training:test:validation batches is 80:10:10'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Validation batch artifact (10% of peaks, class-imbalanced distribution): 'By default, the split between training:test:validation batches is 80:10:10'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Training batch artifact with equal class counts (80% of normalized peaks, all classes equal to smallest class size): 'when set to `True`, the number of peaks for each class will be equal to the smallest'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Test batch artifact with equal class counts (10% of normalized peaks, all classes equal to smallest class size): 'when set to `True`, the number of peaks for each class will be equal to the smallest'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Validation batch artifact with equal class counts (10% of normalized peaks, all classes equal to smallest class size): 'when set to `True`, the number of peaks for each class will be equal to the smallest'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Verification report documenting per-class peak counts in each batch condition (normalise_class=False vs True): 'The `normalise_class` argument allows you to make sure every class has the same number of peaks for the training'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] NeatMS: 'NeatMS provides the necessary functions to do that, all we will have to do is create a `Neural network handler` object and call the batch creation method'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Python: 'open source python package'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog found.: 'No changelog found.'
