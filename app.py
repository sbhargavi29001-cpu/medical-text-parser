import spacy
import re

# Load spaCy model
nlp = spacy.load("en_core_web_sm")


def extract_info(text):
    text_lower = text.lower()

    diagnosis = []
    symptoms = []
    medications = []
    dosage = []
    follow_up = []

    # -----------------------------
    # ✅ Diagnosis
    # -----------------------------
    if "diagnosed with" in text_lower:
        part = text_lower.split("diagnosed with")[-1]
        diagnosis.append(part.split(".")[0].strip())

    # -----------------------------
    # ✅ Symptoms (multiple patterns)
    # -----------------------------
    symptom_patterns = ["complains of", "reports", "presents with"]

    for pattern in symptom_patterns:
        if pattern in text_lower:
            part = text_lower.split(pattern)[-1]
            symptoms.append(part.split(".")[0].strip())
            break

    # -----------------------------
    # ✅ Medication + Dosage (Regex)
    # -----------------------------
    med_pattern = r"(prescribed\s+)([A-Za-z]+)\s*(\d+mg|\d+\s*mg)?"

    matches = re.findall(med_pattern, text, re.IGNORECASE)

    for match in matches:
        drug = match[1]
        dose = match[2]

        if drug:
            medications.append(drug)

        if dose:
            dosage.append(dose)

    # -----------------------------
    # ✅ Follow-up
    # -----------------------------
    if "follow up" in text_lower or "follow-up" in text_lower:
        follow_up.append("Follow-up required")

    # -----------------------------
    # ✅ spaCy Enhancement
    # -----------------------------
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ in ["PRODUCT"]:
            medications.append(ent.text)

    # -----------------------------
    # ✅ Remove duplicates
    # -----------------------------
    medications = list(set(medications))
    dosage = list(set(dosage))

    # -----------------------------
    # ✅ Final Output
    # -----------------------------
    result = {
        "Diagnosis": diagnosis if diagnosis else ["Not found"],
        "Symptoms": symptoms if symptoms else ["Not found"],
        "Medications": medications if medications else ["Not found"],
        "Dosage": dosage if dosage else ["Not found"],
        "Follow-up": follow_up if follow_up else ["Not found"]
    }

    return result


# -----------------------------
# ✅ Sample Run
# -----------------------------
if __name__ == "__main__":
    text = """Patient diagnosed with hypertension.
    Complains of headache and dizziness.
    Prescribed Amlodipine 5mg daily.
    Advised to follow up after 1 week."""

    result = extract_info(text)

    print("\n--- Structured Medical Summary ---\n")
    for key, value in result.items():
        print(f"{key}: {', '.join(value)}")