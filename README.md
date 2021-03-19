# Minerva Capstone Project: Patent Claim and Abstract Generation
## Author: Jason Liang
## Advisor: Prof. Watson
### Abstract
Patent is a form of intellectual property that aims to protect an invention developed by one or a group of innovators so they are rewarded some form of “monopoly” over that particular invention for an extended period of time within a geographical location. In order to obtain such a protection, innovators have to draft a patent application to the patent office, the granting of the patent depends significantly on the wording in the claims of the patent which relates to the scope of protection of the innovation. The goal of the study is to build a Natural Language Processing model that learns from how patent claims are normally written and, given information about a particular field of patents (according to the CPC classification), generate pseudo-patent claims that resembles patent claims that would have been written for the technology. There are two parts to this project: the data collection using a web crawler and the model. I will first complete the web crawler and start collecting data from the database for one specific classification. Once sufficient amounts of data is collected, I will begin building my model (some kind of encoder-decoder model) and train the model.

### Description of the Github Repository
This repository includes the technical components necessary to enable the project. Each folder in this project represents a particular component of the project and will be referred to in the write-up component of the project. The folders are as follows:

* [Tutorials](./Tutorials)
* [Web Crawler](./PatentSpider)
* [Data Processing Related](./Data%20Processing%20Related)
* [Patent Claim/Abstract Generator](./Patent%20Claim%20Generator)
* [BERT Text Classification](./BERT%20Text%20Classification)
* [Experiments](./Experiments)

Data Processing Related folder includes all code related to pre-processing of the Data. The tutorials are tutorials I consulted to learn more about how to train similar models, these are indications of the work I put into to learn more about the field and how best to implement these models. The web crawler is the first component of the project. It includes all the code of the web crawler I built to collect patent data from the USPTO database. The Patent Claim/Abstract Generator includes the notebooks that fine-tune patent claims and abstracts. This is the bulk of the project and will include code used for the experiments of the project. The BERT Text Classification includes the code for pre-processing and training a text classifier for real and fake patent data. This classifier is used as a metric to evaluate how well the text generators perform. Finally, the Experiments section includes all the code for the experiments.




