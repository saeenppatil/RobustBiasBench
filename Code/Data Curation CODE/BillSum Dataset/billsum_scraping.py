import tensorflow_datasets as tfds
import json
import os

# Define the output path for the JSON file
output_path = os.path.expanduser("~/Desktop/Webscrape/all_bills.json")

# Load the 'train' split of the BillSum dataset
dataset = tfds.load('billsum', split='train')

# Extract 'title' and 'text' fields from each example
bills = []
for example in tfds.as_numpy(dataset):
    title = example['title'].decode('utf-8')
    text = example['text'].decode('utf-8')
    bills.append({'title': title, 'text': text})

# Save the extracted data to a JSON file
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(bills, f, ensure_ascii=False, indent=2)

print(f"Saved {len(bills)} entries to {output_path}")