import json

labamba_event_list = None
total_labamba_time = 0

with open("results/labamba_events_list.json", "r") as fp:
    labamba_event_list = json.load(fp)["events"]

for event in labamba_event_list:
    start_time = event["startTime"].split("T")[1].split(":")[:2]
    end_time = event["endTime"].split("T")[1].split(":")[:2]
    for i in range(2):
        start_time[i] = int(start_time[i])
        end_time[i] = int(end_time[i])
    if end_time[0] < 5:
        end_time[0] += 24
    print(f"{start_time} {end_time}")
    duration = ((end_time[0] - start_time[0])*60) - start_time[1] + end_time[1]
    print(duration)
    total_labamba_time += duration

result = f"Total LaBamba time in minutes: {total_labamba_time}"
print(result)

with open("results/abakus_statistics.txt", "a") as f:
    f.write(result)
