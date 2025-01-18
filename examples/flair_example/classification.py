# from pathlib import Path
import pandas as pd
from sentence_transformers import SentenceTransformer

from flair.models import TARSClassifier
from flair.trainers import ModelTrainer
from flair.data import Sentence, Corpus
# from flair.datasets import ColumnCorpus, ClassificationDataset, CSVClassificationDataset

ZERO_SHOT = 0
FEW_SHOT = 1


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

def create_corpus(text: list[str], labels: list[str]) -> Corpus:
    # load the data corpus
    def create_sentence(sentence, label):
        ret = Sentence(sentence)
        ret.add_label("label", label)
        return ret
    sentences = [create_sentence(sentence, label) for sentence,label in zip(text, labels)]
    return Corpus(train=sentences, dev=[], test=[])

def main(mode: int):
    text = main_corpus["text"].to_numpy()
    label = main_corpus["label"].to_numpy()
    data = pd.DataFrame({"text": text, "label": label})

    # 1. Load a pre-trained TARS model for Polish (use a sentence_transformer from huggingface)
    model = SentenceTransformer("Voicelab/sbert-base-cased-pl")

    if mode == ZERO_SHOT:

        tarsClassifier = TARSClassifier(model)

        # 2. Prepare a test sentence
        sentences = [Sentence(sentence) for sentence in data["text"]]

        # 3. Define some classes that you want to predict using descriptive names
        classes = ["gotowanie", "polityka", "nauka"]

        for sentence in sentences:
            #4. Predict for these classes
            tarsClassifier.predict_zero_shot(sentence, classes)
            
            # Print sentence with predicted labels
            print(f"{sentence.text} -> {sentence.labels}")

    if mode == FEW_SHOT:

        corpus = create_corpus(data["text"][[0,1,3,4,6,7]], data["label"][[0,1,3,4,6,7]])
        label_dictionary = corpus.make_label_dictionary(label_type="label")
        # label_dictionary.add_item('O')
        tarsClassifier = TARSClassifier(model, label_dictionary=label_dictionary, label_type="label")

        trainer = ModelTrainer(tarsClassifier, corpus)
        trainer.train('./', max_epochs=min(len(corpus.train), 5), save_final_model=False)

        # 2. Prepare test sentences
        sentences = [Sentence(sentence) for sentence in data["text"][[2,5,8]]]

        for sentence in sentences:
            tarsClassifier.predict(sentence)
            print(f"{sentence.text} -> {sentence.get_label()}")

if __name__ == "__main__":
    main(ZERO_SHOT)
    main(FEW_SHOT)
