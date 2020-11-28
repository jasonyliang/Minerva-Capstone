# Patent Claim Generator
## Description
This section contains the code for fine-tuning GPT-2 Text Generation models for patent claims and abstracts. This is the second component of the capstone project where I use patent data collected using the web crawler to fine-tune a text generation model to produce patent claims.


## Colab
As fine-tuning and model training, in general, requires a lot of training time and computation power, as well as concerns of cost with cloud computing platforms, instead of running training on a local computer that only supports CPU or relying on cloud services, the study decides to rely on Google Colaboratory’s (Colab) free Jupyter notebook environment, which offers GPUs during training if necessary. Using the GPU options in the environment allows for much faster training time at no cost (even though GPU resources may still be limited), allowing the study to circumvent the constraint of financial and computational resources. While most of the code would be conducted on Colab, the code will be available in a Github repository in the forms of Jupyter notebook that can be accessed locally. 

While the code in the repo are presented as jupyter notebooks that could be ran locally (although the directories need to be structured and rerouted to the path of where you store your data), these notebooks were ran through Colab, where GPUs are available. I would advise potential users of the code to upload the notebooks to Colab to play around with the code.

## Libraries
Hugging Face's open-source Transformer library contains various transformer models and datasets that enable developers to build on their work and build their own models for a variety of NLP tasks.

The present study uses the pre-trained models set up by the hugging face Transformers as their pre-trained models are backed by Python deep learning libraries such as Pytorch and TensorFlow. The pre-train models provided by hugging face allow users to access their models to conduct tasks from text summarization to text generation; their APIs also allow for fine-tuning of their models.

This study uses hugging face’s API to fine-tune the GPT-2 model with patent data collected during the data collection phase of the project. Given a predefined number of fine-tuning epochs and data, the study is able to rely on hugging face’s fine-tuning code to fine-tune the GPT-2 models that produce, instead of plain written text, patent claims. The study looked at text generation in both patent claims and patent abstracts to evaluate how well the current NLP models are able to produce fabricated versions of the two and whether it is more capable of doing one over the other. Since the number of epochs used to fine-tune the model will impact the quality of the generated text, the study will also try to produce fine-tuned models with different training epochs and evaluate them for comparison.

## Fine-Tuning
To fine-tune a GPT-2 model using the Transformer library, we can use the `run_language_modeling.py` file from the library:

```
!wget https://raw.githubusercontent.com/huggingface/transformers/master/examples/contrib/legacy/run_language_modeling.py
```

Using the code contained in this file, we can run to fine-tune our model:
```
python run_language_modeling.py
        --output_dir=$OUTPUT_DIR
        --model_type=gpt2
        --model_name_or_path=$MODEL_NAME
        --do_train
        --train_data_file=$TRAIN_FILE
        --do_eval
        --eval_data_file=$TEST_FILE
        --per_gpu_train_batch_size=1
        --save_steps=-1
        --num_train_epochs=2
```
The parameter `num_train_epochs` determines the number of fine-tuning epochs we take, given the number of epochs we fine-tune for, our generated outputs can look very different. This is the main focus of our experiments to help determine the optimal number of epochs needed to generated good patent claims and abstracts.

The saved parameters and tokenizers would then be saved in the `$OUTPUT_DIR` you specified.

## Sample Claims
Using the model files, you can use the following code to generate fake patent claims and abstracts:
```
OUTPUT_DIR = # directory where you store the model parameters
device = 'cpu'
if torch.cuda.is_available():
    device = 'cuda'
# we use the GPT-2 model to load our fine-tuned model and get the tokenization
tokenizer = GPT2Tokenizer.from_pretrained(OUTPUT_DIR)
model = GPT2LMHeadModel.from_pretrained(OUTPUT_DIR)
model = model.to(device)
                                        
def generate(input_str, length=250, n=5):
  '''
  This is the main generation code using our model
  '''
  cur_ids = torch.tensor(tokenizer.encode(input_str)).unsqueeze(0).long().to(device)
  model.eval()
  with torch.no_grad():
    for i in range(length):
      outputs = model(cur_ids[:, -1024:], labels=cur_ids[:, -1024:])
      loss, logits = outputs[:2]
      softmax_logits = torch.softmax(logits[0,-1], dim=0)
      next_token_id = choose_from_top(softmax_logits.to('cpu').numpy(), n=n)
      cur_ids = torch.cat([cur_ids, torch.ones((1,1)).long().to(device) * next_token_id], dim=1)
    output_list = list(cur_ids.squeeze().to('cpu').numpy())
    output_text = tokenizer.decode(output_list)
    return output_text

def choose_from_top(probs, n=5):
    '''
    This chooses the top n choices and probabilistically select one choice
    '''
    ind = np.argpartition(probs, -n)[-n:]
    top_prob = probs[ind]
    top_prob = top_prob / np.sum(top_prob) # Normalize
    choice = np.random.choice(n, 1, p = top_prob)
    token_id = ind[choice][0]
    return int(token_id)
```
For more information, please take a look at a blog I wrote on patent claim generation: ![blog](https://jason-liang.hashnode.dev/generating-fake-patents-just-the-patent-claim-part)