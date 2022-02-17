import requests
import json

labamba_event_type = "party"
# Spørringen nedenfor gir per nå en liste med alle arrangementer etter forrige jubileum
abakus_api_query = 'https://lego-staging.abakus.no/api/v1/events/?date_after=2017-02-18&date_before=2022-03-07'

def is_actual_labamba_event(event):
    if event["eventType"] != labamba_event_type:
        return False
    if "avlyst" in event["title"].lower():
        return False
    if "labamba" not in event["title"].lower() and "labamba" not in event["description"].lower():
        return False
    return True

labamba_event_list = []
labamba_event_count = 0
response = requests.get(abakus_api_query)
response_dict = response.json()

while response_dict.get("next", None) is not None:
    for event in response_dict["results"]:
        if is_actual_labamba_event(event):
            labamba_event_count += 1
            labamba_event_list.append(event)
    
    print(labamba_event_count)
    response = requests.get(response_dict["next"])
    response_dict = response.json()

with open("results/labamba_events_list.json", "w") as fp:
    json.dump({'events': labamba_event_list}, fp, sort_keys=True, indent=4)