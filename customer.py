import streamlit as st

# CUSTOMER CLASSES 
class Customer:
    def __init__(self, cid, name, location, x, y):
        self.id = cid
        self.name = name
        self.location = location
        self.x = x
        self.y = y
    
    def __str__(self):
        return f"ID: {self.id}, Ten: {self.name}, Quan: {self.location}, Toa do: ({self.x}, {self.y})"
    
    def to_dict(self):
        return {
            'ID': self.id,
            'Ten': self.name,
            'Quan': self.location,
            'X': self.x,
            'Y': self.y
        }

class CustomerManagementSystem:
    def __init__(self):
        self.customers = {}
        self.next_id = 1
    
    def load_from_file(self, filename="customers.csv"):
        """Đọc dữ liệu từ file CSV"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f.readlines()[1:]:
                    parts = [p.strip() for p in line.strip().split(',')]
                    if len(parts) >= 5:
                        customer = Customer(int(parts[0]), parts[1], parts[2], float(parts[3]), float(parts[4]))
                        self.customers[customer.id] = customer
                        self.next_id = max(self.next_id, customer.id + 1)
            # st.success(f"Da tai {len(self.customers)} khach hang tu file")
        except FileNotFoundError:
            # st.warning(f"Khong tim thay file {filename}. Su dung du lieu mau.")
            self._load_sample_data()
        return self
    
    def _load_sample_data(self):
        """Tải dữ liệu mẫu nếu không có file"""
        sample_customers = [
            Customer(1, "Nguyen Thi Hoa", "Quan 1", 10.7756, 106.7019),
            Customer(2, "Tran Van Minh", "Quan 3", 10.7889, 106.7050),
            Customer(3, "Le Thi Lan", "Quan 1", 10.7650, 106.6950),
            Customer(4, "Pham Van Nam", "Quan 2", 10.7800, 106.7100),
            Customer(5, "Vo Thi Mai", "Quan 1", 10.7700, 106.7000)
        ]
        for customer in sample_customers:
            self.customers[customer.id] = customer
            self.next_id = max(self.next_id, customer.id + 1)
    
    def save_to_file(self, filename="customers.csv"):
        """Lưu dữ liệu vào file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("ID,Name,Location,X,Y\n")
                for c in self.customers.values():
                    f.write(f"{c.id},{c.name},{c.location},{c.x},{c.y}\n")
            st.success(f"Da luu {len(self.customers)} khach hang vao file")
        except Exception as e:
            st.error(f"Loi khi luu file: {e}")
    
    def add_customer(self, name, location, x, y):
        """Thêm khách hàng mới - O(1)"""
        if not name or not location:
            return None
        customer = Customer(self.next_id, name, location, x, y)
        self.customers[customer.id] = customer
        self.next_id += 1
        return customer
    
    def update_customer(self, cid, name=None, location=None, x=None, y=None):
        """Cập nhật thông tin khách hàng - O(1)"""
        if cid not in self.customers:
            return False
        c = self.customers[cid]
        if name: c.name = name
        if location: c.location = location
        if x is not None: c.x = x
        if y is not None: c.y = y
        return True
    
    def delete_customer(self, cid):
        """Xóa khách hàng - O(1)"""
        if cid in self.customers:
            del self.customers[cid]
            return True
        return False
    
    def search_by_id(self, cid):
        """Tìm khách hàng theo ID - O(1)"""
        return self.customers.get(cid, None)
    
    def search_by_name(self, name):
        """Tìm khách hàng theo tên - O(n)"""
        results = []
        for c in self.customers.values():
            if name.lower() in c.name.lower():
                results.append(c)
        return results
    
    def search_customer(self, keyword):
        """Tìm kiếm theo ID hoặc tên"""
        try:
            cid = int(keyword)
            customer = self.search_by_id(cid)
            return [customer.to_dict()] if customer else []
        except ValueError:
            results = self.search_by_name(keyword)
            return [c.to_dict() for c in results]
    
    def top_k_customers(self, k, from_top=True):
        """Hiển thị top k khách hàng theo ID"""
        if not self.customers:
            return []
        sorted_customers = sorted(self.customers.values(), key=lambda c: c.id)
        if from_top:
            return [c.to_dict() for c in sorted_customers[:k]]
        else:
            return [c.to_dict() for c in sorted_customers[-k:]]
    
    def list_by_location(self, location, limit=10):
        """Liệt kê khách hàng theo quận"""
        filtered = [c for c in self.customers.values() if location.lower() in c.location.lower()]
        filtered.sort(key=lambda c: c.id)
        if limit:
            return [c.to_dict() for c in filtered[:limit]], len(filtered)
        return [c.to_dict() for c in filtered], len(filtered)
    
    def get_all_customers(self):
        """Lấy danh sách tất cả khách hàng"""
        return [c.to_dict() for c in self.customers.values()]
