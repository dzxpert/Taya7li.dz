# Taya7li.dz — Algerian Derja NSFW & Offensive Speech Lexicon

A curated, bilingual dataset of offensive words, insults, and profanities in the Algerian Arabic dialect (Derja). This dataset is extracted and structured specifically to run inside lightweight semantic filtering engines to detect toxic, offensive, or NSFW texts in Algerian contexts.

## Overview

Social media moderation and toxicity detection in North African dialects face unique challenges due to:
1. **Dialectal Variation**: Derja differs significantly from Modern Standard Arabic (MSA).
2. **Multilingual Scripting (Bilingualism)**: Algerian users text using both the Arabic alphabet and Latin/French scripts (commonly referred to as **Arabizi** or Chat-Arabic, incorporating numbers like `7` for `ح`, `3` for `ع`, `9` for `ق`, etc.).

This project addresses these challenges by providing a structured dictionary mapping root offensive concepts to their various morphological and script spelling variations.

## Source Dataset

The lexicon is extracted and curated from the **AlgD Toxicity Speech Dataset** hosted on Zenodo:
* **Zenodo Record**: [10937445](https://zenodo.org/records/10937445)
* **Dataset Shape**: 14,150 comments annotated for Hate Speech, Cyberbullying, and Offensive Language.

## Extraction Methodology

To construct a highly accurate and clean lexicon, the following pipeline was used:
1. **Topic-Based Filtering**: Analyzed toxicity rates across topics, highlighting categories with high concentrations of offensive speech (such as Misogyny and parliamentary politics).
2. **Statistical Token Ratio Filtering**: Surfaced candidate words by calculating the probability ratio of tokens appearing in toxic vs. clean comments:
   $$\text{Ratio}(w) = \frac{P(w \mid \text{Toxic})}{P(w \mid \text{Clean})}$$
3. **Bilingual Mapping**: For every verified slang term, we mapped its standard Arabic spelling alongside its common Latin script/Arabizi phonetic spellings used in Algerian texting.
4. **False Positive Removal**: Manually removed common conversational terms, prepositions, or topic terms that statistically matched the toxic distribution but carry no inherent offensive meaning.

## Dataset Structure

The compiled dictionary is saved in `algerian_curse_words.json`.

### Schema Details

Each entry in the JSON array follows this structure:

```json
{
  "root": "Standard Arabic script representation of the term root",
  "variations": [
    "List of all variations including Arabic affixes, plurals, and Latin/Arabizi spellings"
  ],
  "arabizi": "Primary Latin/Arabizi transliteration reference",
  "severity": "Severity classification (High, Medium, or Low)",
  "category": "Insult type (e.g., Vulgar/NSFW, Scatological, Animal Insult, Political/Sycophancy, Sectarian, Lying, Silencing)",
  "english_meaning": "English translation or semantic equivalent"
}
```

### Severity Levels
* **High**: Severe profanities, explicit vulgarity, and direct offensive cursing.
* **Medium**: Scatological terms, animal-based insults, political bootlicking slurs, sectarian slurs, and harsh silencing commands.
* **Low**: Mild expressions of disgust, spitting sounds, and trivial character insults.

---

## How to Integrate with Your Semantic Engine

Below is a Python example showing how to load the JSON dataset and build a high-performance, lightweight matching engine that handles bilingual inputs:

```python
import json
import re

class AlgerianNSFWDetector:
    def __init__(self, dataset_path='algerian_curse_words.json'):
        # Load the structured dictionary
        with open(dataset_path, 'r', encoding='utf-8') as f:
            self.lexicon = json.load(f)
            
        # Flatten all variations into a fast-lookup set
        self.nsfw_set = set()
        for item in self.lexicon:
            # You can filter by severity if needed (e.g., item['severity'] in ['High', 'Medium'])
            for var in item['variations']:
                self.nsfw_set.add(var.lower())

    def clean_text(self, text):
        # Normalize text: strip punctuation and convert to lowercase
        # Works for both Arabic and Latin characters
        text = re.sub(r'[^\w\s]', ' ', text)
        return text.lower().split()

    def detect(self, text):
        # Clean and split the text into tokens
        words = self.clean_text(text)
        matched_words = [w for w in words if w in self.nsfw_set]
        
        return {
            "is_nsfw": len(matched_words) > 0,
            "match_count": len(matched_words),
            "matches": matched_words
        }

# Usage Example:
# detector = AlgerianNSFWDetector()
# result = detector.detect("some input text here")
# print(result)
```

## Contributing & Curation

The source data resides in `algerian_curse_words.json`. If you wish to propose updates or add new variations, please submit a pull request modifying the JSON structure directly.
