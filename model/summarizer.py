from transformers import T5Tokenizer, T5ForConditionalGeneration

# Load T5-small model and tokenizer
tokenizer = T5Tokenizer.from_pretrained("t5-small")
model = T5ForConditionalGeneration.from_pretrained("t5-small")

def summarize_text(text: str, max_length: int = 120):
    """
    Generate a concise summary from extracted resume text.
    The input is truncated to avoid overload.
    """
    # Safety truncation to keep things fast
    text = text[:2000]  

    input_text = "summarize: " + text
    inputs = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)

    summary_ids = model.generate(
        inputs,
        max_length=max_length,
        min_length=40,
        length_penalty=2.0,
        num_beams=4,
        early_stopping=True
    )

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary.strip()
