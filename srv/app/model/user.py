
from app import app, andromeda_core
from flask import session
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, first_name, second_name, phone):
        self.id = id
        self.first_name = first_name
        self.second_name = second_name
        self.phone = phone
        #self._is_authenticated = False
        #self._is_active = True
        #self._is_anoymous = False

    #@property
    #def is_authenticated(self):
    #    return self._is_authenticated

    #@is_authenticated.setter
    #def is_authenticated(self, val):
    #    self._is_authenticated = val

    #@property
    #def is_active(self):
    #    return self._is_active

    #@is_active.setter
    #def is_active(self, val):
    #    self._is_active = val

    #@property
    #def is_anoymous(self):
    #    return self._is_anoymous

    #@is_anoymous.setter
    #def is_anoymous(self, val):
    #    self._is_anoymous = val

    def dict(self):
        return {"id": self.id,
                "first_name_wide_ch" : self.first_name,
                "second_name_wide_ch" : self.second_name,
                "phone" : self.phone  
                }

#session['session_user'] = None

#g_user = None
