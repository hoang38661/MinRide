import math
from datetime import datetime

class AutoMatchingSystem:
    def __init__(self, driver_manager, customer_manager, booking_system):
        self.driver_manager = driver_manager
        self.customer_manager = customer_manager
        self.booking_system = booking_system
        self.requests = []
        self.next_id = 1
        self.busy = set()

    def distance(self, a, b): return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

    def create_request(self, customer_id, trip_distance):
        if customer_id not in self.customer_manager.customers:
            return None, "Khách hàng không tồn tại"
        c = self.customer_manager.customers[customer_id]
        req = {
            "id": self.next_id,
            "customer_id": customer_id,
            "location": (c.x, c.y),
            "trip_distance": trip_distance,
            "state": "waiting",
            "driver": None,
            "created": datetime.now()
        }
        self.requests.append(req)
        self.next_id += 1
        return req, None

    def find_best_driver(self, location):
        available = [d for d in self.driver_manager.drivers if d.id not in self.busy]
        if not available: return None, "Không có tài xế rảnh"
        best = min(available, key=lambda d: self.distance((d.x, d.y), location))
        return best, None

    def auto_match_all(self):
        matched = []
        for r in [r for r in self.requests if r["state"] == "waiting"]:
            d, err = self.find_best_driver(r["location"])
            if not d: 
                r["state"] = "failed"
                continue
            r["state"] = "matched"
            r["driver"] = d
            self.busy.add(d.id)
            booking, _ = self.booking_system.create_booking(r["customer_id"], d.id, r["trip_distance"])
            matched.append({"request_id": r["id"], "customer_id": r["customer_id"], "driver_id": d.id, "fare": booking["fare"]})
        return matched

    def get_all(self): 
        return self.requests
