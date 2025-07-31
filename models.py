from flask_login import UserMixin


# User Roles
ROLES = ["staff", "admin", "director", "cdsa", "superadmin"]

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['_id'])
        self.first_name = user_data['first_name']
        self.last_name = user_data['last_name']
        self.directorate = user_data['directorate']
        self.password = user_data['password']
        self.email = user_data['email']
        self.role = user_data['role']

    def get_id(self):
        return self.id

    def is_admin(self):
        return self.role in ["staff", "admin", "director", "cdsa", "superadmin"]
    
    def is_superadmin(self):
        return self.role in ['cdsa', 'superadmin']
    

class Swipe():
    def __init__(self, swipe_data):
        self.id = str(swipe_data['_id'])
        self.card_id = swipe_data['card_id']
        self.staff_id = swipe_data['staff_id']
        self.time = swipe_data['time']
        

class Card_db():
    def __init__(self,card_data):
        self.id = str(card_data['_id'])
        self.card_id = card_data['card_id']
        self.first_name = card_data['first_name']
        self.last_name = card_data['last_name']
        self.directorate = card_data['directorate']
        self.staff_id = card_data['staff_id']

        