import requests
import json

# Abakus anniversary date: lørdag 18. mars 2017
labamba_event_type = "party"

def is_actual_labamba_event(event):
    if event["eventType"] != labamba_event_type:
        return False
    if "AVLYST" in event["title"]:
        return False
    if "labamba" not in event["title"].lower() and "labamba" not in event["description"].lower():
        return False
    return True

labamba_event_list = []
labamba_event_count = 0
response = requests.get('https://lego-staging.abakus.no/api/v1/events/?date_after=2017-02-18&date_before=2022-01-23&page_size=60')
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
    json.dump({'events': labamba_event_list}, fp)