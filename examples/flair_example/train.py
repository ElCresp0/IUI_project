import pandas as pd

from flair.models import TARSClassifier
from flair.data import Sentence

from sklearn.model_selection import train_test_split

# create the dataset

# # download the dataset
# df = pd.read_json("hf://datasets/rafalposwiata/open-coursebooks-pl/data.jsonl", lines=True)

# # take "field" and "paragraphs" columns where "paragraphs" in not an empty list
# df = (df[df["paragraphs"].astype(bool)]).reset_index()[["field", "paragraphs"]]

# # convert "paragraphs" from list to a string
# df["text"] = df["paragraphs"].apply(lambda x: ".".join(x))

# # TARS preprocessing
# df['label'] = df['field'].apply(lambda field: '__label__' + field.replace(' ', '_'))
# df = df[["label", "text"]]

# # split the dataset
# train, test = train_test_split(df, test_size=0.2)
# test, dev = train_test_split(test, test_size=0.5)

# for split, split_name in [(train, "train"),(test, "test"),(dev, "dev")]:
#     split.to_csv(f'data/pl/{split_name}.csv', sep='\t', index = False, header = False)


# train the model

from flair.data import Corpus
from flair.datasets import ColumnCorpus
from flair.embeddings import WordEmbeddings, FlairEmbeddings, DocumentLSTMEmbeddings
from flair.models import TextClassifier
from flair.trainers import ModelTrainer
from pathlib import Path

data_folder = 'data/pl'
columns = {0: 'label', 1: 'text'}

corpus: Corpus = ColumnCorpus(data_folder, columns,
                              train_file='train.csv',
                              test_file='test.csv',
                              dev_file='dev.csv')

label_dictionary = corpus.make_label_dictionary(label_type="label")
label_dictionary.add_item('O')

# corpus = NLPTaskDataFetcher.load_classification_corpus(Path('./'), test_file='test.csv', dev_file='dev.csv', train_file='train.csv')

word_embeddings = [WordEmbeddings('glove'), FlairEmbeddings('news-forward-fast'), FlairEmbeddings('news-backward-fast')]
document_embeddings = DocumentLSTMEmbeddings(word_embeddings, hidden_size=512, reproject_words=True, reproject_words_dimension=256)

# stacked_embeddings = StackedEmbeddings([WordEmbeddings('glove'), FlairEmbeddings('news-forward-fast'), FlairEmbeddings('news-backward-fast')])

classifier = TextClassifier(document_embeddings, label_type="label", label_dictionary=label_dictionary, multi_label=False)
trainer = ModelTrainer(classifier, corpus)
trainer.train('./', max_epochs=10)
