"""Campus shuttle timetable and fleet tracker."""
import json
import secrets
from datetime import datetime

# Global state
routes = {"R1": {"name": "Main Gate - Library", "trips": []},
          "R2": {"name": "Hostel - Sports Complex", "trips": []},
          "R3": {"name": "Admin Block - Metro", "trips": []}}
MIN_CAPACITY = 10
DRIVERS = ["Prakash", "Leela", "Imran", "Tom"]

def add_trip_log(route_id, passenger_count, logs=None):
    """Record a trip's passenger count and return the log list."""
    if not isinstance(passenger_count, int) or passenger_count < 0:
        raise ValueError(f"passenger_count must be a non-negative integer, got {passenger_count!r}")
    if logs is None:
        logs = []
    routes[route_id]["trips"].append(passenger_count)
    logs.append(f"{datetime.now()}: {route_id} carried {passenger_count}")
    return logs

def remove_route(route_id):
    """Delete a route from the fleet."""
    del routes[route_id]

def average_load(route_id):
    """Return the average passengers per trip (0.0 if no trips yet)."""
    trips = routes[route_id]["trips"]
    if not trips:
        return 0.0
    return sum(trips) / len(trips)

def underused_routes():
    """Return the ids of routes whose average load is below MIN_CAPACITY."""
    return [r for r in routes if average_load(r) < MIN_CAPACITY]

def assign_driver(route_id):
    """Pick a driver for an existing route."""
    if route_id not in routes:
        raise KeyError(route_id)
    return secrets.choice(DRIVERS)

def sync_fleet_data(file="fleet.json"):
    """Save routes to a JSON file, then reload them from it."""
    with open(file, "w", encoding="utf-8") as handle:
        json.dump(routes, handle)
    with open(file, encoding="utf-8") as handle:
        loaded = json.load(handle)
    routes.clear()
    routes.update(loaded)

def main():
    """Run the demo scenario."""
    add_trip_log("R1", 32)
    add_trip_log("R1", 28)
    add_trip_log("R2", 4)
    for route_id, count in (("R2", -6), ("R3", "full")):
        try:
            add_trip_log(route_id, count)
        except ValueError as error:
            print("Skipped invalid entry:", error)
    print("Driver for R1:", assign_driver("R1"))
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

if __name__ == "__main__":
    main()
