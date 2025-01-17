import pandas as pd
from flair.data import Sentence
from pathlib import Path
from sklearn.model_selection import train_test_split

# create the dataset

# download the dataset
df = pd.read_json("hf://datasets/rafalposwiata/open-coursebooks-pl/data.jsonl", lines=True)

# take "field" and "paragraphs" columns where "paragraphs" in not an empty list
df = (df[df["paragraphs"].astype(bool)]).reset_index()[["field", "paragraphs"]]

# convert "paragraphs" from list to a string
df["text"] = df["paragraphs"].apply(lambda x: ".".join(x))

# TARS preprocessing
df['label'] = df['field'].apply(lambda field: '__label__' + field.replace(' ', '_'))
df = df[["label", "text"]]

# split the dataset
train, test = train_test_split(df, test_size=0.2)
test, dev = train_test_split(test, test_size=0.5)

data_dir = Path("data").absolute()
if not data_dir.exists():
    data_dir.mkdir()

for split, split_name in [(train, "train"),(test, "test"),(dev, "dev")]:
    split.to_csv(f'data/pl/{split_name}.csv', sep='\t', index = False, header = False)
