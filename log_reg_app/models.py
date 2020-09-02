from django.db import models
from django.utils.datastructures import MultiValueDictKeyError
from django.core.files.storage import FileSystemStorage
import re
import bcrypt
import datetime
from datetime import date



EMAIL_MATCH = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def get_all_by_email(self):
        return self.order_by('email')

    def register(self, form_data):
        my_hash = bcrypt.hashpw(form_data['password'].encode(), bcrypt.gensalt()).decode()
        return self.create(
            username=form_data['username'],
            first_name=form_data['first_name'],
            last_name=form_data['last_name'],
            password=my_hash,
            email=form_data['email'],
        )

    def authenticate(self, email, password):
        
        users_with_email = self.filter(email=email)
        if not users_with_email:
            return False
        user = users_with_email[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())

    def validate(self, form_data):
        
        errors = {}
        if len(form_data['first_name']) < 1:
            errors['first_name'] = 'First Name field is required.'

        if len(form_data['last_name']) < 1:
            errors['last_name'] = 'Last Name field is required.'

        if len(form_data['email']) < 1:
            errors['email'] = 'Email field is required.'
            
        if len(form_data['username']) < 1:
            errors['username'] = 'username field is required.'
        
        if not EMAIL_MATCH.match(form_data['email']):
            errors['email'] = 'Invalid Email.'
            

        if form_data['password'] != form_data['confirm']:
            errors['password'] = "Passwords do not match"
        
        # prevent duplicate emails!
        users_with_email = self.filter(email=form_data['email'])
        if users_with_email: # if NON-EMPTY list
            errors['email'] = 'Email already in use.'
        
        
        return errors
            
            
        
    # REMEMBER TO ADD ANOTHER PARAMETER FOR THE FILES DIRECTORY WITH POST
    def profile_validator(self, form_data, file_data):
        errors = {}
        if len(form_data['username']) < 1:
            errors['username'] = 'username field is required.'
        
        if len(form_data['first_name']) < 1:
            errors['first_name'] = 'First Name field is required.'

        if len(form_data['last_name']) < 1:
            errors['last_name'] = 'Last Name field is required.'

        if len(form_data['email']) < 1:
            errors['email'] = 'Email field is required.'
            
        if len(form_data['bio']) < 1:
            errors['bio'] = 'Bio field is required.'
        
        # LOOKING FOR KEY VALUE STRING "PICTURE" IN FILE DATA
        # IF THERE IS A PHOTO THEN NO ERROR MESSAGE

        if "picture" in file_data:
            print("there is a photo")
        else:
            errors['picture'] = 'Picture field is required.'
            
        return errors
    
    
    # CHASSIS VALIDATOR 
    def chassis_validator(self, form_data, file_data):
        errors = {}
        if len(form_data['year']) < 1:
            errors['year'] = 'Vehicle must have year.'
        
        if len(form_data['make']) < 1:
            errors['make'] = 'Vehicle make is required.'

        if len(form_data['model']) < 1:
            errors['model'] = 'Vehicle model is required.'

        # LOOKING FOR KEY VALUE STRING "PICTURE" IN FILE DATA
        # IF THERE IS A PHOTO THEN NO ERROR MESSAGE

        if "car_pic" in file_data:
            print("there is a photo")
        else:
            errors['car_pic'] = 'Picture field is required.'
              
        return errors
        
        
       
            
            
        
       
        
        
        
        
        
          
    
    



# MODELS 
class User(models.Model):
    username = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    bio = models.CharField(max_length=255, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    profile_pic = models.CharField(max_length=255, null=True)
    car_pic = models.CharField(max_length=255, null=True)
    year = models.CharField(max_length=255, null=True)
    make = models.CharField(max_length=255, null=True)
    model = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # (posts = from related name on Posts)
    
    objects = UserManager()

    def __str__(self):
        return f"{self.id} {self.first_name} {self.last_name}"
    
    
    