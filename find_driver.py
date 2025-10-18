import streamlit as st
import math

# FIND DRIVER SYSTEM  
class FindDriverSystem:
    def __init__(self, driver_manager, customer_manager):
        self.driver_manager = driver_manager
        self.customer_manager = customer_manager
    
    def calculate_distance(self, x1, y1, x2, y2):
        """Tính khoảng cách Euclidean"""
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    def find_drivers_within_radius(self, customer_id, radius, sort_priority=None, 
                                   top_k=None, min_rating=None, min_trips=None, min_experience=None):
        """
        Tìm tài xế trong bán kính
        
        sort_priority: list các tiêu chí ['distance', '-rating', 'trips', '-experience']
                      Dấu '-' nghĩa là giảm dần
        """
        # Kiểm tra khách hàng
        if customer_id not in self.customer_manager.customers:
            return [], f"Khach hang ID {customer_id} khong ton tai"
        
        customer = self.customer_manager.customers[customer_id]
        cust_x, cust_y = customer.x, customer.y
        
        # Tìm tài xế trong bán kính
        candidates = []
        for driver in self.driver_manager.drivers:
            distance = self.calculate_distance(cust_x, cust_y, driver.x, driver.y)
            
            if distance <= radius:
                # Áp dụng bộ lọc
                if min_rating and driver.rating < min_rating:
                    continue
                if min_trips and driver.trips < min_trips:
                    continue
                if min_experience and driver.experience < min_experience:
                    continue
                
                candidates.append({
                    'driver': driver,
                    'distance': distance
                })
        
        if not candidates:
            return [], None
        
        # Sắp xếp theo priority
        if sort_priority:
            def get_sort_key(item):
                keys = []
                for criterion in sort_priority:
                    reverse = criterion.startswith('-')
                    field = criterion.lstrip('-')
                    
                    if field == 'distance':
                        value = item['distance']
                    elif field == 'rating':
                        value = item['driver'].rating
                    elif field == 'trips':
                        value = item['driver'].trips
                    elif field == 'experience':
                        value = item['driver'].experience
                    else:
                        value = 0
                    
                    keys.append(-value if reverse else value)
                return tuple(keys)
            
            candidates.sort(key=get_sort_key)
        
        # Top K
        if top_k:
            candidates = candidates[:top_k]
        
        # Chuyển đổi kết quả
        results = []
        for item in candidates:
            driver = item['driver']
            result = driver.to_dict()
            result['Distance'] = item['distance']
            results.append(result)
        
        return results, None
