import configparser
import logging

import requests
import tqdm
from requests.adapters import HTTPAdapter, Retry

from .framework import Framework


NO_RESPONSE = ''


class BielikApiService(Framework):
    """This class maps classification tasks to Bielik API calls

    Use it to execute zero_shot and few_shot text classification
    """

    def __init__(self):
        super().__init__()
        # login = ''
        # password = ''
        config = configparser.ConfigParser()
        config.read(['config/default.ini', 'config/config.ini'])

        login = config["bielik"]["login"]
        password = config["bielik"]["password"]
        auth = (login, password)
        if not any(auth):
            logging.warning(
                "No login and password provided in config/config.ini")

        self.base_url = 'https://153.19.239.239/api/llm/prompt/chat'
        self.auth_kwargs = {
            'auth': auth,
            'verify': False,
        }
        self.system_prompt = 'Odpowiadaj krótko i zwięźle'
        self.temperature = 0.1
        self.max_response_length = 16

        self.session = requests.Session()
        retries = Retry(total=3, status_forcelist=[503, 504])
        self.session.mount("http://", HTTPAdapter(max_retries=retries))
        self.session.mount("https://", HTTPAdapter(max_retries=retries))

    def _maybe_results(self, results: list):
        return results if any(results) else NO_RESPONSE

    def zero_shot_classification(self, args: dict):
        """Run zero-shot classification using this framework

        input: args:dict like {"text": text, "label": label}
        ^label should be a list of labels
        """
        def one_text_classification(text, labels):
            labels_string = ', '.join(labels)
            prompt = (
                f'Przyporządkuj podany tekst do jednej z kategorii: {labels_string}.\n'
                f'Możesz używać wyłącznie tych kategorii i musisz wybrać jedną.\n\n'
                f'Tekst: {text}\n'
                f'Kategoria:'
            )
            return self._request_api(prompt)

        results = []
        for text in tqdm.tqdm(args['text'], desc='Text processing'):
            result = one_text_classification(text, args['label'])
            results.append(result)
        return self._maybe_results(results)

    def few_shot_classification(self, args: dict):
        """Run few-shot classification using this framework

        input: args:dict like {"text": text, "examples": examples}
        """

        def one_text_classification(text, examples):
            examples_text = '\n'.join(
                [f'Przykład: {text}\nKategoria: {label}' for text, label in zip(
                    examples['text'], examples['label'], strict=False)]
            )

            unique_labels = list(set(examples['label']))
            labels_string = ', '.join(unique_labels)

            prompt = (
                f'Na podstawie poniższych przykładów przypisz tekst do jednej z kategorii: {labels_string}.\n'
                f'Możesz używać wyłącznie tych kategorii i musisz wybrać jedną.\n\n'
                f'{examples_text}\n\n'
                f'Nowy tekst: {text}\nKategoria:'
            )
            return self._request_api(prompt)

        results = []
        for text in tqdm.tqdm(args['text'], desc='Text processing'):
            result = one_text_classification(text, args['examples'])
            results.append(result)
        return self._maybe_results(results)

    def _request_api(self, prompt: str):
        data = {
            'messages': [{'role': 'system', 'content': self.system_prompt}, {'role': 'user', 'content': prompt}],
            'max_length': self.max_response_length,
            'temperature': self.temperature,
        }

        try:
            response = self.session.put(
                self.base_url,
                json=data,
                headers={'Accept': 'application/json',
                         'Content-Type': 'application/json'},
                timeout=10,
                ** self.auth_kwargs,
            )
            response.raise_for_status()
        except Exception as e:
            raise Exception(
                f"Response {response.status_code}. Prompt: {prompt}") from e
            # return NO_RESPONSE

        if response.status_code > 500:
            logging.warning(f'bielik response {response.status_code}:\n'
                            f'prompt: {prompt}')

        response_json = response.json()
        return response_json.get('response', NO_RESPONSE)
