import time
import random
from sklearn.metrics import accuracy_score, f1_score
from utilities import *


def evaluate_few_shot(
    sentences_train, 
    categories_train, 
    sentences_val, 
    categories_val, 
    framework="stormtrooper", 
    language="pl",
    sample_size=100,    # Number of sentences to use for few-shot learning
    batch_size=100,     # Number of sentences to process in a single task
    max_tasks=5         # Number of tasks that can be processed concurrently
):
    """Evaluate a few-shot learning model using the API and computes accuracy and F1 score."""
    active_tasks = []
    result = []
    idx = 0

    while idx < len(sentences_val) or active_tasks:
        # Adding new tasks to the queue
        while len(active_tasks) < max_tasks and idx < len(sentences_val):
            batch_sentences = sentences_val[idx:idx + batch_size]
            batch_categories = categories_val[idx:idx + batch_size]

            sample_indices = random.sample(range(len(sentences_train)), min(sample_size, len(sentences_train)))
            sample_sentences = [sentences_train[i] for i in sample_indices]
            sample_categories = [categories_train[i] for i in sample_indices]

            try:
                task_id = create_few_shot_task(framework, language, sample_sentences, batch_sentences, sample_categories)
                print(f"Task {task_id} has been sent.")
                active_tasks.append({"task_id": task_id, "true_categories": batch_categories})
            except Exception as e:
                print(f"Error sending task: {e}")

            idx += batch_size

        # Checking the status of active tasks
        completed_tasks = []
        for task in active_tasks:
            try:
                response = get_task_status(task["task_id"])
                if response["status"] == "SUCCESS":
                    print(f"Task {task['task_id']} completed successfully.")
                    result_batch = get_task_result(task["task_id"])
                    for true_category, predicted_category in zip(task["true_categories"], result_batch):
                        result.append({"true": true_category, "predicted": predicted_category})
                    completed_tasks.append(task)
                elif response["status"] == "PENDING":
                    print(f"Task {task['task_id']} is still processing.")
            except Exception as e:
                print(f"Error checking status for task {task['task_id']}: {e}")

        # Removing completed tasks from the active queue
        active_tasks = [task for task in active_tasks if task not in completed_tasks]

        # Waiting before the next status check
        time.sleep(CHECK_INTERVAL)

    # Calculating metrics
    true_labels = [item["true"] for item in result]
    predicted_labels = [item["predicted"] for item in result]
    
    accuracy = accuracy_score(true_labels, predicted_labels)
    f1 = f1_score(true_labels, predicted_labels, average="weighted")
    
    return result, accuracy, f1

def evaluate_zero_shot(
    sentences_val, 
    categories_val, 
    framework="stormtrooper", 
    language="pl",
    batch_size=100,     # Number of sentences to process in a single task
    max_tasks=5         # Number of tasks that can be processed concurrently
):
    """Evaluate a zero-shot learning model using the API and computes accuracy and F1 score."""
    active_tasks = []
    result = []
    idx = 0

    while idx < len(sentences_val) or active_tasks:
        # Adding new tasks to the queue
        while len(active_tasks) < max_tasks and idx < len(sentences_val):
            batch_sentences = sentences_val[idx:idx + batch_size]
            batch_categories = categories_val[idx:idx + batch_size]

            try:
                task_id = create_zero_shot_task(framework, language, batch_sentences, batch_categories)
                print(f"Task {task_id} has been sent.")
                active_tasks.append({"task_id": task_id, "true_categories": batch_categories})
            except Exception as e:
                print(f"Error sending task: {e}")

            idx += batch_size

        # Checking the status of active tasks
        completed_tasks = []
        for task in active_tasks:
            try:
                response = get_task_status(task["task_id"])
                if response["status"] == "SUCCESS":
                    print(f"Task {task['task_id']} completed successfully.")
                    result_batch = get_task_result(task["task_id"])
                    for true_category, predicted_category in zip(task["true_categories"], result_batch):
                        result.append({"true": true_category, "predicted": predicted_category})
                    completed_tasks.append(task)
                elif response["status"] == "PENDING":
                    pass
                    # print(f"Task {task['task_id']} is still processing.")
            except Exception as e:
                print(f"Error checking status for task {task['task_id']}: {e}")

        # Removing completed tasks from the active queue
        active_tasks = [task for task in active_tasks if task not in completed_tasks]

        # Waiting before the next status check
        time.sleep(CHECK_INTERVAL)

    # Calculating metrics
    true_labels = [item["true"] for item in result]
    predicted_labels = [item["predicted"] for item in result]
    
    accuracy = accuracy_score(true_labels, predicted_labels)
    f1 = f1_score(true_labels, predicted_labels, average="weighted")
    
    return result, accuracy, f1
