import spacy

nlp = spacy.load("./model_train/model")

if __name__ == '__main__':
    text = "Lawyers for former President Donald Trump asked a federal judge on Saturday afternoon for an extension in responding to the Justice Department's motion for a protective order. The order would limit what discovery evidence Trump could share publicly about the ongoing criminal case related to the 2020 presidential election. Federal prosecutors filed the motion on Friday night — just hours after Trump suggested on Truth Social that he would take revenge on anyone who goes after him."
    doc = nlp(text)
    # for ent in doc.ents:
    #     print(ent.text, ent.start_char, ent.end_char, ent.label_)

    # simplify output, you may change the code below to customize the output
    for ent in doc.ents:
        print(ent.text, ent.label_)