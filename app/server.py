# uvicorn app.server:app --reload
from fastapi import FastAPI
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# API init
app = FastAPI()

# Load your pre-trained GPT-2 model and tokenizer
model_path = "./trained_gpt2_model"
tokenizer = GPT2Tokenizer.from_pretrained(model_path)
model = GPT2LMHeadModel.from_pretrained(model_path)

# API call
@app.post("/generate_text")
async def generate_text(request: dict):
    prompt = request.get("prompt")
    if prompt == None:
        return {"generated_text": "Prompt field is missing"}
    # Tokenize the prompt and generate text
    input_ids = tokenizer.encode(prompt, return_tensors='pt')
    output = model.generate(input_ids,
                            pad_token_id=tokenizer.eos_token_id,
                            max_length=150, min_length = 100,
                            temperature=0.6,
                            no_repeat_ngram_size=3, 
                            do_sample=True)
    generated_text = tokenizer.batch_decode(output[:, input_ids.shape[1]:])[0]
    return {"generated_text": generated_text}
