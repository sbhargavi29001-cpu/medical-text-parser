import spacy

nlp = spacy.load("en_core_web_sm")

text = "Patient diagnosed with diabetes and prescribed Metformin."

doc = nlp(text)

for ent in doc.ents:
    print(ent.text, ent.label_)