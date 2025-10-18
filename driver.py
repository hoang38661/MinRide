import streamlit as st
from data import *

# CLASSES 
class Driver:
    def __init__(self, id, name, rating, x, y, trips=0, experience=0):
        self.id = id
        self.name = name
        self.rating = rating
        self.x = x
        self.y = y
        self.trips = trips
        self.experience = experience
    
    def __str__(self):
        return f"ID: {self.id}, Ten: {self.name}, Rating: {self.rating}, Toa do: ({self.x}, {self.y})"
    
    def to_dict(self):
        return {
            'ID': self.id,
            'Ten': self.name,
            'Rating': self.rating,
            'X': self.x,
            'Y': self.y,
        }
    
class DriverManagementSystem:
    def __init__(self):
        self.drivers = []    
        self.id_index = {}      
        self.next_id = 1
    
    def load_from_file(self, filename="drivers.csv"):
        """Đọc dữ liệu từ file CSV"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f.readlines()[1:]:
                    parts = [p.strip() for p in line.strip().split(',')]
                    if len(parts) >= 5:
                        driver = Driver(
                            int(parts[0]), 
                            parts[1], 
                            float(parts[2]), 
                            float(parts[3]), 
                            float(parts[4]),
                            int(parts[5]) if len(parts) > 5 else 0,
                            int(parts[6]) if len(parts) > 6 else 0
                        )
                        self.drivers.append(driver)
                        self.id_index[driver.id] = driver
                        self.next_id = max(self.next_id, driver.id + 1)
            # st.success(f"Da tai {len(self.drivers)} tai xe tu file")
        except FileNotFoundError:
            # st.warning(f"Khong tim thay file {filename}. Su dung du lieu mau.")
            self._load_sample_data()
        return self
    
    def _load_sample_data(self):
        """Tải dữ liệu mẫu nếu không có file"""
        sample_drivers = [
            Driver(1, "Nguyen Van A", 4.5, 10.8231, 106.6297, 120, 5),
            Driver(2, "Tran Van B", 4.8, 10.7769, 106.7009, 85, 3),
            Driver(3, "Le Van C", 4.2, 10.8050, 106.6500, 200, 7)
        ]
        for driver in sample_drivers:
            self.drivers.append(driver)
            self.id_index[driver.id] = driver
            self.next_id = max(self.next_id, driver.id + 1)
    
    def save_to_file(self, filename="drivers.csv"):
        """Lưu dữ liệu vào file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("ID,Name,Rating,X,Y,Trips,Experience\n")
                for d in self.drivers:
                    f.write(f"{d.id},{d.name},{d.rating},{d.x},{d.y},{d.trips},{d.experience}\n")
            st.success(f"Da luu {len(self.drivers)} tai xe vao file")
        except Exception as e:
            st.error(f"Loi khi luu file: {e}")
    
    def get_all_drivers(self):
        """Lấy danh sách tất cả tài xế"""
        return [d.to_dict() for d in self.drivers]
    
    def display_all(self):
        """Hiển thị toàn bộ danh sách"""
        if not self.drivers:
            st.info("Danh sach trong!")
            return
        return self.get_all_drivers()
    
    def display_top_k(self, k, from_top=True):
        """Hiển thị top k tài xế"""
        if not self.drivers:
            return []
        k = min(k, len(self.drivers))
        show = self.drivers[:k] if from_top else self.drivers[-k:]
        return [d.to_dict() for d in show]
    
    def add_driver(self, name, rating, x, y, trips=0, experience=0):
        """Thêm tài xế mới - O(1)"""
        driver = Driver(self.next_id, name, rating, x, y, trips, experience)
        self.drivers.append(driver)
        self.id_index[driver.id] = driver
        self.next_id += 1
        return driver
    
    def search_driver(self, keyword):
        """Tìm kiếm theo ID (O(1)) hoặc tên (O(n))"""
        try:
            id_val = int(keyword)
            if id_val in self.id_index:
                return [self.id_index[id_val].to_dict()]
        except ValueError:
            pass
        
        results = [d.to_dict() for d in self.drivers if keyword.lower() in d.name.lower()]
        return results
    
    def update_driver(self, id, new_name=None, new_rating=None, new_x=None, new_y=None, new_trips=None, new_experience=None):
        """Cập nhật thông tin tài xế - O(1) tìm, O(1) cập nhật"""
        if id not in self.id_index:
            return False
        
        driver = self.id_index[id]
        if new_name: driver.name = new_name
        if new_rating is not None: driver.rating = new_rating
        if new_x is not None: driver.x = new_x
        if new_y is not None: driver.y = new_y
        if new_trips is not None: driver.trips = new_trips
        if new_experience is not None: driver.experience = new_experience
        return True
    
    def delete_driver(self, id):
        """Xóa tài xế - O(1) tìm, O(n) xóa khỏi list"""
        if id not in self.id_index:
            return False
        
        driver = self.id_index[id]
        self.drivers.remove(driver)
        del self.id_index[id]
        return True
    
    def quick_sort(self, arr, ascending=False):
        """Quick Sort theo rating - O(n log n)"""
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2]
        if ascending:
            left = [x for x in arr if x.rating < pivot.rating]
            middle = [x for x in arr if x.rating == pivot.rating]
            right = [x for x in arr if x.rating > pivot.rating]
        else:
            left = [x for x in arr if x.rating > pivot.rating]
            middle = [x for x in arr if x.rating == pivot.rating]
            right = [x for x in arr if x.rating < pivot.rating]
        return self.quick_sort(left, ascending) + middle + self.quick_sort(right, ascending)
    
    def sort_by_rating(self, ascending=False):
        """Sắp xếp theo rating"""
        if not self.drivers:
            return
        self.drivers = self.quick_sort(self.drivers, ascending)
