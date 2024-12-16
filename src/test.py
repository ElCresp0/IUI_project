import argparse
import json
from time import sleep
import requests


parser = argparse.ArgumentParser()
parser.add_argument("--method", choices=["few_shot", "zero_shot"], default="few_shot", dest="method", type=str)
parser.add_argument("--task-id", default="", dest="task_id", type=str)
args = parser.parse_args()


body_zero_shot = {
    "sentences": [
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
    "categories": [
        "gotowanie",
        "polityka",
        "nauka"
    ]
}

body_few_shot = {
    "sample_sentences": [
        "wymieszać sos a następnie polać nim potrawę",
        "obrać warzywa, pokroić i smażyć na oliwie z oliwek przez kilka minut",
        "partia Polska-Polska wywiązuje się ze swojej pierwszej obietnicy wyborczej",
        "Prezydent Szczecina przejechał gęś. Nie będzie mógł kontynuować swojej kadencji.",
        "Energia potencjalna - energia, jaką ma ciało w zależności od położenia ciała w przestrzeni",
        "Kryptoanaliza (analiza kryptograficzna) - analiza systemu kryptograficznego w celu uzyskania informacji wrażliwej."
    ],
    "sentences": [
        "ugotować ryż, dodać bazylię i oregano, na koniec posypać serem",
        "Rafał Rafałczyk zdobył niecałe 20 procent głosów w swoim okręgu wyborczym",
        "Reakcja chemiczna - każdy proces, w wyniku którego pierwotna substancja zwana substratem przemienia się w inną substancję zwaną produktem.",
    ],
    "categories": [
        "gotowanie",
        "gotowanie",
        "polityka",
        "polityka",
        "nauka",
        "nauka"
    ]
}

################################
# create a task
################################

if args.task_id:
    task_id = args.task_id
else:
    body = body_few_shot if args.method == "few_shot" else body_zero_shot
    res = requests.post(f"http://localhost:8080/classifier/{args.method}/stormtrooper", json=body, params={"language": "pl"})
    res.raise_for_status()
    print(res.text)
    task_id = json.loads(res.text).get("taskId")

################################
# await task completion
################################

finished = False
new_line = ''
while not finished:
    res = requests.get(f"http://localhost:8080/task/status/{task_id}")
    res.raise_for_status()

    finished = (res.text == '"SUCCESS"')
    if not res.text in ['"PENDING"', '"SUCCESS"']:
        raise Exception(f"unexpected status: {res.text}")

    if not finished:
        new_line = '\n'
        print('.', end='', flush=True)
        seconds = 5
        sleep(seconds)
print('', end=new_line)

################################
# download task results
################################

res = requests.get(f"http://localhost:8080/task/result/{task_id}")
res.raise_for_status()
print(json.loads(res.text))

# """
# RESULT zero_shot (tylko trzecie od dołu niepoprawne):
# [
#     'gotowanie',
#     'gotowanie',
#     'gotowanie',
#     'polityka',
#     'polityka',
#     'polityka',
#     'gotowanie',
#     'nauka',
#     'nauka'
# ]
# """

# """
# RESULT few_shot (wszystkie poprawne):
# [
#     'gotowanie',
#     'polityka',
#     'nauka'
# ]
# """