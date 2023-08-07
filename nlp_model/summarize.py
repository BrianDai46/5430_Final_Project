from transformers import AutoModelWithLMHead, AutoTokenizer

class Summarizer():
    def __init__(self) -> None:
        self.tokenizer = AutoTokenizer.from_pretrained("mrm8488/t5-base-finetuned-summarize-news")
        self.model = AutoModelWithLMHead.from_pretrained("mrm8488/t5-base-finetuned-summarize-news")

    def summarize(self, text, max_length=150):
        input_ids = self.tokenizer.encode(text, return_tensors="pt", add_special_tokens=True)
        generated_ids = self.model.generate(input_ids=input_ids, num_beams=2, max_length=max_length,  repetition_penalty=2.5, length_penalty=1.0, early_stopping=True)
        preds = [self.tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=True) for g in generated_ids]
        # Capitalize the first letter in each sentence.
        sentences = preds[0].split('. ')
        capitalized_sentences = [s[0].upper() + s[1:] if s else "" for s in sentences]
        capitalized_text = '. '.join(capitalized_sentences)
        if capitalized_text and not capitalized_text.endswith('.'):
            capitalized_text += '.'
        return capitalized_text
