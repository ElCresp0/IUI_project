import requests
from requests.adapters import HTTPAdapter, Retry
import tqdm

from .framework import Framework


class BielikApiService(Framework):
    def __init__(self):
        super().__init__()
        login = ''
        password = ''
        auth = (login, password)

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

    def zero_shot_classification(self, args: dict):
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
        return results

    def few_shot_classification(self, args: dict):
        def one_text_classification(text, examples):
            examples_text = '\n'.join(
                [f'Przykład: {t}\nKategoria: {l}' for t, l in zip(
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
        return results

    def _request_api(self, prompt: str):
        data = {
            'messages': [{'role': 'system', 'content': self.system_prompt}, {'role': 'user', 'content': prompt}],
            'max_length': self.max_response_length,
            'temperature': self.temperature,
        }

        response = self.session.put(
            self.base_url,
            json=data,
            headers={'Accept': 'application/json',
                     'Content-Type': 'application/json'},
            ** self.auth_kwargs,
        )
        response.raise_for_status()
        response_json = response.json()
        return response_json.get('response', '')
