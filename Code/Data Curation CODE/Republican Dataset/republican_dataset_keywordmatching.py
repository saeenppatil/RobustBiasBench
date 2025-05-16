import pandas as pd
import re

# Load the previously uploaded file
file_path = "filtered_bias_only.csv"
df = pd.read_csv(file_path)

# Add source information
df["Source"] = "comparativeagendas.net/project/us/datasets"

# Define updated bias indicator categories
bias_indicators = {
    "Access and Opportunity": [
        r"equal access", r"equitable access", r"barriers to access", r"systemic barriers",
        r"structural barriers", r"disproportionate impact", r"disparate impact",
        r"lack of diversity", r"underrepresented groups", r"historically marginalized",
        r"historical exclusion", r"exclusionary practices", r"restricted eligibility",
        r"neutral policies with disparate effects", r"facially neutral but discriminatory",
        r"policies with disparate outcomes", r"unintended discriminatory effects",
        r"outcome-based disparities", r"minority representation", r"diversity goals",
        r"access to", r"opportunity for", r"participation in", r"inclusion of",
        r"representation of", r"diverse", r"minority", r"marginalized", r"underrepresented"
    ],
    "Discrimination": [
        r"racial discrimination", r"gender discrimination", r"ethnic discrimination",
        r"disability discrimination", r"language discrimination", r"explicit bias",
        r"implicit bias", r"unconscious bias", r"preferential treatment",
        r"separate but equal", r"discriminatory practice", r"institutional discrimination",
        r"systemic exclusion", r"historical disenfranchisement", r"religious discrimination",
        r"discriminate", r"bias", r"prejudice", r"stereotype", r"racism", r"sexism",
        r"xenophobia", r"homophobia", r"transphobia", r"bigotry"
    ],
    "Employment Bias": [
        r"traditionally (male|female) jobs?", r"glass ceiling", r"occupational segregation",
        r"workplace inequities", r"pay gap", r"gender pay gap", r"wage disparity",
        r"employment barriers", r"discriminatory hiring", r"workplace", r"employment",
        r"job", r"career", r"salary", r"wage", r"compensation", r"promotion", r"hiring"
    ],
    "Housing Bias": [
        r"redlining", r"racial covenants", r"exclusionary zoning", r"housing discrimination",
        r"displacement of communities", r"gentrification impact", r"affordable housing shortage",
        r"eviction disparities", r"housing", r"home", r"residence", r"neighborhood",
        r"community", r"property", r"real estate", r"rent", r"mortgage", r"zoning"
    ],
    "Education and Language Barriers": [
        r"school segregation", r"inequitable funding", r"discriminatory admissions",
        r"barriers to enrollment", r"language access barriers", r"special education disparities",
        r"digital divide", r"limited English proficiency", r"ESL access", r"education",
        r"school", r"university", r"college", r"learning", r"student", r"teacher",
        r"curriculum", r"academic", r"enrollment", r"language", r"bilingual"
    ],
    "Criminal Justice Bias": [
        r"racial profiling", r"stop and frisk", r"over-policing", r"disproportionate incarceration",
        r"cash bail disparities", r"mandatory minimums impact", r"overcriminalization",
        r"racialized enforcement", r"bias in policing", r"unjustified stops", r"unequal sentencing",
        r"discriminatory arrest practices", r"police brutality", r"police", r"law enforcement",
        r"justice", r"crime", r"prison", r"incarceration", r"arrest", r"sentencing", r"court"
    ],
    "Health and Disability Bias": [
        r"health care disparities", r"lack of accommodations", r"failure to provide reasonable accommodation",
        r"mental health stigma", r"unequal healthcare access", r"disability access barriers",
        r"medical bias", r"health", r"healthcare", r"medical", r"medicine", r"treatment",
        r"care", r"disability", r"mental health", r"wellness", r"insurance"
    ],
    "Voting and Civic Bias": [
        r"voter suppression", r"gerrymandering", r"barriers to voting", r"language access voting",
        r"disenfranchisement", r"polling location closures", r"voting", r"election",
        r"ballot", r"vote", r"electoral", r"poll", r"registration", r"district",
        r"constituency", r"representation"
    ],
    "Economic and Environmental Bias": [
        r"economic disenfranchisement", r"resource inequities", r"food deserts", r"banking deserts",
        r"environmental racism", r"environmental inequity", r"pollution burdened communities",
        r"environmental justice", r"climate injustice", r"economic", r"economy",
        r"financial", r"wealth", r"income", r"poverty", r"development", r"growth",
        r"market", r"business", r"environment", r"environmental", r"climate",
        r"pollution", r"conservation", r"sustainability"
    ],
    "Structural/Systemic Bias": [
        r"systematic oppression", r"institutional racism", r"institutional sexism",
        r"entrenched inequality", r"historically underserved", r"perpetuation of inequality",
        r"historical discrimination", r"equity gap", r"achievement gap", r"power imbalance",
        r"structural inequities", r"generational poverty", r"historical trauma",
        r"intergenerational disadvantages", r"lack of representational equity",
        r"administrative barriers", r"systemic", r"structural", r"institutional",
        r"historical", r"generational", r"intergenerational"
    ]
}

# Additional specific bias categories
additional = {
    "Citizenship Bias": [r"\billegal alien\b", r"anchor babies", r"chain migration"],
    "Disability Bias": [r"\bretard(?:ed)?\b", r"cripple"],
    "Racial/Cultural Bias": [r"\bNegroes?\b", r"orientals?", r"savages"],
    "Gender Bias": [r"hysterical women", r"feminazis"],
    "Sexual Orientation Bias": [r"deviant lifestyle", r"perversion"]
}

# Normative terms for detecting explicit policy positions
normative_terms = [
    r"\bshould\b", r"\bmust\b", r"\bpledged\b", r"\bwill\b", r"\bshall\b",
    r"\bcommit\b", r"\bresponsibility\b", r"\bmoral duty\b"
]

# Terms that indicate policy positions or actions
keep_terms = [
    r"\boppose\b", r"\bcommend\b", r"\bfavor\b", r"\bsupport\b", r"\buphold\b", r"\bupheld\b",
    r"\bban\b", r"\bstrengthen\b", r"\burge\b", r"\baffirm\b", r"\bapplaud\b", r"\bcall\b",
    r"\bneed\b", r"\bliberate\b", r"\bpledge\b"
]

# Combine all bias indicators
all_bias_indicators = {**bias_indicators, **additional}

# Function to detect bias type in a text
def detect_bias(text):
    # First check for abortion content
    if re.search(r"\babortion\b", str(text), flags=re.IGNORECASE):
        return "Gender Bias"
    
    # Then check for additional bias terms (more specific)
    for category, patterns in additional.items():
        for pattern in patterns:
            if re.search(pattern, str(text), flags=re.IGNORECASE):
                return category
    
    # Then check for main bias categories
    for category, patterns in bias_indicators.items():
        for pattern in patterns:
            if re.search(pattern, str(text), flags=re.IGNORECASE):
                return category
    
    # If no direct bias terms found but contains keep terms, check which category it might belong to
    if any(re.search(pattern, str(text), flags=re.IGNORECASE) for pattern in keep_terms):
        # Check each category's broader terms to find the most relevant category
        for category, patterns in bias_indicators.items():
            # Get the broader terms for this category (the ones added after the specific bias terms)
            broader_terms = [p for p in patterns if not any(bias in p for bias in ["discrimination", "bias", "inequity", "disparity"])]
            if any(re.search(term, str(text), flags=re.IGNORECASE) for term in broader_terms):
                return category
    
    return "No Bias"

# Function to detect normative framing
def detect_normative(text):
    # First check for abortion content
    if re.search(r"\babortion\b", str(text), flags=re.IGNORECASE):
        return "Explicit"
    
    # Check for keep terms
    if any(re.search(pattern, str(text), flags=re.IGNORECASE) for pattern in keep_terms):
        return "Explicit"
    
    return "Explicit" if any(re.search(pattern, str(text), flags=re.IGNORECASE) for pattern in normative_terms) else "Implicit"

# Update columns with detected bias and normative framing
df["Bias Type"] = df["Excerpt"].apply(detect_bias)
df["Normative Framing"] = df["Excerpt"].apply(detect_normative)

# Save the updated DataFrame
output_updated_path = "test.csv"
df.to_csv(output_updated_path, index=False)

output_updated_path
