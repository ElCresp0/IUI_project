from flair.data import Corpus
from flair.datasets import ColumnCorpus
from flair.models import TARSClassifier
from flair.trainers import ModelTrainer
from sentence_transformers import SentenceTransformer


# load and train the model

# load the data corpus
data_folder = 'data/pl'
columns = {0: 'label', 1: 'text'}

corpus: Corpus = ColumnCorpus(data_folder, columns,
                              train_file='train.csv',
                              test_file='test.csv',
                              dev_file='dev.csv')

label_dictionary = corpus.make_label_dictionary(label_type="label")
label_dictionary.add_item('O')

# load the model
model = SentenceTransformer("Voicelab/sbert-base-cased-pl")
tarsClassifier = TARSClassifier(model, label_dictionary=label_dictionary, label_type="label")

# train the model (it's saved automatically)
trainer = ModelTrainer(tarsClassifier, corpus)
trainer._save_model("base-model.pt")
trainer.train('./', max_epochs=64)
