from model import ModelService
from stormtrooper.set_fit import SetFitClassifier

# TODO:
# tu i/lub w Dockerflie zmienić tak żeby TYLKO kontener worker (celery) ściągał model
# model_path = ModelService().get_sbert_base_cased_pl()
# _ = SetFitClassifier(model_path)
