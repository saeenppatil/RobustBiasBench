import pandas as pd
import re

# Load your CSV
df = pd.read_csv("US-Legislative-public_laws_20.1_8.csv", encoding="ISO-8859-1")  # Replace with your actual file path

# Define the bias indicators
bias_indicators = {
    "disability bias": [
        r"blind", r"deaf", r"disability", r"disorder", r"disabled", r"impaired", r"impairment",
        r"mental health", r"handicapped", r"disabilities", r"wheelchair", r"special education"
    ],
    "economic bias": [
        r"low income", r"poverty", r"homeless", r"fee waiver", r"low-income", r"calwork"
    ],
    "gender bias": [
        r"female", r"sexual harassment", r"title ix"
    ],
    "racial/cultural bias": [
        r"segregation", r"race", r"racial", r"minority", r"ethnic", r"discrimination",
        r"desegregation", r"affirmative action", r"diversity", r"title vi"
    ],
    "religion bias": [
        r"religion", r"religious", r"worship", r"prayer"
    ],
    "education bias": [
        r"english proficiency", r"fluent", r"fluency", r"primary language", r"secondary language",
        r"elementary school", r"middle school", r"high school", r"university", r"public school",
        r"charter school", r"private school", r"educationally disadvantaged", r"504 plan"
    ],
    "criminal justice bias": [
        r"police", r"criminal record", r"crime"
    ],
    "citizenship bias": [
        r"immigrant", r"vote", r"voting"
    ]
}

import pandas as pd
import re

# Load CSV
df = pd.read_csv("US-Legislative-public_laws_20.1_8.csv", encoding="ISO-8859-1")

# Define the bias indicators
bias_mapping = {
    "disability bias": [
        r"blind", r"deaf", r"disability", r"disorder", r"disabled", r"impaired", r"impairment",
        r"mental health", r"handicapped", r"disabilities", r"wheelchair", r"special education"
    ],
    "economic bias": [
        r"low income", r"poverty", r"homeless", r"fee waiver", r"low-income", r"calwork"
    ],
    "gender bias": [
        r"female", r"sexual harassment", r"title ix"
    ],
    "racial/cultural bias": [
        r"segregation", r"race", r"racial", r"minority", r"ethnic", r"discrimination",
        r"desegregation", r"affirmative action", r"diversity", r"title vi"
    ],
    "religion bias": [
        r"religion", r"religious", r"worship", r"prayer"
    ],
    "education bias": [
        r"english proficiency", r"fluent", r"fluency", r"primary language", r"secondary language",
        r"elementary school", r"middle school", r"high school", r"university", r"public school",
        r"charter school", r"private school", r"educationally disadvantaged", r"504 plan"
    ],
    "criminal justice bias": [
        r"police", r"criminal record", r"crime"
    ],
    "citizenship bias": [
        r"immigrant", r"vote", r"voting"
    ]
}

# Function to match a single sentence
def match_bias_category(text):
    for category, patterns in bias_mapping.items():
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return category
    return None

# Prepare results
matched_rows = []

for _, row in df.iterrows():
    description = str(row.get("description", ""))
    year = row.get("year", "")

    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', description)

    for sentence in sentences:
        found = False
        for category, patterns in bias_mapping.items():
            for pattern in patterns:
                match = re.search(pattern, sentence, re.IGNORECASE)
                if match:
                    matched_rows.append({
                        "sentence": sentence.strip(),
                        "matched_word": match.group(),
                        "bias_type": category,
                        "year": year
                    })
                    found = True
                    break
            if found:
                break

# Create DataFrame and save
out_df = pd.DataFrame(matched_rows)
out_df.to_csv("MatchedBiasSentences_WithWord.csv", index=False)