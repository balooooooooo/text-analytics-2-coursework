# uvicorn app.server:app --reload
from fastapi import FastAPI
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# API init
app = FastAPI()

# Load your pre-trained GPT-2 model and tokenizer
model_path = "./app/trained_gpt2_model"
tokenizer = GPT2Tokenizer.from_pretrained(model_path, local_files_only=True)
model = GPT2LMHeadModel.from_pretrained(model_path, local_files_only=True)

# API call
@app.post("/generate_review")
async def generate_text(request: dict):
    prompt = request.get("prompt")
    if prompt == None:
        return {"generated_text": "Prompt field is missing"}
    # Tokenize the prompt and generate text
    input_ids = tokenizer.encode(prompt, return_tensors='pt')
    output = model.generate(input_ids,
                            pad_token_id=tokenizer.eos_token_id,
                            min_length = 50, max_length=request.get("max_len"),
                            temperature=request.get("temp"),
                            no_repeat_ngram_size=3, 
                            do_sample=True)
    generated_text = tokenizer.batch_decode(output[:, input_ids.shape[1]:])[0]
    return {"generated_text": generated_text}

# API call
@app.get("/")
async def read_root():
    import os
    return {
        "message": "This is the homepage, duh."
        }