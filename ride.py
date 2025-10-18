import streamlit as st
from datetime import datetime

# RIDE CLASSES
class Ride:
    def __init__(self, ride_id, customer_id, driver_id, distance, fare, start_time=None, end_time=None, start_point="", end_point=""):
        self.ride_id = ride_id
        self.customer_id = customer_id
        self.driver_id = driver_id
        self.distance = distance
        self.fare = fare
        self.start_time = start_time if start_time else datetime.now()
        self.end_time = end_time if end_time else datetime.now()
        self.start_point = start_point
        self.end_point = end_point
    
    def __str__(self):
        return f"Ride ID: {self.ride_id}, Driver: {self.driver_id}, Customer: {self.customer_id}, Distance: {self.distance}km, Fare: {self.fare}"
    
    def to_dict(self):
        return {
            'RideID': self.ride_id,
            'CustomerID': self.customer_id,
            'DriverID': self.driver_id,
            'Distance': self.distance,
            'Fare': self.fare,
            'StartTime': self.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'EndTime': self.end_time.strftime('%Y-%m-%d %H:%M:%S'),
        }

class RideManagementSystem:
    def __init__(self):
        self.rides = []
        self.driver_rides = {}
        self.next_id = 1
    
    def load_from_file(self, filename="rides.csv"):
        """Đọc dữ liệu từ file CSV"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f.readlines()[1:]:
                    parts = [p.strip() for p in line.strip().split(',')]
                    if len(parts) >= 5:
                        ride_id = int(parts[0])
                        customer_id = parts[1]
                        driver_id = int(parts[2])
                        distance = float(parts[3])
                        fare = float(parts[4])
                        
                        start_time = datetime(2024, 10, ride_id % 28 + 1, (ride_id * 2) % 24, (ride_id * 15) % 60)
                        end_time = datetime(2024, 10, ride_id % 28 + 1, ((ride_id * 2) % 24 + 1) % 24, (ride_id * 20) % 60)
                        
                        ride = Ride(ride_id, customer_id, driver_id, distance, fare, start_time, end_time, "Diem A", "Diem B")
                        self.rides.append(ride)
                        
                        if driver_id not in self.driver_rides:
                            self.driver_rides[driver_id] = []
                        self.driver_rides[driver_id].append(ride)
                        
                        self.next_id = max(self.next_id, ride_id + 1)
            # st.success(f"Da tai {len(self.rides)} chuyen di tu file")
        except FileNotFoundError:
            # st.warning(f"Khong tim thay file {filename}. Su dung du lieu mau.")
            self._load_sample_data()
        return self
    
    def _load_sample_data(self):
        """Tải dữ liệu mẫu"""
        sample_rides = [
            Ride(1, "C8", 9, 88.8, 765900, datetime(2024, 10, 1, 8, 30), datetime(2024, 10, 1, 9, 15), "Quan 1", "Quan 5"),
            Ride(2, "C6", 6, 39.9, 342940, datetime(2024, 10, 2, 14, 0), datetime(2024, 10, 2, 15, 10), "Quan 5", "Thu Duc"),
            Ride(3, "C5", 9, 69.7, 523934, datetime(2024, 9, 29, 7, 0), datetime(2024, 9, 29, 7, 45), "Tan Binh", "Quan 3"),
            Ride(4, "C5", 4, 63.0, 460593, datetime(2024, 10, 3, 10, 20), datetime(2024, 10, 3, 11, 30), "Quan 2", "Quan 7"),
            Ride(5, "C6", 2, 30.7, 234885, datetime(2024, 10, 4, 16, 45), datetime(2024, 10, 4, 17, 30), "Quan 3", "Quan 1"),
        ]
        for ride in sample_rides:
            self.rides.append(ride)
            if ride.driver_id not in self.driver_rides:
                self.driver_rides[ride.driver_id] = []
            self.driver_rides[ride.driver_id].append(ride)
            self.next_id = max(self.next_id, ride.ride_id + 1)
    
    def save_to_file(self, filename="rides.csv"):
        """Lưu dữ liệu vào file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("RideID,CustomerID,DriverID,Distance(km),Fare(VND)\n")
                for r in self.rides:
                    f.write(f"{r.ride_id},{r.customer_id},{r.driver_id},{r.distance},{r.fare}\n")
            st.success(f"Da luu {len(self.rides)} chuyen di vao file")
        except Exception as e:
            st.error(f"Loi khi luu file: {e}")
    
    def get_driver_trips(self, driver_id, ascending=True):
        """Lấy danh sách chuyến đi của tài xế - O(1) lookup + O(n log n) sort"""
        if driver_id not in self.driver_rides:
            return []
        trips = self.driver_rides[driver_id].copy()
        trips.sort(key=lambda x: x.start_time, reverse=not ascending)
        return [t.to_dict() for t in trips]
    
    def filter_trips_by_time(self, driver_id, start_date, end_date):
        """Lọc chuyến đi theo khoảng thời gian"""
        if driver_id not in self.driver_rides:
            return []
        
        trips = self.driver_rides[driver_id]
        filtered = []
        
        for trip in trips:
            if start_date <= trip.start_time <= end_date:
                filtered.append(trip)
        
        filtered.sort(key=lambda x: x.start_time)
        return [t.to_dict() for t in filtered]
    
    def get_recent_trips(self, driver_id, limit=10):
        """Lấy n chuyến đi gần nhất"""
        if driver_id not in self.driver_rides:
            return []
        trips = self.driver_rides[driver_id].copy()
        trips.sort(key=lambda x: x.start_time, reverse=True)
        return [t.to_dict() for t in trips[:limit]]
    
    def get_all_rides(self):
        """Lấy tất cả chuyến đi"""
        return [r.to_dict() for r in self.rides]
