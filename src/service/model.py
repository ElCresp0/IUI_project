
# this is service which give you path to selected model
# or in the future could load model
class ModelService:
    # used to zero-shot or few-shot, question mark - needs to be verified
    # language
    def __init__(self):
        self.path_sbert_base_cased_pl: str = "Voicelab/sbert-base-cased-pl"
        self.path_bielik_11B_v2: str = "speakleash/Bielik-11B-v2"
        self.path_bart_large_mnli: str = "facebook/bart-large-mnli"
        self.path_gpt4_x_alpaca: str = "chavinlo/gpt4-x-alpaca"
        self.path_few_shot_fb_bart_large_mnli: str = "tyzp-INC/few-shot-fb-bart-large-mnli"

    # zero-shot / few-shot
    # PL
    def get_sbert_base_cased_pl(self) -> str:
        return self.path_sbert_base_cased_pl
    
    # zero-shot / few-shot ?
    # PL
    def get_bielik_11B_v2(self) -> str:
        return self.path_bielik_11B_v2
    
    # zero-shot / few-shot ?
    # EN
    def get_bart_large_mnli(self) -> str:
        return self.path_bart_large_mnli
    
    # zero-shot / few-shot ?
    # EN
    def get_gpt4_x_alpaca(self) -> str:
        return self.path_gpt4_x_alpaca
    
    # zero-shot ? / few-shot
    # EN
    def get_few_shot_fb_bart_large_mnli(self) -> str:
        return self.path_few_shot_fb_bart_large_mnli
