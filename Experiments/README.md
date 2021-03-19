# Experiments
## Description
This folder contains all the experiments conducted to test the hypothesis that with more fine-tuning epochs, patent claim and abstract generation models would generate . The code in this folder corresponds to section 6.3.4 ("Text Classification Results With More Fine-tuning Steps") and produced visualizations used in the section.

Within each folder, we have the following notebooks corresponding to the abstract and claim generation models:
- Patent Abstract/Claim Generation (number of fine-tuning epochs)
- Fake and Real Patents Data Set (Number of fine-tuning epochs, Abstract/Claim)
- Text Classifier Bert Preprocessing (Number of fine-tuning epochs, Abstract/Claim)
- BERT Patent Abstract/Claim Classification

The Patent Abstract/Claim Generation is the code used to fine-tune the generation models and save the models.

The Fake and Real Patents Data Set is the code used to generate the synthetic dataset used in the BERT classification model fine-tuning.

The Text Classifier Bert Preprocessing notebooks preprocesses the synthetic dataset and split the dataset into training, validation, and test sets that are inputted in the BERT Text Classification Model.

Finally, the BERT Patent Abstract/Claim Classification notebooks fine-tuned the BERT classification models to classify between real and fake patent data.
