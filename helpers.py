class Get_post():
    def __init__(self, id):
        self.id = id
        
    def __str__(self) -> str:
        pass
    
    def get_first_part(self):
        data = str(self.id).split("-")[1]
        result = data[-3:]
        return result
    
    def get_from_id(self):
        data1 = str(self.id).split("-")
        result = ''.join([data2[-3:] for data2 in data1])
        return result
    

# def ddd():
#     data1 = str(self.id).split("-")
#     result = ''.join([data2[-3:] for data2 in data1])
#     return result