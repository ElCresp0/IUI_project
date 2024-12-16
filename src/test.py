import json
from time import sleep
import requests

body = {
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

################################
# create a task
################################

res = requests.post("http://localhost:8080/classifier/zero_shot/stormtrooper", json=body, params={"language": "pl"})
res.raise_for_status()
print(res.text)
task_id = json.loads(res.text).get("taskId")

################################
# await task completion
################################

finished = False
while not finished:
    res = requests.get(f"http://localhost:8080/task/status/{task_id}")
    res.raise_for_status()

    finished = (res.text == '"SUCCESS"')
    if not res.text in ['"PENDING"', '"SUCCESS"']:
        raise Exception(f"unexpected status: {res.text}")

    if not finished:
        print('.', end='', flush=True)
        seconds = 3
        sleep(seconds)

################################
# download task results
################################

res = requests.get(f"http://localhost:8080/task/result/{task_id}")
res.raise_for_status()
print(json.loads(res.text))

# """
# RESULT:
# [
#     "gotowanie",
#     "gotowanie",
#     "gotowanie",
#     "polityka",
#     "polityka",
#     "polityka",
#     "gotowanie",
#     "nauka",
#     "nauka"
# ]
# """