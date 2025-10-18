from datetime import datetime

class Action:
    def __init__(self, type, entity, data):
        self.type, self.entity, self.data = type, entity, data
        self.time = datetime.now()
        
    def to_dict(self):
        return {"type": self.type, "entity": self.entity, "time": self.time.strftime("%H:%M:%S"), "data": str(self.data)}

class UndoStack:
    def __init__(self, limit=10): self.stack, self.limit = [], limit

    def push(self, action): 
        self.stack.append(action)
        if len(self.stack) > self.limit: self.stack.pop(0)

    def pop(self): 
        return self.stack.pop() if self.stack else None
    
    def clear(self): 
        self.stack.clear()

    def history(self): 
        return [a.to_dict() for a in reversed(self.stack)]
