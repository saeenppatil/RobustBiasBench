import pandas as pd
import re

# Load your file
df = pd.read_csv('BiasSentences_Cleaned.csv')  # Update if needed

# Combine all original patterns into your final 8 categories
bias_mapping = {
    "disability bias": [
        r"disability discrimination", r"health care disparities", r"lack of accommodations",
        r"failure to provide reasonable accommodation", r"mental health stigma",
        r"unequal healthcare access", r"disability access barriers", r"historical trauma"
    ],
    "religion bias": [
        r"religious discrimination", r"faith-based", r"religious institutions?", r"religion"
    ],
    "racial/cultural bias": [
        r"racial discrimination", r"ethnic discrimination", r"language discrimination",
        r"implicit bias", r"explicit bias", r"unconscious bias", r"racial profiling",
        r"racial covenants", r"language access barriers", r"language access voting",
        r"systemic exclusion", r"institutional racism", r"historically marginalized",
        r"historical exclusion", r"historical disenfranchisement", r"historically underserved",
        r"perpetuation of inequality", r"environmental racism", r"environmental inequity",
        r"racialized enforcement", r"lack of diversity", r"minority communities",
        r"communities of color", r"gerrymandering", r"voter suppression"
    ],
    "gender bias": [
        r"gender discrimination", r"glass ceiling", r"institutional sexism",
        r"gender pay gap", r"traditionally (male|female) jobs?"
    ],
    "economic bias": [
        r"equal access", r"equitable access", r"barriers to access", r"systemic barriers",
        r"structural barriers", r"disproportionate impact", r"disparate impact",
        r"restricted eligibility", r"underrepresented groups", r"occupational segregation",
        r"pay gap", r"wage disparity", r"economic disenfranchisement", r"resource inequities",
        r"food deserts", r"banking deserts", r"affordable housing shortage",
        r"housing discrimination", r"displacement of communities", r"gentrification impact",
        r"job access", r"poverty", r"income inequality"
    ],
    "criminal justice bias": [
        r"stop and frisk", r"over-policing", r"overcriminalization", r"bias in policing",
        r"mandatory minimums impact", r"disproportionate incarceration", r"cash bail disparities",
        r"unjustified stops", r"unequal sentencing", r"discriminatory arrest practices"
    ],
    "education bias": [
        r"school segregation", r"discriminatory admissions", r"inequitable funding",
        r"barriers to enrollment", r"special education disparities", r"digital divide",
        r"limited English proficiency", r"education funding", r"language access",
        r"achievement gap", r"equity gap"
    ],
    "preferential treatment": [
        r"preferential treatment", r"separate but equal", r"favored status",
        r"set aside", r"exclusive benefit"
    ]
}

# Matching function
def match_bias_category(text):
    if not isinstance(text, str):
        return 'no bias'
    for category, patterns in bias_mapping.items():
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return category
    return 'no bias'

# Apply to dataset
df['Final Bias Category'] = df['Original Policy'].apply(match_bias_category)

# Save output
df.to_csv('BillsBiasSentences_Final.csv', index=False)
