import requests
import json

bedpres_event_types = ["company_presentation", "alternative_presentation"]
# Spørringen nedenfor gir per nå en liste med alle arrangementer etter forrige jubileum
abakus_api_query = 'https://lego-staging.abakus.no/api/v1/events/?date_after=2017-02-18&date_before=2022-03-07'

def is_bedpres(event):
    if event["eventType"] not in bedpres_event_types:
        return False
    if "avlyst" in event["title"].lower():
        return False
    return True

bedpres_event_list = []
bedpres_count = 0
response = requests.get(abakus_api_query)
response_dict = response.json()

while response_dict.get("next", None) is not None:
    for event in response_dict["results"]:
        if is_bedpres(event):
            bedpres_count += 1
            bedpres_event_list.append(event)
    
    print(bedpres_count)
    response = requests.get(response_dict["next"])
    response_dict = response.json()

with open("results/bedpres_list.json", "w") as fp:
    json.dump({'events': bedpres_event_list}, fp, sort_keys=True, indent=4)

result = f"Total number of bedpres: {bedpres_count}"
print(result)

with open("results/abakus_statistics.txt", "a") as f:
    f.write(result + "\n")
