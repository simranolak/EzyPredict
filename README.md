# EzyPredict

## Summary

The EzyPredict Dataset and code repository is an attempt to predict EC number of enzymes in the _Saccharomyces cerevisiae_ metabolic model from peptide sequence and protein propertied. It includes UniProtIDs, peptide statistics, ESM2 encodings, and Enzyme Commission labels (up to level 2). This dataset aims to train machine learning models to predict enzyme functions based on sequence and physicochemical properties. While not research-scale, it serves as a valuable exercise in enzyme function prediction. The dataset is limited to _S. cerevisiae_ and not suitable for generalization. It includes exploratory data analysis scripts using PCA and kPCA that were used to set the filtering criteria retrospectively for the datapreparation script. The final model training script trains a neural network with 75% accuracy to predict EC number upto level 2 using the input data.

The accuracy of different EC numbers varies. The dataset also has uneven class numbers which will be balanced in future iterations.




## Datasheets and Model Card

- datasheet for the curated dataset : EzyPredict/metadata/Datasheet_for_EzyPredict_Scerevisiae_dataset.pdf
- model card : EzyPredict/metadata/zyPredict_modelcard.md

## Code 

Run in the following sequence :

1 - EzyPredict_1_preparedata.ipynb

2 - EzyPredict_2_exploredata.ipynb

3 - EzyPredict_3_TrainMLmodel.ipynb

EzyPredict_HelperFunctions.py - contains functions imported by 1 and 2 to interconvert between identifiers, fetch ESM2 encodings and pepstats.

## Model Optimisation 

Bayesian Optimisation was carried out to optimise the number of neurons and learning rate of a simple neural network with one hidden layer

<img width="620" alt="Screenshot 2023-10-03 at 21 48 45" src="https://github.com/simranolak/EzyPredict/assets/19653603/89247062-c6f9-48e6-9cd9-68e16fe15d43">

### Before Optimisation : Overall Accuracy - 52.38%

![image](https://github.com/simranolak/EzyPredict/assets/19653603/27632bc7-6dc5-43ab-81e0-a552cc09ceb6)

![unoptimised simpleNN](https://github.com/simranolak/EzyPredict/assets/19653603/b6582ced-3acf-4415-a8fc-1ee54a04c14e)

### After Optimisation : Overall Accuracy 75.13%

![image](https://github.com/simranolak/EzyPredict/assets/19653603/6ca65afd-84ba-4f58-be85-81e45b854096)
![optimised simpleNN](https://github.com/simranolak/EzyPredict/assets/19653603/18fcea41-3f0f-4e4b-bd75-36a92e486f1d)


