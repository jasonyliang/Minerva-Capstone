# BERT Text Classification
## Description

## Colab
As fine-tuning and model training, in general, requires a lot of training time and computation power, as well as concerns of cost with cloud computing platforms, instead of running training on a local computer that only supports CPU or relying on cloud services, the study decides to rely on Google Colaboratory’s (Colab) free Jupyter notebook environment, which offers GPUs during training if necessary. Using the GPU options in the environment allows for much faster training time at no cost (even though GPU resources may still be limited), allowing the study to circumvent the constraint of financial and computational resources. While most of the code would be conducted on Colab, the code will be available in a Github repository in the forms of Jupyter notebook that can be accessed locally. 

While the code in the repo are presented as jupyter notebooks that could be ran locally (although the directories need to be structured and rerouted to the path of where you store your data), these notebooks were ran through Colab, where GPUs are available. I would advise potential users of the code to upload the notebooks to Colab to play around with the code.

## Libraries
Similar to the Patent Claim/Abstract Generators, we will be using and fine-tuning the BERT pre-trained models from Hugging Face's Transformer Library. Since we are not trying to build the best text classifier that has the best performance but rather to build a model that could provide a standard metric, I use simply the 'bert-base-uncased' model.

## Fine-Tuning
For standardized purposes, I fine-tune the classification model for just 5 training epochs and save the model iteration with the best validation loss.

The text classification model will be fine-tuned using a dataset that mixes real patent data (the same data used to fine-tune the patent claim generator) and fake patent data that are labeled. The synthetic dataset is then split into a training set, a validation set, and a test set. During the training of a predefined number of epochs, we save the version of the model that has the lowest loss on the validation step. The accuracy is then calculated by using the model to predict the labels of the test set. The higher the accuracy, the more able the classifier is able to distinguish between the real and fake patent claims, indicating that the text generator is not performing as well. If the classifier has a low accuracy (close to 50\%) it means that the classifier struggles with distinguishing between fake and real patent claims, giving us confidence in our text generation model.

The process for generating the synthetic data is available in `Fake_and_Real_Claims_Data_Set.ipynb` and `Fake_and_Real_Patents_Data_Set_(Abstract).ipynb`. Here, we use the models and model parameters generated from the patent claim/abstract generators to generate fake claims and abstracts that we then supply to the dataset.

To ensure that the metrics are comparable between different models, the study keeps the hyperparameters of the model (the base model, the learning rate, and the number of epochs) constant. Achieving high accuracy in the text classification model is not a priority of this project, in fact, the study looks for a text generation model that has a lower accuracy when being classified. For each text generation model, we produce the synthetic dataset using the model and use the dataset to fine-tune the text classification model to find the classification accuracy. We set the learning rate to `1e-5` and `5` training epochs.

