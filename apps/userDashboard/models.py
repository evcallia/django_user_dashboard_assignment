from __future__ import unicode_literals

from django.db import models
import re
from django.contrib import messages
import bcrypt
# Create your models here.
class userManager(models.Manager):
    # return true if appropriate fields are valid duting registration process
    def validateRegistration(self, request):
        if self.validateEmail(request) and self.validateName(request) and self.validatePassword(request):
            if len(User.objects.all()) < 1:
                #user must be admin
                User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()), user_level=9)
            else:
                User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()), user_level=1)
            if 'add_user' in request.POST: #user is being created by admin and shouldn't be logged in
                return True
            else: #this will log them in once their information has been checked
                return self.validateLogin(request)
        else:
            return False

    # return true if email is valid and not in use
    def validateEmail(self, request, *args):
        email = request.POST['email']
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+.[a-zA-Z]*$')
        if not EMAIL_REGEX.match(email):
            messages.error(request, "Email is not valid")
            return False
        else:
            # check if email is already in database
            try:
                user = User.objects.get(email=email)
                if 'edit_type' in request.POST and int(user.id) == int(args[0]):
                    return True #it's ok that the email matches, it's theirs
                else:
                    messages.error(request, "Email is already in use")
                    return False
            except User.DoesNotExist:
                pass
        return True

    def validateName(self, request):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        no_error = True
        if len(first_name) < 2 or any(char.isdigit() for char in first_name):
            messages.error(request, 'Frist name must be 2 characters and only letters')
            no_error = False
        if len(last_name) < 2 or any(char.isdigit() for char in last_name):
            messages.error(request, 'Last name must be 2 characters and only letters')
            no_error = False
        return no_error

    def validatePassword(self, request):
        password = request.POST['password']
        confirm_password = request.POST['password_confirmation']
        no_error = True
        if len(password) < 8:
            messages.error(request, 'Password must be greater than 8 characters')
            no_error = False
        if not password == confirm_password:
            messages.error(request, 'Password confirmation must match password')
            no_error = False
        return no_error

    def validateLogin(self, request):
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.get(email=email)
            if bcrypt.hashpw(password.encode(), user.password.encode()) == user.password:
                request.session['id'] = user.id
                return True
        except User.DoesNotExist:
            messages.error(request, "Invalid email")
            return False

    def update(self, request, id):
        user = User.objects.get(id=id)
        if request.POST['edit_type'] == 'info':
            if self.validateName(request) and self.validateEmail(request, id):
                user.first_name = request.POST['first_name']
                user.last_name = request.POST['last_name']
                user.email = request.POST['email']
                if 'user_level' in request.POST:
                    user.user_level = request.POST['user_level']
            else:
                return False
        elif request.POST['edit_type'] == 'password' :
            if self.validatePassword(request):
                user.password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            else:
                return False
        else:
            print user.description
            user.description = request.POST['description']
            print user.description
        user.save()
        return True





class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    user_level = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = userManager()

class Message(models.Model):
    message = models.CharField(max_length=255)
    messager_id = models.ForeignKey(User)
    post_to_id = models.ForeignKey(User, related_name='post_to')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    comment = models.CharField(max_length=255)
    message_id = models.ForeignKey(Message)
    commenter_id = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#models.TextField()
#user_id = models.ForeignKey(User)












#
