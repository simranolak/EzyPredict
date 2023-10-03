# EzyPredict Dataset

As far as you can, complete the model datasheet. If you have got the data from the internet, you may not have all the information you need, but make sure you include all the information you do have. 

## Motivation

The purpose of this dataset is to train a machine learning model to predict the function (Enzyme Commission number up to level 2) of an enzyme based on its sequence and physicochemical properties. This small dataset was created as an exercise during a course and is not a research-scale or deployment scale dataset or implementation fit for the purpose of prediction enzyme function in general. Much larger datasets are required for that.

Created by : Simran Kaur Aulakh in Sept - October 2023.
 
## Composition

Total Entries: 944

Features: 1292 ( 1291 inputs + 1 output)

## Collection process

The dataset was created by sourcing ORF (Open Reading Frame) IDs from the Yeast8 model, converting these to UniProtIDs, then using sequences of each UniProtID to : 

-   Fetch peptide biophysical and biochemical data using the pepstats API (https://www.ebi.ac.uk/Tools/seqstats/emboss_pepstats/). Only the following were retained : 
        Isoelectric Point
        Fraction of amino acids classified as each of the following categories : 
        - Tiny
        - Small
        - Aliphatic
        - Aromatic
        - Non-polar
        - Polar
        - Charged
        - Basic
        - Acidic

-   Fetch Enzyme Commission (EC) numbers for functional annotation using a Uniprot download file (“uniprot2EC_uniprotkb_download_2023_09_07.tsv”). Only the first 2 levels of EC numbers were considered.
Convert protein sequences into ESM2 Encodings: Protein sequences were encoded using the ESM2 model,transforming them into fixed-size vectors representing the sequence. Peptides longer than 1024 amino acids were discarded for this training exercise.

Raw data : all raw data files created during the preprocessing were saved and are also provided in the repository

## Preprocessing/cleaning/labelling

- Was any preprocessing/cleaning/labeling of the data done (e.g., discretization or bucketing, tokenization, part-of-speech tagging, SIFT feature extraction, removal of instances, processing of missing values)? If so, please provide a description. If not, you may skip the remaining questions in this section. 
- Was the “raw” data saved in addition to the preprocessed/cleaned/labeled data (e.g., to support unanticipated future uses)? 

## Ethical Review
 The dataset contains no data from humans.
All databases and software accessed for the creation of the dataset are under open licences, free for usage by anyone in the public. All sources have been cited.


## Uses

This dataset can be used for:
- Training machine learning models to predict enzyme function of _S. cerevisiae_  enzymes as a learning exercise
- Studying correlations between protein sequence properties and their function.

This dataset should not be used for:
- Extrapolating the results to other organisms
- High-confidence prediction of enzyme function in _S. cerevisiae_ 
- Predictions of non enzymatic protein function


## Distribution

The dataset can be accessed through the project’s Github repository : https://github.com/simranolak/EzyPredict. It’s a private repository so access will be provided upon request

UniProt - Creative Commons (CC BY 4.0 LIcence)  (https://www.uniprot.org/help/license )
Pepstats - Creative Commons (CC0 Licence)  (https://www.ebi.ac.uk/licencing) 
ESM2 - under MIT licence - open for any copying, modification and use without any liability or warranty on the part of facebook research. (https://github.com/facebookresearch/esm/blob/main/LICENSE) 

## Maintenance

The dataset can be updated as new protein sequences get added to UniProt or when updates are made to the pepstats tool or the ESM2 model.
All data collection scripts are included in the repository. 
UniProt and Pepstats are mainted by EMBL-EBI (https://www.ebi.ac.uk/).
ESM2 model is mainted by Meta / Facebook Research
