from django.shortcuts import render,redirect
from . models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render(request ,"index.html")

def registration(request):
    errors = User.objects.basic_validator(request.POST)
        # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')
    else:
        fname=request.POST['first_name']
        lname=request.POST['last_name']
        email=request.POST['email']
        password=request.POST['password']
        hashed=bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        User.objects.create(first_name=fname,last_name=lname,email=email,password=hashed)
        user=User.objects.last()
        request.session['user_id']=user.id
    return redirect('/wall')

def wall(request):
    if 'user_id' not in request.session:
        redirect('/')
    context={
        'user':User.objects.get(id=request.session['user_id']),
        'allmessages':Message.objects.all().order_by("-created_at")
    }
    return render(request,"wall.html",context)

def login(request):
    email=request.POST['email']
    password=request.POST['password']
    user=User.objects.filter(email=email).first()
    if user:
        if bcrypt.checkpw(password.encode(), user.password.encode()):
            request.session['user_id']=user.id
            return redirect('/wall')
    messages.error(request, 'Invalid Credentials')
    return redirect('/')

def logout(request):
    return redirect('/')

def create_message(request):
    message=request.POST['message']
    user_id=int(request.POST['user_id'])
    user=User.objects.get(id=user_id)
    Message.objects.create(message=message,user=user)
    return redirect('/wall')

def delete_message(request):  
    message = Message.objects.get(id=request.POST['message_id'])
    message.delete()
    return redirect('/wall')

def delete_comment(request):
    comment_id=request.POST['comment_id']
    comment=Comment.objects.get(id=comment_id)
    comment.delete()
    return redirect('/wall')  

def create_comment(request):
    comment=request.POST['comment']
    user=User.objects.get(id=request.POST['user_id'])
    message=Message.objects.get(id=request.POST['message_id'])
    Comment.objects.create(comment=comment,user=user,message=message)
    return redirect('/wall')



# Create your views here.

# Create your views here.
