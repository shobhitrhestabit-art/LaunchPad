### Quantization
Even though our model is smart it is not practical .

i cannot learn the model on laptop or server cheaply .

Problems:

FP16 base model → large

PyTorch runtime → heavy

GPU dependency → expensive

Cloud inference → costly

So even though the model is smart, it’s not practical.




How to make the trained model , fast ,cheap and runnable anywhere .


### What does day3 do ?

we froze the model weights and added the adapters ,but the model is still huge because the base model is in fp16.

FP16 means:

16 bits per parameter

Billions of parameters → GBs of memory


so the preoblem is how can we run the model fast,cheap.



Compress the model 
using the 8bit and 4 bit quantization --- > small size and memory 

Day-3 fixes the FP16 problem by:

Quantisation

Convert FP16  - >INT8 ->  INT4

Reduce memory drastically


🔹 GGUF format

Replace PyTorch runtime

Use llama.cpp (C++ inference)

## GGUF 
PyTorch model (FP16)
   ↓
Quantization (INT8 / INT4)
   ↓
GGUF file creation
   ↓
Run with llama.cpp


models are enviornment dependent they are dependen to their framework to run the model . to make the model run anywhere we convert it into gguf format .

what is GGUF ?
GGUF is a binary file format designed specifically to run large language models efficiently for inference, mainly using llama.cpp.

inference means getting the output ,

GGUF contains weights in formats like:

q8_0

q4_0

q4_k_m

q8_0: 8-bit uniform quantization with minimal accuracy loss.

q4_0: Basic 4-bit uniform quantization for maximum compression.

q4_k_m: Advanced 4-bit K-quantization that preserves accuracy better using multiple scales.

llama.cpp is a C/C++ inference engine designed to run large language models locally, fast, and without PyTorch or Python

llama.cpp does not understand:

.bin

.pt

.safetensors

Because those are:

PyTorch-specific

Training-oriented

llama.cpp understands only:

GGUF

So the relationship is:

GGUF  →  INPUT FORMAT
llama.cpp → EXECUTION ENGINE



🔹 Deliverables
/quantized/model-int8
/quantized/model-int4
/quantized/model.gguf
QUANTISATION-REPORT.m