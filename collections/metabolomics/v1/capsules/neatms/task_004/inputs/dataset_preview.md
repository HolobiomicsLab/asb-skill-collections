### `figures/ADAP_threshold_all_vs_recall_training_500.png`
_binary file, 24231 bytes_

### `figures/ROC_recall_High_vs_all.png`
_binary file, 7925 bytes_

### `figures/Screenshot 2020-04-28 at 16.43.33.png`
_binary file, 56331 bytes_

### `figures/annotation_tool.png`
_binary file, 53552 bytes_

### `figures/recall_table.png`
_binary file, 16823 bytes_

### `paper.md`
```
# bihealth__NeatMS

## Introduction

# NeatMS
[![PyPI version](https://img.shields.io/pypi/v/NeatMS?color=brightgreen&label=pypi%20package)](https://pypi.org/project/NeatMS/) [![install with bioconda](https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg?style=flat)](http://bioconda.github.io/recipes/neatms/README.html) [![Documentation Status](https://readthedocs.org/projects/neatms/badge/?version=latest)](https://neatms.readthedocs.io/en/latest/?badge=latest) [![License MIT](https://img.shields.io/pypi/l/NeatMS?color=brightgreen)](https://github.com/bihealth/NeatMS/blob/master/LICENSE)



## Methods

# Hyperparameter optimization

This the last step before we can used our newly trained model to classify peaks from other datasets. In this section, we will not only see how to use the automated method NeatMS provides to optimize the target parameter, but we will also explain the impact this parameter has on the classifier and how we can set it manually.

The last layer of the neural network uses a softmax activation function, which means that the output of the network is a probability distribution of 3 probabilities between 0 and 1, all of them adding up to 1 (3 is number of classes, we have one probability per class). The most simple approach would be to label the peak with the label corresponding to the highest probability returned by the model, but we can also investigate these probabilities and their impact on the prediction. We will particularly focus on the probability that corresponds to the `High quality` class and see how it impacts the prediction of the validation set (which remains untouched so far).

> You can follow the same approach using other classes than `High quality`. However, as `High quality` is the default class used in NeatMS, we will only cover this case here.

Calling the method `get_threshold()` will compute and return the optimal threshold using the validation set that you can then pass everytime you use this neural network. 
…[truncated]
```
