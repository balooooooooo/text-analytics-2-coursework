from fastapi import FastAPI
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# API initialization
app = FastAPI()

# Loading pre-trained model
model_path = "./app/trained_gpt2_model_large"
tokenizer = GPT2Tokenizer.from_pretrained(model_path, local_files_only=True)
model = GPT2LMHeadModel.from_pretrained(model_path, local_files_only=True)

# API call
# Accpets only a dictionary, which should always contain prompt, max_len and temp
@app.post("/generate_review")
async def generate_text(request: dict):
    # Get prompt. If there is no prompt, exit early
    # Possible checks that prompt/max_len/temp exists, but not implemented since only we will use it
    prompt = request.get("prompt")
    # Tokenization and generation
    input_ids = tokenizer.encode(prompt, return_tensors='pt') # Encode prompt
    output = model.generate(input_ids,
                            pad_token_id=tokenizer.eos_token_id, # end-of-sequence tokens
                            min_length = 50, max_length=request.get("max_len"), # min/max length
                            temperature=request.get("temp"), # temperature
                            no_repeat_ngram_size=3, # control repeated n-grams
                            do_sample=True # use samples (necessary for temperature)
                            )
    # Decode and return
    generated_text = tokenizer.batch_decode(output[:, input_ids.shape[1]:])[0] # Decode generated text
    return {"generated_text": generated_text}