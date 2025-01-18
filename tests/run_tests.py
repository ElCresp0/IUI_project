from sklearn.metrics import accuracy_score, f1_score
from utilities import *
from load_dataset import load_polish_dataset, load_english_dataset
from evaluate_model import evaluate_few_shot, evaluate_zero_shot
import time


if __name__ == "__main__":
    sentences_train, categories_train, sentences_val, categories_val = load_polish_dataset()
    # sentences_train, categories_train, sentences_val, categories_val = load_english_dataset()

    start_time = time.time()
    
    result, accuracy, f1 = evaluate_zero_shot(sentences_val, categories_val, framework="bielik_api", language="pl", batch_size=10)
    # result, accuracy, f1 = evaluate_few_shot(sentences_train, categories_train, sentences_val, categories_val)

    end_time = time.time()
    execution_time = end_time - start_time
    
    print(f"Accuracy: {accuracy:.4f}")
    print(f"F1 Score: {f1:.4f}")
    print(f"\nTime taken for execution: {execution_time:.4f} seconds")
    print("\nExample results:")
    print(result[:10])  # First 10 results
