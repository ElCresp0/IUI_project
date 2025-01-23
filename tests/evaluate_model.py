import time
import random
from sklearn.metrics import accuracy_score, f1_score
from tqdm import tqdm
from collections import defaultdict
from utilities import *

def get_sample_with_all_labels(sentences, categories, sample_size):
    label_to_examples = defaultdict(list)
    for sentence, category in zip(sentences, categories):
        label_to_examples[category].append(sentence)
    
    # Ensure at least one example per label
    sample_sentences = []
    sample_categories = []
    for label, examples in label_to_examples.items():
        chosen_example = random.choice(examples)
        sample_sentences.append(chosen_example)
        sample_categories.append(label)
    
    # Fill up the remaining sample size randomly
    remaining_samples_needed = sample_size - len(sample_sentences)
    if remaining_samples_needed > 0:
        all_examples = [(sentence, category) for sentence, category in zip(sentences, categories) if sentence not in sample_sentences]
        additional_samples = random.sample(all_examples, min(remaining_samples_needed, len(all_examples)))
        sample_sentences.extend([sample[0] for sample in additional_samples])
        sample_categories.extend([sample[1] for sample in additional_samples])
    
    return sample_sentences, sample_categories

def evaluate_few_shot(
    sentences_train, 
    categories_train, 
    sentences_val, 
    categories_val, 
    framework="stormtrooper", 
    language="pl",
    sample_size=20,      # Number of sentences to use for few-shot learning
    batch_size=5,        # Number of sentences to process in a single task
    max_tasks=20         # Number of tasks that can be processed concurrently
):
    """Evaluate a few-shot learning model using the API and computes accuracy and F1 score."""
    active_tasks = []
    result = []
    idx = 0
    
    total_batches = (len(sentences_val) + batch_size - 1) // batch_size
    pbar = tqdm(total=total_batches, desc="Processing Few-Shot Evaluation")

    while idx < len(sentences_val) or active_tasks:
        # Adding new tasks to the queue
        while len(active_tasks) < max_tasks and idx < len(sentences_val):
            batch_sentences = sentences_val[idx:idx + batch_size]
            batch_categories = categories_val[idx:idx + batch_size]

            sample_sentences, sample_categories = get_sample_with_all_labels(sentences_train, categories_train, sample_size)

            try:
                task_id = create_few_shot_task(framework, language, sample_sentences, batch_sentences, sample_categories)
                print(f"Task {task_id} has been sent.")
                active_tasks.append({"task_id": task_id, "true_categories": batch_categories, "batch_sentences": batch_sentences})
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
                    pbar.update(1)
                elif response["status"] == "FAILURE":
                    print(f"Task {task['task_id']} failed. Resending with new examples.")
                    sample_sentences, sample_categories = get_sample_with_all_labels(sentences_train, categories_train, sample_size)
                    new_task_id = create_few_shot_task(framework, language, sample_sentences, task["batch_sentences"], sample_categories)
                    print(f"New Task {new_task_id} has been sent.")
                    task["task_id"] = new_task_id
                elif response["status"] == "PENDING":
                    pass
                    # print(f"Task {task['task_id']} is still processing.")
            except Exception as e:
                print(f"Error checking status for task {task['task_id']}: {e}")

        # Removing completed tasks from the active queue
        active_tasks = [task for task in active_tasks if task not in completed_tasks]

        # Waiting before the next status check
        time.sleep(CHECK_INTERVAL)

    pbar.close()
    
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
    
    unique_batch_categories = list(set(batch_categories))

    total_batches = (len(sentences_val) + batch_size - 1) // batch_size
    pbar = tqdm(total=total_batches, desc="Processing Zero-Shot Evaluation")

    while idx < len(sentences_val) or active_tasks:
        # Adding new tasks to the queue
        while len(active_tasks) < max_tasks and idx < len(sentences_val):
            batch_sentences = sentences_val[idx:idx + batch_size]
            batch_categories = categories_val[idx:idx + batch_size]

            try:
                task_id = create_zero_shot_task(framework, language, batch_sentences, unique_batch_categories)
                print(f"Task {task_id} has been sent.")
                active_tasks.append({"task_id": task_id, "true_categories": batch_categories, "batch_sentences": batch_sentences})
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
                elif response["status"] == "FAILURE":
                    print(f"Task {task['task_id']} failed. Resending with new examples.")
                    new_task_id = create_zero_shot_task(framework, language, task["batch_sentences"], unique_batch_categories)
                    print(f"New Task {new_task_id} has been sent.")
                    task["task_id"] = new_task_id
                elif response["status"] == "PENDING":
                    pass
                    # print(f"Task {task['task_id']} is still processing.")
            except Exception as e:
                print(f"Error checking status for task {task['task_id']}: {e}")

        # Removing completed tasks from the active queue
        active_tasks = [task for task in active_tasks if task not in completed_tasks]

        # Waiting before the next status check
        time.sleep(CHECK_INTERVAL)

    pbar.close()
    
    # Calculating metrics
    true_labels = [item["true"] for item in result]
    predicted_labels = [item["predicted"] for item in result]
    
    accuracy = accuracy_score(true_labels, predicted_labels)
    f1 = f1_score(true_labels, predicted_labels, average="weighted")
    
    return result, accuracy, f1
