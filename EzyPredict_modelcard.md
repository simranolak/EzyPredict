# Model Card

## Model Description

**Input:** The model accepts an input feature vector of length 1291, which comprises:

UniProtID: A unique identifier for each protein sourced from UniProt.
Pepstats Features: Biochemical and biophysical properties of the protein including:
Isoelectric Point
Fraction of amino acids classified under categories like Tiny, Small, Aliphatic, Aromatic, Non-polar, Polar, Charged, Basic, and Acidic.
Encodings: A 1028-column vector derived from the ESM2 model representing the encoding for protein sequences.

**Output:**
The model predicts the EC number (Enzyme Commission number) up to level 2, which denotes the function of the protein.

**Model Architecture:** The model is based on a simple feedforward neural network with the following architecture:

Input Layer: Number of neurons equals the number of input features.
Hidden Layer: Consists of 100 neurons and uses ReLU (Rectified Linear Unit) as the activation function.
Output Layer: Number of neurons corresponds to the number of classes (n_classes). The exact number of classes is not specified in the provided information.

## Performance
Accuracy on whole dataset : 75% 

## Limitations

Limited to use for S.cerevisiae and learning how to make an ML model.

Limited to use on sequences less than 1024 amino acids. Sequence trimming and sliding window approaches were tested but led to artefacts in the encodings. Therefore, sequences longer than 1024 amino acids have just been left out. Further work needs to be done to figure out how to include them.

## Trade-offs

Performance vs. Data Complexity: While the dataset contains a mix of protein physicochemical properties and sequence encodings, it's limited to S. cerevisiae. This specificity might lead to good performance on similar S. cerevisiae data but might not generalize well to other organisms

Depth of EC Number Prediction: The model predicts EC numbers up to level 2. This might not provide a very detailed functional classification for certain enzymes.