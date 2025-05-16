# In[0] - Imports and Constants
import pandas as pd
import re
import os
import numpy as np

# --- Constants ---
INPUT_CSV_FILENAME = './US-Legislative-congressional_bills_19.3_3_3.csv'
# New output filename reflecting original keywords and new format
OUTPUT_CSV_FILENAME = 'congressional_bills_analyzed_original_keywords_new_format.csv'
# Citation remains the same, adjust if needed
CITATION_STRING = "Policy Agendas Project. 2023. Congressional Bills Project Dataset."

# --- Original Bias Keywords (from Notebook) ---
# Reinstating the original dictionary with additions
bias_categories = {
    'Racial/Cultural': [' certain race', 'increase racial restrictions', 'certain ethnicity', 'colored', 'slave', 'master',
                        'off the reservation', 'certain Indians', 'sale of Native lands', 'prohibit people of color',
                        ' only certain cultures', 'certain culture', 'certain heritage', 'certain cultures',
                        'racial segregation', 'ethnic group', 'tribal lands', 'minority group', 'racial quota',
                        'affirmative action', 'national origin', 'civil rights', 'desegregation', 'hate crime',
                        'indigenous rights'],

    'Economic': ['exclude poor', 'socioeconomic', 'wealth', 'decrease pensions', 'decrease in pensions',
                 'exclude pensions', 'low-income', 'poverty level', 'means-tested', 'income inequality',
                 'wealth gap', 'economic disparity', 'redlining', 'predatory lending', 'wage gap',
                 'economic justice', 'gentrification', 'usury'],

    'Gender': ['depending on gender', 'feminine', 'masculine', 'only males', 'sex discrimination',
               'gender identity', 'sexual orientation', 'equal pay', "women's rights", "men's rights",
               'gender quota', 'gender preference', 'reproductive rights', 'domestic violence',
               'sexual harassment', 'LGBTQ+', 'gender parity'],

    'Disability': ['retard', 'retarded', 'diability', 'handicap', 'mental health stigma',
                   'persons with disabilities', 'accessibility', 'reasonable accommodation', 'ableism',
                   'special needs', 'impaired', 'institutionalization', 'disability rights', 'inclusion',
                   'neurodiversity', 'independent living'],

    'Religion': ['certain religions', 'only christians', 'no muslims', 'certain faiths', 'must be christian', 'no muslim',
                 'no muslims', 'religious freedom', 'religious exemption', 'freedom of worship', 'sectarian',
                 'non-believers', 'religious persecution', 'state religion', 'religious discrimination',
                 'separation of church and state', 'freedom of conscience'],

    'Age': ['certain age', 'certain elderly', 'no seniors', 'only youths', 'only minors', 'certain teens', 'certain children',
            'age discrimination', 'elder abuse', 'mandatory retirement', 'juvenile', 'senior citizen',
            'ageism', 'child labor', 'elder care', 'generational equity'],

    'Criminal Justice' : ['racial profiling', 'bias in policing', 'cash bail disparities', 'sentencing disparity',
                          'mandatory minimums', 'stop and frisk', 'prison reform', 'wrongful conviction', 'police brutality',
                          'mass incarceration', 'police misconduct', 'restorative justice', 'three-strikes law'],

    'Education': ['school segregation', 'Native language', 'Native English', 'English speaker',
                  'must speak English', 'educational equity', 'school funding disparity', 'achievement gap',
                  'special education', 'bilingual education', 'language barrier', 'Title IX',
                  'inclusive education', 'book ban', 'curriculum bias'],

    'Citizenship': ['illegals','aliens', 'illegal aliens', 'undocumented immigrant', 'naturalization',
                    'deportation', 'asylum seeker', 'refugee status', 'immigration status', 'non-citizen',
                    'foreign national', 'border control', 'visa restrictions', 'xenophobia',
                    'migrant workers', 'lawful permanent resident'],

    'Multiple': ['preference', 'support discrimination', 'favoring', 'bias', 'inequality', 'prohibit people of',
                 'certain people', 'only allow certain' , 'prohibit those', 'unequal treatment', 'disparate impact',
                 'systemic bias', 'exclusionary', 'preferential treatment', 'discriminatory practice',
                 'social justice', 'equity', 'equal opportunity', 'protected class', 'marginalized group']
}

# --- Compile Regex Patterns (Adapted for original bias_categories) ---
compiled_patterns_original = []
print("Compiling regex patterns from original bias_categories...")
for category, keywords in bias_categories.items():
    # Clean keywords: remove leading/trailing whitespace and filter empty strings
    cleaned_keywords = [kw.strip() for kw in keywords if kw and kw.strip()]
    if not cleaned_keywords:
        print(f"Warning: No valid keywords found for category '{category}'. Skipping.")
        continue
    try:
        # Create a single pattern for the category matching whole words/phrases (case-insensitive)
        # Use word boundaries (\b) around each keyword
        pattern_str = r'\b(?:' + '|'.join(re.escape(kw) for kw in cleaned_keywords) + r')\b'
        compiled_pattern = re.compile(pattern_str, re.IGNORECASE)
        compiled_patterns_original.append((compiled_pattern, category))
    except re.error as e:
        print(f"Warning: Error compiling regex for category '{category}'. Skipping. Error: {e}")
    except Exception as e:
        print(f"Warning: An unexpected error occurred compiling regex for category '{category}': {e}. Skipping.")

print(f"Compiled {len(compiled_patterns_original)} patterns from original categories.")


# --- Analysis Function (Adapted for original bias_categories) ---
def find_bias_categories_original(text):
    """
    Finds categories based on the original bias_categories keywords.
    Returns a sorted list of unique matching category names.
    """
    matched_categories = set()
    if not isinstance(text, str):
        return [] # Return empty list for non-string input
    for pattern, category_name in compiled_patterns_original:
        if pattern.search(text):
            matched_categories.add(category_name)
    return sorted(list(matched_categories))

# --- Date Formatting Function (Not strictly needed for output, but kept for potential use) ---
def format_date(row):
    try:
        year = str(int(row['year']))
        month = '01'
        day = '01'
        return f"{year}-{month}-{day}"
    except (ValueError, TypeError, KeyError):
        if 'year' in row and pd.notna(row['year']):
            try:
                return str(int(row['year']))
            except (ValueError, TypeError):
                return None
        return None

# In[1] - Load, Process, and Save Data

# --- Load Data ---
print(f"Attempting to load data from: {INPUT_CSV_FILENAME}")
try:
    # Skip the first 200000 data rows
    df_bills = pd.read_csv(
        INPUT_CSV_FILENAME,
        skiprows=range(1, 200001),
        header=0,
        encoding='ISO-8859-1',
        low_memory=False
    )
    print(f"Successfully loaded {len(df_bills)} rows from {INPUT_CSV_FILENAME} (starting from row 200001).")
except FileNotFoundError:
    print(f"Error: Input CSV file not found at {INPUT_CSV_FILENAME}")
    raise SystemExit(1)
except Exception as e:
    print(f"Error loading CSV file: {e}")
    raise SystemExit(1)

# --- Data Cleaning (NaNs in required columns) ---
print("Cleaning data...")
# Ensure bill_id is also checked for NaN removal as it's used for deduplication now
required_columns = ['id', 'bill_id', 'year', 'description']
if not all(col in df_bills.columns for col in required_columns):
    missing = [col for col in required_columns if col not in df_bills.columns]
    print(f"Error: Missing required columns in the input CSV: {missing}")
    raise SystemExit(1)

# Drop rows where any of the required output columns (esp. id, bill_id, description) are NaN
original_count = len(df_bills)
df_bills = df_bills.dropna(subset=required_columns)
dropped_na_count = original_count - len(df_bills)
if dropped_na_count > 0:
    print(f"Removed {dropped_na_count} rows due to missing values in required columns (id, bill_id, year, description).")

# --- Analyze Data ---
print("Analyzing descriptions for bias keywords (using original categories)...")
# Use .loc to avoid SettingWithCopyWarning
df_bills.loc[:, 'found_categories'] = df_bills['description'].apply(find_bias_categories_original)

# --- Drop Duplicates by bill_id ---
print("Removing duplicate rows based on 'bill_id'...") # Changed from 'id'
count_before_dedupe = len(df_bills)
# Changed subset from ['id'] to ['bill_id']
df_bills = df_bills.drop_duplicates(subset=['bill_id'], keep='first')
count_after_dedupe = len(df_bills)
print(f"Removed {count_before_dedupe - count_after_dedupe} duplicate rows based on 'bill_id'. Kept {count_after_dedupe} rows.")

# --- Filter Rows with No Bias Found ---
# Reinstating the filtering step
print("Filtering out rows where no bias keywords were found...")
initial_analyzed_count = len(df_bills)
# Filter based on the 'found_categories' column containing at least one item
df_bills_filtered = df_bills[df_bills['found_categories'].apply(lambda x: isinstance(x, list) and len(x) > 0)].copy()
final_analyzed_count = len(df_bills_filtered)
print(f"Filtered out {initial_analyzed_count - final_analyzed_count} rows with no keyword matches. Kept {final_analyzed_count} rows.")
# Subsequent steps will use df_bills_filtered

# --- Process Bias Column for Final Output Format ---
print("Processing 'bias' column for final output format...")
bias_column_values = []

# Process rows in df_bills_filtered now
if not df_bills_filtered.empty:
    # Iterate over the filtered DataFrame
    for categories in df_bills_filtered['found_categories']:
        # No need to check for empty list here, as filtering already removed them
        if isinstance(categories, list):
            count = len(categories)
            if count == 1:
                bias_column_values.append(categories[0]) # Use the single category name
            elif count > 1:
                bias_column_values.append("Multiple") # Use "Multiple" if more than one category found
            # else case (empty list) is handled by the filtering above
        else: # Handle unexpected data types
             bias_column_values.append(np.nan) # Keep assigning NaN for truly unexpected types
    # Add the processed 'bias' column to df_bills_filtered
    df_bills_filtered['bias'] = bias_column_values
else:
    print("DataFrame is empty after filtering for bias keywords.")
    # Ensure df_bills_filtered has the 'bias' column even if empty
    df_bills_filtered['bias'] = []

# --- Normalize Descriptions for Deduplication ---
def normalize_description(text):
    if not isinstance(text, str):
        return ""
    # Lowercase
    text = text.lower()
    # Remove common prefixes (use regex for word boundaries and start of string)
    # Examples: "a bill to ", "an act to ", "to "
    text = re.sub(r'^(a bill to |an act to |to )\s*', '', text)
    # Remove common suffixes (use regex for end of string)
    # Example: ", and for other purposes."
    text = re.sub(r'\s*, and for other purposes\.$', '', text)
    # Remove punctuation (keep spaces)
    text = re.sub(r'[^\w\s]', '', text)
    # Collapse multiple whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

print("Normalizing descriptions for more robust deduplication...")
# Apply normalization to the filtered DataFrame
df_bills_filtered['normalized_description'] = df_bills_filtered['description'].apply(normalize_description)

# --- Drop Duplicates by Normalized Description ---
print("Removing duplicate rows based on normalized 'description'...")
# Operate on the filtered DataFrame, using the normalized column
count_before_desc_dedupe = len(df_bills_filtered)
# Keep 'first' ensures we keep the one that appeared earliest
df_bills_filtered = df_bills_filtered.drop_duplicates(subset=['normalized_description'], keep='first')
count_after_desc_dedupe = len(df_bills_filtered)
print(f"Removed {count_before_desc_dedupe - count_after_desc_dedupe} duplicate rows based on normalized 'description'. Kept {count_after_desc_dedupe} rows.")

# --- Create Final DataFrame (New Structure) ---
print("Creating final DataFrame with the specified structure...")
# Create the final DataFrame from the filtered and deduplicated data
if not df_bills_filtered.empty:
    # Select required columns (excluding normalized_description and bill_id)
    df_analyzed = df_bills_filtered[['id', 'year', 'description', 'bias']].copy()
    # Add the 'Normative Framing' column
    df_analyzed['Normative Framing'] = "Manual Review Needed"
else:
    # Create an empty DataFrame with the correct columns if no results
    df_analyzed = pd.DataFrame(columns=[
        'id', 'year', 'description', 'bias', 'Normative Framing'
    ])

# --- Ensure correct column order ---
df_analyzed = df_analyzed[['id', 'year', 'description', 'bias', 'Normative Framing']]

# --- Sort by Bias Category ---
print("Sorting data by bias category...")
# Sort, placing NaN or "No Bias Keyword Found" potentially at the end depending on pandas version/exact string
df_analyzed = df_analyzed.sort_values(by='bias', na_position='last')

# --- Reset Index to Start from 1 ---
print("Resetting index to start from 1...")
df_analyzed = df_analyzed.reset_index(drop=True)
df_analyzed.index = df_analyzed.index + 1

# --- Save Results ---
print(f"Attempting to save analyzed data to: {OUTPUT_CSV_FILENAME}")
try:
    # Save as CSV with UTF-8 encoding
    df_analyzed.to_csv(OUTPUT_CSV_FILENAME, index=False, encoding='utf-8')
    print(f"Successfully saved analyzed data ({len(df_analyzed)} rows) to {OUTPUT_CSV_FILENAME}")
except Exception as e:
    print(f"Error saving CSV file: {e}")
    raise SystemExit(1)

# --- Display Sample Output (Optional) ---
print("\nSample of analyzed data:")
print(df_analyzed.head())

print("\nScript finished.")