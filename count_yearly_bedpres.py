import requests
import json

# Abakus anniversary date: lørdag 18. mars 2017
bedpres_event_types = ["company_presentation", "alternative_presentation"]

def is_bedpres(event):
    if event["eventType"] not in bedpres_event_types:
        return False
    if "avlyst" in event["title"].lower():
        return False
    return True

event_list = []
yearly_event_count = {}
response = requests.get('https://lego-staging.abakus.no/api/v1/events/?date_after=2017-01-01&date_before=2022-03-10')
response_dict = response.json()

while response_dict.get("next", None) is not None:
    for event in response_dict["results"]:
        year = int(event["startTime"].split("-")[0])
        if not year in yearly_event_count:
            yearly_event_count[year] = 0
        if is_bedpres(event):
            yearly_event_count[year] += 1
            event_list.append(event)
    
    print(yearly_event_count)
    
    response = requests.get(response_dict["next"])
    response_dict = response.json()

with open("results/bedpres_yearly_list.json", "w") as fp:
    json.dump({'events': event_list}, fp, sort_keys=True, indent=4)

printout = f"Number of yearly bedpres: {yearly_event_count}\n"
with open("results/abakus_statistics.txt", "a") as f:
    f.write(printout)
