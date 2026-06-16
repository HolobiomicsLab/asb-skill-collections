### `paper.md`
```
# BioNet-XMU__DeepION

## Introduction

# DeepION
DeepION is a deep learning-based low-dimensional representation model of ion images for mass spectrometry imaging. In this model, two modes of DeepION, denoted as “COL” and “ISO” are designed for the cases of regular co-localized ions from different molecules and isotope ions from a same molecule respectively. Developer is Lei Guo from Laboratory of Biomedical Network, Department of Electronic Science, Xiamen University of China.

# Overview of DeepION
<div align=center>
<img src="https://github.com/gankLei-X/DeepION/assets/70273368/7aab5832-d2e9-448c-838c-6f697993aa2f" width="800" height="480" /><br/>
</div>

__Schematic overview of DeepION consisting of four modules.__ (1) Data Augmentation module. The original ion image is first imported into the data augmentation module "T"  to generate two augmented images, where the T_COL including color jitter, filtering, Poisson noise, and random missing value is carried in COL mode, while T_ISO introduces an additional process of intensity-dependent missing value in ISO mode. (2) Encoder module. Two augmented images are propagated through a pair of ResNet18-based encoders that shared parameters, then output two 512-dimensional representation vectors. (3) Projection module and Prediction module are used to avoid collapsing solutions during the optimization process of maximizing the similarity between two augmentations from a same image and ensure to learn the meaningful representation vectors. A contrastive loss is employed 

## Methods

_No usage/docs found._

## Results

_No examples found._

## Discussion

_No changelog found._

## References

- Source: github:BioNet-XMU__DeepION
- Synthesized at: 2026-06-15T13:51:23+00:00
```
