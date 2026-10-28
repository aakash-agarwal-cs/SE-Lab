import json
import secrets
from datetime import datetime

# Global state
routes = {"R1": {"name": "Main Gate - Library", "trips": []},
          "R2": {"name": "Hostel - Sports Complex", "trips": []},
          "R3": {"name": "Admin Block - Metro", "trips": []}}
MIN_CAPACITY = 10

def add_trip_log(route_id, passenger_count, logs=[]):
    if not isinstance(passenger_count, int) or passenger_count < 0:
        raise ValueError("passenger_count must be a non-negative integer, got %r" % (passenger_count,))
    routes[route_id]["trips"].append(passenger_count)
    logs.append("%s: %s carried %s" % (datetime.now(), route_id, passenger_count))
    return logs

def remove_route(route_id):
    del routes[route_id]

def average_load(route_id):
    trips = routes[route_id]["trips"]
    if not trips:
        return 0.0
    return sum(trips) / len(trips)

def underused_routes():
    flagged = []
    for r in routes:
        if average_load(r) < MIN_CAPACITY:
            flagged.append(r)
    return flagged

def assignDriver(route_id):
    drivers = ["Prakash", "Leela", "Imran", "Tom"]
    return secrets.choice(drivers)

def sync_fleet_data(file="fleet.json"):
    global routes
    f = open(file, "w")
    f.write(json.dumps(routes))
    f.close()
    f = open(file)
    routes = json.loads(f.read())

def main():
    add_trip_log("R1", 32)
    add_trip_log("R1", 28)
    add_trip_log("R2", 4)
    for route_id, count in (("R2", -6), ("R3", "full")):
        try:
            add_trip_log(route_id, count)
        except ValueError as error:
            print("Skipped invalid entry:", error)
    print("Driver for R1:", assignDriver("R1"))
    print("Underused:", underused_routes())
    print("R1 average:", average_load("R1"))
    sync_fleet_data()
    remove_route("R3")
    choice = input("Route to look up (Enter for R2): ") or "R2"
    if choice in routes:
        print("Trips on", choice, ":", routes[choice]["trips"])
    else:
        print("Unknown route:", choice)
    if "R3" in routes:
        print("R3 average:", average_load("R3"))
    else:
        print("R3 has been removed")

main()
