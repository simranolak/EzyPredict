# EzyPredict
predicting EC numbers from protein data of _Sacchromyces cerevisiae_ enzymes

The EzyPredict Dataset and code repository is an attempt to predict EC number of enzymes in the _Saccharomyces cerevisiae_ metabolic model from peptide sequence and protein propertied. It includes UniProtIDs, peptide statistics, ESM2 encodings, and Enzyme Commission labels (up to level 2). This dataset aims to train machine learning models to predict enzyme functions based on sequence and physicochemical properties. While not research-scale, it serves as a valuable exercise in enzyme function prediction. The dataset is limited to _S. cerevisiae_ and not suitable for generalization. It includes exploratory data analysis scripts using PCA and kPCA that were used to set the filtering criteria retrospectively for the datapreparation script. The final model training script trains a neural network with 75% accuracy to predict EC number upto level 2 using the input data.

The accuracy of different EC numbers varies. The dataset also has uneven class numbers which will be balanced in future iterations.




Datasheets and Model Card are available in :

datasheet for the curated dataset : EzyPredict/metadata/Datasheet_for_EzyPredict_Scerevisiae_dataset.pdf
model card : EzyPredict/metadata/zyPredict_modelcard.md

To run the code run :

1 - EzyPredict_1_preparedata.ipynb

2 - EzyPredict_2_exploredata.ipynb

3 - EzyPredict_3_TrainMLmodel.ipynb


Bayesian Optimisation was carried out to optimise the network
![image](https://github.com/simranolak/EzyPredict/assets/19653603/b37aace2-3889-4117-a531-e0bbc5144ce0)


Before Optimisation : Overall Accuracy - 52.38%


![image](https://github.com/simranolak/EzyPredict/assets/19653603/a1d38423-f72b-4691-99ea-f5580596ba99)


After Optimisation : Overall Accuracy 74.6%

![image](https://github.com/simranolak/EzyPredict/assets/19653603/ecab7158-2b7d-4e26-9ec0-7683ecc5a671)



