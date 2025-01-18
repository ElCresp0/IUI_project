from datasets import load_dataset
from sklearn.model_selection import train_test_split

def load_polish_dataset(test_size=0.2, random_state=42):
    """Loads the dataset, processes it, and splits it into training and validation sets."""
    ds = load_dataset("rafalposwiata/open-coursebooks-pl")
    train_data = ds["train"]
    
    processed_data = []
    for row in train_data:
        field = row["field"]
        for sentence in row["paragraphs"]:
            processed_data.append({"sentences": sentence, "categories": field})
    
    sentences = [item["sentences"] for item in processed_data]
    categories = [item["categories"] for item in processed_data]
    
    unique_categories = list(set(categories))
    
    sentences_train, sentences_val, categories_train, categories_val = train_test_split(
        sentences, categories, test_size=test_size, random_state=random_state, stratify=categories
    )
    print(f"Training dataset size: {len(sentences_train)} sentences")
    print(f"Validation dataset size: {len(sentences_val)} sentences")
    print(f"Number of unique categories: {len(unique_categories)}, Categories: {unique_categories}")
    
    return sentences_train, categories_train, sentences_val, categories_val

def load_english_dataset(test_size=0.2, random_state=42):
    """Loads the dataset, processes it, and splits it into training and validation sets."""
    ds = load_dataset("derek-thomas/ScienceQA")
    train_data = ds["train"]
      
    sentences = []
    categories = []
    for row in train_data:
        if row["lecture"] and row["topic"]:
            sentences.append(row["lecture"])
            categories.append(row["topic"])

    unique_categories = list(set(categories))
        
    sentences_train, sentences_val, categories_train, categories_val = train_test_split(
        sentences, categories, test_size=test_size, random_state=random_state, stratify=categories
    )
    print(f"Training dataset size: {len(sentences_train)} sentences")
    print(f"Validation dataset size: {len(sentences_val)} sentences")
    print(f"Number of unique categories: {len(unique_categories)}, Categories: {unique_categories}")
    
    return sentences_train, categories_train, sentences_val, categories_val