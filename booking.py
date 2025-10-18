import math
from datetime import datetime, timedelta
from ride import Ride

class BookingSystem:
    FARE_RATE = 12000  # 12.000 VND/km

    def __init__(self, driver_manager, customer_manager, ride_manager):
        self.driver_manager = driver_manager
        self.customer_manager = customer_manager
        self.ride_manager = ride_manager
        self.bookings = []  # Danh sách tất cả chuyến

    def get_location(self, obj_manager, obj_id):
        if obj_manager and obj_id in getattr(obj_manager, "id_index", {}):
            obj = obj_manager.id_index[obj_id]
        elif obj_manager and obj_id in getattr(obj_manager, "customers", {}):
            obj = obj_manager.customers[obj_id]
        else:
            return None, None, None
        return obj.x, obj.y, obj.name

    def distance(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def create_booking(self, customer_id, driver_id, trip_distance):
        cx, cy, cname = self.get_location(self.customer_manager, customer_id)
        dx, dy, dname = self.get_location(self.driver_manager, driver_id)
        if cx is None or dx is None:
            return None, "ID không tồn tại."

        pickup = self.distance(dx, dy, cx, cy)
        total = pickup + trip_distance
        fare = total * self.FARE_RATE

        booking = {
            "booking_id": len(self.bookings) + 1,
            "customer_name": cname,
            "driver_name": dname,
            "total_distance": total,
            "fare": fare,
            "status": "Pending",
            "created_at": datetime.now(),
        }
        self.bookings.append(booking)
        return booking, None

    def confirm_all(self):
        count = 0
        for b in self.bookings:
            if b["status"] == "Pending":
                ride = Ride(
                    ride_id=self.ride_manager.next_id,
                    customer_id=b["booking_id"],
                    driver_id=b["booking_id"],
                    distance=b["total_distance"],
                    fare=b["fare"],
                    start_time=b["created_at"],
                    end_time=b["created_at"] + timedelta(minutes=60),
                    start_point="Start",
                    end_point="End"
                )
                self.ride_manager.rides.append(ride)
                self.ride_manager.next_id += 1
                b["status"] = "Confirmed"
                count += 1
        return count

    def cancel_all(self):
        count = 0
        for b in self.bookings:
            if b["status"] == "Pending":
                b["status"] = "Canceled"
                count += 1
        return count

    def get_pending(self):
        return [b for b in self.bookings if b["status"] == "Pending"]

    def get_all(self):
        return self.bookings
