# Data Preprocessing Code
## Description
The following jupyter notebooks documents some of the code I used to process the patent data that have been crawled by the Patent Crawler. Preprocessing of patent data (which is outputted as CSVs) is required for both the patent claim/abstract generators and the fake/real patent classifiers.

## Patent Claim/Abstract Generators
The preprocessing for text generation requires that the data is parsed and split into three data sets randomly: training, validation, and testing set. The csv file would then be fed to fine-tune the generation models.

## Fake/Real Patent Classifiers
This is a two-fold process: first, we need to retrieve the real patent data from the dataframe provided from the crawler; then, we need to generate fake patent data from the patent claim/abstract generators. This requires us to extract prompt words from the real patent data and then use those to generate fake patent data.

More information about the preprocessing steps are available in the main capstone report.



