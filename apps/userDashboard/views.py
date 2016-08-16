from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import User, Message, Comment
#CONTROLLER
#Create your views here.
def index(request): #:index
    return render(request, 'userDashboard/index.html')

def login(request): #:login
    if 'id' in request.session:
        return redirect(reverse('dashboard:dashboard'))
    return render(request, 'userDashboard/login.html')

def process_login(request): #:proc_login
    if User.objects.validateLogin(request):
        print 'should route to dashboard'
        return redirect(reverse('dashboard:dashboard'))
    else:
        return redirect(reverse('dashboard:login'))

def register(request): #:register
    if 'id' in request.session:
        return redirect(reverse('dashboard:dashboard'))
    return render(request, 'userDashboard/register.html')

def create(request): #:create
    if User.objects.validateRegistration(request):
        return redirect(reverse('dashboard:dashboard'))
    elif 'add_user' in request.POST:
        return redirect(reverse('dashboard:new'))
    else:
        return redirect(reverse('dashboard:register'))

def dashboard(request): #:dashboard
    if 'id' in request.session:
        context = {
        'user_level': User.objects.get(id=request.session["id"]).user_level,
        'users': User.objects.all()
        }
        return render(request, 'userDashboard/dashboard.html', context)
    else:
        return redirect(reverse('dashboard:login'))

def new(request): #:new
    if 'id' in request.session and User.objects.get(id=request.session["id"]).user_level == 9:
        return render(request, 'userDashboard/newuser.html')
    else:
        return redirect(reverse('dashboard:login'))

def show(request, id): #:show
    if 'id' in request.session:
        return render(request, "userDashboard/show.html", {'user': User.objects.get(id=id), 'messages': Message.objects.all(), 'comments': Comment.objects.all()})
    else:
        return redirect(reverse('dashboard:login'))

def edit(request, id): #:edit
    if 'id' in request.session and request.session['id'] == int(id) or 'id' in request.session and User.objects.get(id=request.session["id"]).user_level == 9:
        return render(request, "userDashboard/edit.html", {'user': User.objects.get(id=id), 'user_level': User.objects.get(id=request.session["id"]).user_level})
    else:
        return redirect(reverse('dashboard:login'))

def update(request, id): #:update
    if 'id' in request.session and request.session['id'] == int(id) or 'id' in request.session and User.objects.get(id=request.session["id"]).user_level == 9:
        if User.objects.update(request, id):
            messages.success(request, 'Information has been updated successcully')
        return redirect(reverse('dashboard:edit', kwargs={'id':id}))
    else:
        return redirect(reverse('dashboard:login'))

def remove(request, id): #:remove
    if 'id' in request.session and request.session['id'] == int(id) or 'id' in request.session and User.objects.get(id=request.session["id"]).user_level == 9:
        User.objects.get(id = id).delete()
    return redirect(reverse('dashboard:dashboard'))

def log_off(request): #:log-off
    if 'id' in request.session:
        del request.session['id']
        return redirect(reverse('dashboard:index'))
    return redirect(reverse('dashboard:login'))

def message(request, post_to_id): #:message
    Message.objects.create(message=request.POST['message'], messager_id=User.objects.get(id=request.session['id']), post_to_id=User.objects.get(id=post_to_id))
    return redirect(reverse('dashboard:show', kwargs={'id': post_to_id}))

def comment(request, message_id, post_to_id): #:comment
    Comment.objects.create(comment=request.POST['comment'], message_id=Message.objects.get(id=message_id), commenter_id=User.objects.get(id=request.session['id']))
    return redirect(reverse('dashboard:show', kwargs={'id': post_to_id}))











#
