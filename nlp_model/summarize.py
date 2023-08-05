from transformers import AutoModelWithLMHead, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("mrm8488/t5-base-finetuned-summarize-news")
model = AutoModelWithLMHead.from_pretrained("mrm8488/t5-base-finetuned-summarize-news")

def summarize(text, max_length=150):
    input_ids = tokenizer.encode(text, return_tensors="pt", add_special_tokens=True)
    generated_ids = model.generate(input_ids=input_ids, num_beams=2, max_length=max_length,  repetition_penalty=2.5, length_penalty=1.0, early_stopping=True)
    preds = [tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=True) for g in generated_ids]
    # Capitalize the first letter in each sentence.
    sentences = preds[0].split('. ')
    capitalized_sentences = [s[0].upper() + s[1:] for s in sentences]
    capitalized_text = '. '.join(capitalized_sentences)
    if capitalized_text and not capitalized_text.endswith('.'):
        capitalized_text += '.'
    return capitalized_text
    

if __name__ == '__main__':
    text = "Lawyers for former President Donald Trump asked a federal judge on Saturday afternoon for an extension in responding to the Justice Department's motion for a protective order. The order would limit what discovery evidence Trump could share publicly about the ongoing criminal case related to the 2020 presidential election. Federal prosecutors filed the motion on Friday night — just hours after Trump suggested on Truth Social that he would take revenge on anyone who goes after him."
    summarized_output = summarize(text, 80)

    print(summarized_output)