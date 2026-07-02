import json
import re
import os

def load_lexicon(dataset_path='algerian_curse_words.json'):
    if not os.path.exists(dataset_path):
        print(f"Error: {dataset_path} not found.")
        return set()
    
    with open(dataset_path, 'r', encoding='utf-8') as f:
        lexicon = json.load(f)
    
    # Flatten all variations into a fast-lookup set
    nsfw_set = set()
    for item in lexicon:
        for var in item['variations']:
            nsfw_set.add(var.strip().lower())
            
    return nsfw_set

def clean_text(text):
    # Normalize: Convert to lowercase and strip typical punctuation/symbols
    text = re.sub(r'[^\w\s\?]', ' ', text)
    return text.lower().split()

def main():
    # Make sure we read from the same folder as the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(script_dir, 'algerian_curse_words.json')
    
    print(f"Loading Algerian NSFW lexicon from '{dataset_path}'...")
    nsfw_set = load_lexicon(dataset_path)
    print(f"Loaded {len(nsfw_set)} unique variations.")
    print("-" * 50)
    print("Type any word or sentence to test. Type 'exit' or press Ctrl+C to quit.")
    print("-" * 50)
    
    while True:
        try:
            user_input = input("\nEnter text: ").strip()
            if not user_input:
                continue
            if user_input.lower() == 'exit':
                print("Exiting...")
                break
                
            # Clean and split the text into words
            words = clean_text(user_input)
            matched_words = [w for w in words if w in nsfw_set]
            
            if matched_words:
                print(f"❌ DETECTED: Found NSFW/offensive words: {list(set(matched_words))}")
            else:
                print("✅ Clean: No NSFW words detected.")
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
