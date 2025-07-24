from transformers import PegasusForConditionalGeneration, PegasusTokenizer

model_name = "tuner007/pegasus_paraphrase"
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name)

def paraphrase(text):
    batch = tokenizer.prepare_seq2seq_batch([text], truncation=True, padding='longest', return_tensors="pt")
    translated = model.generate(**batch, max_length=60, num_beams=10, num_return_sequences=1)
    paraphrased = tokenizer.decode(translated[0], skip_special_tokens=True)
    return paraphrased
# style.py