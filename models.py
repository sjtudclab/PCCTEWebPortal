
# __author__ = 'Eugene'


class Entity(object):
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, kwargs[key])


class User(object):
    def __init__(self, user_id, username, password, user_type, icon='/files/default_user.png', name='default', email='null',
                 identity_number='null', card_id='null'):
        super().__init__()
        self.user_id = user_id
        self.username = username
        self.password = password
        self.user_type = user_type
        self.icon = icon
        self.name = name
        self.email = email
        self.identity_number = identity_number
        self.card_id = card_id

class Personnel(object):
    def __init__(self, user_id, name, position, job_detail, role, block_number, address_detail):
        super().__init__()
        self.user_id = user_id
        self.name = name
        self.position = position
        self.job_detail = job_detail
        self.role = role
        self.block_number = block_number
        self.address_detail = address_detail

class Apartment(object):
    def __init__(self, building_id, building_name, building_description, apartment_id, apartment_name, area, owner, serial_number):
        super().__init__()
        self.building_id = building_id
        self.building_name = building_name
        self.building_description = building_description
        self.apartment_id = apartment_id
        self.apartment_name = apartment_name
        self.area = area
        self.owner = owner
        self.serial_number = serial_number


class User_Role(object):
    def __init__(self, user_role_id, user_id, role_id, role_type_id, role_description, user_role_description, description_detail):
        super().__init__()
        self.user_role_id = user_role_id
        self.user_id = user_id
        self.role_id = role_id
        self.role_type_id = role_type_id
        self.role_description = role_description
        self.user_role_description = user_role_description
        self.description_detail = description_detail

class User_Living_Info(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class User_Resident_Info(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class User_Net_Info(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class User_Party_Info(Entity):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

