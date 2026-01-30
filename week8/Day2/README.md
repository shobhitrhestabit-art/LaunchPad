### Day2 

we want to teach an alreday trained language model some new behaviour without retraining the entire model .


we dont want to teach everything to the model so to make the model know our domain and database and our task style we fine tune it so model.

so instead of teaching everything again we want to keep existing knowledge and add small target learning 


we adjust model weights so outputs much better our dataset.


### Day2 Flow

we load the model using hugging face ,
we load the model and freeze the weights of the base model using bitandbytes 

we then create adapters basically matrix A& B  in the adapters (small weights )

when the input is ingested ,the model leanrs the through computation of the base models and the adapters output ,

then it backpropogates the model ,and updates the adapters weights ,not the base model weights .







### Parameter-Efficient Fine Tuning (PEFT)

instead of training 100% weights 

we train -1%
we frooze everything else


we freeze the weights and create trainable which are trainable 




### New Readme

we load the model in the quantized weights 

## 1. bitsandbytes (The Memory Shrinker)
This is the core engine for Quantization.

What it does: It compresses model weights from 16-bit or 32-bit down to 4-bit or 8-bit.

Why you need it: Without this, a 1.1B model might struggle on a basic GPU. With it, the model fits easily into VRAM, leaving room for the actual training data


## 2. transformers (The Architecture)
This is the main library for interacting with pre-trained models.

What it does: It provides the AutoModelForCausalLM and AutoTokenizer classes used to download and load TinyLlama from the Hugging Face Hub.

Why you need it: It acts as the bridge between the raw model files and your Pytho





###Tokenizer 

BPE (Byte Pair Encoding), SentencePiece, or WordPiece tokenizer.