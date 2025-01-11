import random
import requests
import time
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
from datasets import load_dataset

API_URL = "http://localhost:8080"
CHECK_INTERVAL = 2  # Czas w sekundach między sprawdzaniem statusu

def process_and_split_dataset(test_size=0.2, random_state=42):
    ds = load_dataset("rafalposwiata/open-coursebooks-pl")
    train_data = ds["train"]
    
    processed_data = []
    for row in train_data:
        field = row["field"]
        for sentence in row["paragraphs"]:
            processed_data.append({"sentences": sentence, "categories": field})
    
    sentences = [item["sentences"] for item in processed_data]
    categories = [item["categories"] for item in processed_data]
    
    sentences_train, sentences_val, categories_train, categories_val = train_test_split(
        sentences, categories, test_size=test_size, random_state=random_state, stratify=categories
    )
    
    return sentences_train, categories_train, sentences_val, categories_val

def send_task(api_url, sample_sentences, sample_categories, sentences_to_classify):
    payload = {
        "sample_sentences": sample_sentences,
        "categories": sample_categories,
        "sentences": sentences_to_classify,
    }
    response = requests.post(f"{api_url}/task/submit", json=payload)
    if response.status_code == 200:
        return response.json()["task_id"]
    else:
        raise Exception(f"Błąd API przy wysyłaniu zadania: {response.status_code}, {response.text}")

def check_task_status(api_url, task_id):
    response = requests.get(f"{api_url}/task/status/{task_id}")
    if response.status_code == 200:
        return response.text.strip()  # Bezpośredni status jako tekst ("SUCCESS", "PENDING")
    else:
        raise Exception(f"Błąd API przy sprawdzaniu statusu zadania {task_id}: {response.status_code}, {response.text}")

def get_task_result(api_url, task_id):
    response = requests.get(f"{api_url}/task/result/{task_id}")
    if response.status_code == 200:
        return response.json()  # Bezpośrednia lista wynikowych etykiet
    else:
        raise Exception(f"Błąd API przy odbieraniu wyniku zadania {task_id}: {response.status_code}, {response.text}")

def evaluate_model(sentences_train, categories_train, sentences_val, categories_val):
    batch_size = 10
    max_tasks = 5  # Liczba zadań, które mogą być jednocześnie przetwarzane
    active_tasks = []
    result = []
    idx = 0

    while idx < len(sentences_val) or active_tasks:
        # Dodawanie nowych zadań do kolejki
        while len(active_tasks) < max_tasks and idx < len(sentences_val):
            batch_sentences = sentences_val[idx:idx + batch_size]
            batch_categories = categories_val[idx:idx + batch_size]

            sample_indices = random.sample(range(len(sentences_train)), min(100, len(sentences_train)))
            sample_sentences = [sentences_train[i] for i in sample_indices]
            sample_categories = [categories_train[i] for i in sample_indices]

            try:
                task_id = send_task(API_URL, sample_sentences, sample_categories, batch_sentences)
                print(f"Zadanie {task_id} zostało wysłane.")
                active_tasks.append({"task_id": task_id, "true_categories": batch_categories})
            except Exception as e:
                print(f"Błąd przy wysyłaniu zadania: {e}")

            idx += batch_size

        # Sprawdzanie statusu aktywnych zadań
        completed_tasks = []
        for task in active_tasks:
            try:
                status = check_task_status(API_URL, task["task_id"])
                if status == "SUCCESS":
                    print(f"Zadanie {task['task_id']} zakończone sukcesem.")
                    result_batch = get_task_result(API_URL, task["task_id"])
                    for true_category, predicted_category in zip(task["true_categories"], result_batch):
                        result.append({"true": true_category, "predicted": predicted_category})
                    completed_tasks.append(task)
                elif status == "PENDING":
                    print(f"Zadanie {task['task_id']} w trakcie przetwarzania.")
            except Exception as e:
                print(f"Błąd przy sprawdzaniu statusu zadania {task['task_id']}: {e}")

        # Usuwanie zakończonych zadań z aktywnej kolejki
        active_tasks = [task for task in active_tasks if task not in completed_tasks]

        # Oczekiwanie przed następnym sprawdzeniem statusu
        time.sleep(CHECK_INTERVAL)

    # Obliczanie metryk
    true_labels = [item["true"] for item in result]
    predicted_labels = [item["predicted"] for item in result]
    
    accuracy = accuracy_score(true_labels, predicted_labels)
    f1 = f1_score(true_labels, predicted_labels, average="weighted")
    
    return result, accuracy, f1

if __name__ == "__main__":
    sentences_train, categories_train, sentences_val, categories_val = process_and_split_dataset()
    
    result, accuracy, f1 = evaluate_model(sentences_train, categories_train, sentences_val, categories_val)
    
    print(f"Accuracy: {accuracy:.4f}")
    print(f"F1 Score: {f1:.4f}")
    print("\nPrzykładowe wyniki:")
    print(result[:10])  # Pierwsze 10 wyników
