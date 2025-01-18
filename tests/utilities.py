import requests
import time

BASE_URL = "http://localhost:8080"
CHECK_INTERVAL = 2

def get_task_status(task_id: str):
    """Sends a GET request to /task/status/{task_id} and returns the task status."""
    url = f"{BASE_URL}/task/status/{task_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json() # Return as a dictionary with status (PENDING, SUCCESS) and progress (0-100%)
        
def get_task_result(task_id: str):
    """Sends a GET request to /task/result/{task_id} and returns the task result."""
    url = f"{BASE_URL}/task/result/{task_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json() # Direct list of resulting labels     
    
def create_zero_shot_task(framework: str, language: str, sentences: list, categories: list):
    """Sends a POST request to /classifier/zero_shot/{framework} to create a Zero-shot task."""
    url = f"{BASE_URL}/classifier/zero_shot/{framework}"
    payload = {
        "sentences": sentences,
        "categories": categories
    }
    params = {
        "language": language
    }
    response = requests.post(url, json=payload, params=params)
    response.raise_for_status()
    return response.json()["taskId"] # Returns the task ID

def create_few_shot_task(framework: str, language: str, sample_sentences: list, sentences: list, categories: list):
    """Sends a POST request to /classifier/few_shot/{framework} to create a Few-shot task."""
    url = f"{BASE_URL}/classifier/few_shot/{framework}"
    payload = {
        "sample_sentences": sample_sentences,
        "sentences": sentences,
        "categories": categories
    }
    params = {
        "language": language
    }
    response = requests.post(url, json=payload, params=params)
    response.raise_for_status()
    return response.json()["taskId"] # Returns the task ID

if __name__ == "__main__":
    # test 1
    sentences = ["This is a test sentence.", "Another test sentence.", "This is not a test sentence.", "This is a test sentence.", "Another test sentence.", "This is not a test sentence"]
    categories = ["test", "test", "non-test", "test", "test", "non-test"]
    task_id = create_zero_shot_task("stormtrooper", "en", sentences, categories)
    while True:
        time.sleep(CHECK_INTERVAL)
        status = get_task_status(task_id)
        print(status)
        if status["status"] == "SUCCESS":
            print(get_task_result(task_id))
            break
    
    # test 2
    sample_sentences = ["To jest zdanie testowe.", "Kolejne zdanie testowe.", "To nie jest zdanie testowe.", "To jest zdanie testowe.", "Kolejne zdanie testowe.", "To nie jest zdanie testowe."]
    categories = ["test", "test", "non-test", "test", "test", "non-test"]
    sentences = ["To jest zdanie testowe.", "To nie jest zdanie testowe."]
    task_id = create_few_shot_task("stormtrooper", "pl", sample_sentences, sentences, categories)
    while True:
        time.sleep(CHECK_INTERVAL)
        status = get_task_status(task_id)
        print(status)
        if status["status"] == "SUCCESS":
            print(get_task_result(task_id))
            break
        