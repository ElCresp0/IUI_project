# from sklearn.datasets import fetch_20newsgroups
from sklearn.metrics import classification_report
import numpy as np
import pandas as pd

from stormtrooper.set_fit import SetFitClassifier
# from stormtrooper import ZeroShotClassifier


ZERO_SHOT = 0
FEW_SHOT = 1

def main(mode: int):
    # Fetching data
    main_corpus = pd.DataFrame({
        "text": [
            "ugotować ryż, dodać bazylię i oregano, na koniec posypać serem",
            "wymieszać sos a następnie polać nim potrawę",
            "obrać warzywa, pokroić i smażyć na oliwie z oliwek przez kilka minut",
            "Rafał Rafałczyk zdobył niecałe 20 procent głosów w swoim okręgu wyborczym",
            "partia Polska-Polska wywiązuje się ze swojej pierwszej obietnicy wyborczej",
            "Prezydent Szczecina przejechał gęś. Nie będzie mógł kontynuować swojej kadencji.",
            "Reakcja chemiczna - każdy proces, w wyniku którego pierwotna substancja zwana substratem przemienia się w inną substancję zwaną produktem.",
            "Energia potencjalna - energia, jaką ma ciało w zależności od położenia ciała w przestrzeni",
            "Kryptoanaliza (analiza kryptograficzna) - analiza systemu kryptograficznego w celu uzyskania informacji wrażliwej."
        ],
        "label": ["gotowanie", "gotowanie", "gotowanie", "polityka", "polityka", "polityka", "nauka", "nauka", "nauka"]
    })

    if mode == ZERO_SHOT:
        corpus = np.array(
            [
                "to zdanie to gotowanie",
                "to zdanie to polityka",
                "to zdanie to nauka"
            ])
        group_labels = np.array(["gotowanie", "polityka", "nauka"])
    else:
        corpus = main_corpus["text"].to_numpy()
        group_labels = main_corpus["label"].to_numpy()
    
    # Wrangling data into a dataframe and selecting training examples
    data = pd.DataFrame({"text": corpus, "label": group_labels})
    if mode == ZERO_SHOT:
        training_data = data.groupby("label").sample(1)
        test_data = pd.DataFrame({"text": main_corpus["text"][[0, 3, 6]].to_numpy(),
                                  "label": main_corpus["label"][[0, 3, 6]].to_numpy()})
    else:
        training_data = data.groupby("label").sample(2)
        test_data = data.drop(index=training_data.index).reset_index()

    # Fitting model
    model = SetFitClassifier("Voicelab/sbert-base-cased-pl")
    # for zero-shot method the training data is generic so the model is not actually trained for classification here
    model.fit(training_data["text"], training_data["label"])

    # Inference
    y_pred = model.predict(test_data["text"])

    # Evaluation
    print(classification_report(test_data["label"], y_pred))

if __name__ == "__main__":
    # zero-shot
    main(ZERO_SHOT)
    #               precision    recall  f1-score   support

    #    gotowanie       0.50      1.00      0.67         1
    #        nauka       0.00      0.00      0.00         1
    #     polityka       1.00      1.00      1.00         1

    #     accuracy                           0.67         3
    #    macro avg       0.50      0.67      0.56         3
    # weighted avg       0.50      0.67      0.56         3

    # few-shot
    main(FEW_SHOT)
    #               precision    recall  f1-score   support

    #    gotowanie       1.00      1.00      1.00         1
    #        nauka       1.00      1.00      1.00         1
    #     polityka       1.00      1.00      1.00         1

    #     accuracy                           1.00         3
    #    macro avg       1.00      1.00      1.00         3
    # weighted avg       1.00      1.00      1.00         3
