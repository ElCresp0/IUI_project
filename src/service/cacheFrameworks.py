from stormtrooper.set_fit import SetFitClassifier

from model import ModelService


model_path = ModelService().get_sbert_base_cased_pl()
_ = SetFitClassifier(model_path)
