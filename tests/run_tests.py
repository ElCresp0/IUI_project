from sklearn.metrics import accuracy_score, f1_score
from utilities import *
from load_dataset import load_polish_dataset, load_english_dataset
from evaluate_model import evaluate_few_shot, evaluate_zero_shot
import time

def results(accuracy, f1, execution_time, result, num_examples = 10):
    """Prints evaluation results."""
    print(f"Accuracy: {accuracy:.4f}")
    print(f"F1 Score: {f1:.4f}")
    print(f"\nTime taken for execution: {execution_time:.4f} seconds")
    print("\nExample results:")
    print(result[:num_examples])  # First 10 results
    print("\n")

if __name__ == "__main__":
    sentences_train, categories_train, sentences_val, categories_val = load_polish_dataset()
    sentences_train_en, categories_train_en, sentences_val_en, categories_val_en = load_english_dataset()

    # Stormtrooper - pl
    print("Stormtrooper PL zero-shot")
    start_time = time.time()    
    result, accuracy, f1 = evaluate_zero_shot(sentences_val, categories_val, framework="stormtrooper", language="pl", batch_size=100)
    end_time = time.time()
    execution_time = end_time - start_time
    results(accuracy, f1, execution_time, result)

    print("Stormtrooper PL few-shot")
    start_time = time.time()    
    result, accuracy, f1 = evaluate_few_shot(sentences_train, categories_train, sentences_val, categories_val)
    end_time = time.time()
    execution_time = end_time - start_time
    results(accuracy, f1, execution_time, result)

    # Stormtrooper - en
    print("Stormtrooper EN zero-shot")
    start_time = time.time()    
    result, accuracy, f1 = evaluate_zero_shot(sentences_val_en, categories_val_en, framework="stormtrooper", language="en", batch_size=100)
    end_time = time.time()
    execution_time = end_time - start_time
    results(accuracy, f1, execution_time, result)

    print("Stormtrooper EN few-shot")
    start_time = time.time()    
    result, accuracy, f1 = evaluate_few_shot(sentences_train_en, categories_train_en, sentences_val_en, categories_val_en,  framework="stormtrooper", language="en")
    end_time = time.time()
    execution_time = end_time - start_time
    results(accuracy, f1, execution_time, result)

    # Bielik - workers = 20
    print("Bielik PL zero-shot")
    start_time = time.time()   
    result, accuracy, f1 = evaluate_zero_shot(sentences_val, categories_val, framework="bielik_api", language="pl", batch_size=100)
    end_time = time.time()
    execution_time = end_time - start_time
    results(accuracy, f1, execution_time, result)
    
    print("Bielik PL few-shot")
    start_time = time.time()    
    result, accuracy, f1 = evaluate_few_shot(sentences_train, categories_train, sentences_val, categories_val,  framework="bielik_api", language="pl")
    end_time = time.time()
    execution_time = end_time - start_time
    results(accuracy, f1, execution_time, result)
