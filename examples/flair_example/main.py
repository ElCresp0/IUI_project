# https://medium.com/@AmyGrabNGoInfo/sentiment-analysis-hugging-face-zero-shot-model-vs-flair-pre-trained-model-57047452225d
# ^ tu jkbc jakis link apropo porownywania modeli


# TODO:
# - run with ../SetFit-Polish data


import pandas as pd
from flair.models import TARSClassifier
from flair.data import Sentence


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

# 1. Load our pre-trained TARS model for English
tars = TARSClassifier.load('tars-base')

tars = TARSClassifier(task_name="ZeroShot", embeddings="Voicelab/sbert-base-cased-pl")
"""
Args:
    task_name: a string depicting the name of the task.
    label_dictionary: dictionary of labels you want to predict.
    label_type: label_type: name of the label
   >embeddings: name of the pre-trained transformer model e.g., 'bert-base-uncased'.
    num_negative_labels_to_sample: number of negative labels to sample for each positive labels against a
        sentence during training. Defaults to 2 negative labels for each positive label. The model would sample all the negative labels if None is passed. That slows down the training considerably.
    multi_label: auto-detected by default, but you can set this to True to force multi-label predictions
        or False to force single-label predictions.
    multi_label_threshold: If multi-label you can set the threshold to make predictions.
    beta: Parameter for F-beta score for evaluation and training annealing.
    prefix: if True, the label will be concatenated at the start, else on the end.
    **tagger_args: The arguments propagated to FewshotClassifier.__init__
"""

# 2. Prepare a test sentence
sentence = Sentence("I am so glad you liked it!")
sentence = Sentence("wymieszać sos a następnie polać nim potrawę")

# 3. Define some classes that you want to predict using descriptive names
classes = ["happy", "sad"]
classes=["gotowanie", "polityka", "nauka"]

#4. Predict for these classes
tars.predict_zero_shot(sentence, classes)

# Print sentence with predicted labels
print(sentence)




from flair.models import TARSTagger
from flair.data import Sentence

# 1. Load zero-shot NER tagger
tars = TARSTagger.load('tars-ner')

# 2. Prepare some test sentences
sentences = [
    Sentence("The Humboldt University of Berlin is situated near the Spree in Berlin, Germany"),
    Sentence("Bayern Munich played against Real Madrid"),
    Sentence("I flew with an Airbus A380 to Peru to pick up my Porsche Cayenne"),
    Sentence("Game of Thrones is my favorite series"),
]
sentences = [
            Sentence("ugotować ryż, dodać bazylię i oregano, na koniec posypać serem"),
            Sentence("wymieszać sos a następnie polać nim potrawę"),
            Sentence("obrać warzywa, pokroić i smażyć na oliwie z oliwek przez kilka minut"),
            Sentence("Rafał Rafałczyk zdobył niecałe 20 procent głosów w swoim okręgu wyborczym"),
            Sentence("partia Polska-Polska wywiązuje się ze swojej pierwszej obietnicy wyborczej"),
            Sentence("Prezydent Szczecina przejechał gęś. Nie będzie mógł kontynuować swojej kadencji."),
            Sentence("Reakcja chemiczna - każdy proces, w wyniku którego pierwotna substancja zwana substratem przemienia się w inną substancję zwaną produktem."),
            Sentence("Energia potencjalna - energia, jaką ma ciało w zależności od położenia ciała w przestrzeni"),
            Sentence("Kryptoanaliza (analiza kryptograficzna) - analiza systemu kryptograficznego w celu uzyskania informacji wrażliwej.")
]

# 3. Define some classes of named entities such as "soccer teams", "TV shows" and "rivers"
labels = ["Soccer Team", "University", "Vehicle", "River", "City", "Country", "Person", "Movie", "TV Show"]
labels = ["gotowanie", "polityka", "nauka"]
tars.add_and_switch_to_new_task('task 1', labels, label_type='ner')

# 4. Predict for these classes and print results
for sentence in sentences:
    pred = tars.predict(sentence)
    if pred:
        print(f"pred: {pred}")
    print(sentence.to_tagged_string("ner"))
