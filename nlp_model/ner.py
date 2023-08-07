import spacy

class NER():
    def __init__(self) -> None:
        self.nlp = spacy.load("model_train\model")

    def ner(self, text):
        doc = self.nlp(text)
        return [(ent.text, ent.label_)for ent in doc.ents]