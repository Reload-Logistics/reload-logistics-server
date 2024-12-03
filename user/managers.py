from multiprocessing.sharedctypes import Value
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _



# Create User Manager
class UserManager(BaseUserManager):
    
    user_in_migrations = True

    # create user function 
    def create_user(self, email, user_first_name, 
                        user_surname, user_contact_number, 
                            password, **other_fields):
        
        # verify email 
        if not email: 
            raise TypeError(_('Please provide a valid email address'))
        

        # save 
        email = self.normalize_email(str(email).lower())
        user = self.model(email = str(email).lower(),
                         user_first_name = str(user_first_name).capitalize(),
                         user_surname = str(user_surname).capitalize(),
                         user_contact_number = str(user_contact_number),
                         **other_fields)
        
        # set user password 
        user.set_password(password)
        user.save(using = self._db)

        # return account 
        return user 
    
    # create super user 
    def create_superuser(self, email, user_first_name, 
                                user_surname, user_contact_number, 
                                    password, **other_fields):
        

        #default setting  
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_verified', True)
        
        # verify
        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to staff = true')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to superuser = true')
        if other_fields.get('is_active') is not True:
            raise ValueError('active must be assigned to active = true')
        if other_fields.get('is_verified') is not True:
            raise ValueError('Superuser must be set to verified')
        
        
        # create user 
        user  = self.create_user(email, user_first_name, 
                                    user_surname, user_contact_number, 
                                        password, **other_fields)
        
        # super 
        return user 
        
