from django.shortcuts import render, redirect , HttpResponse
from log_reg_app.models import *
from Dashboard.models import *
from map_system.models import *
from .models import *
import os
from django.contrib import messages
# THIS IMPORT IS FOR FILE UPLOADS
from django.core.files.storage import FileSystemStorage


# LOADS ABOUT PAGE 
def about(request):
    # if check checks if there is a user logged in, if not it redirects
    if 'user_id' not in request.session:
        return redirect ('/')
    else:
        context = {
            'user': User.objects.get(id=request.session['user_id']),
        }
        return render (request, 'about.html', context)
    
# LOADS ABOUT FEATURED STORY 
def featured_story(request):
    # if check checks if there is a user logged in, if not it redirects
    if 'user_id' not in request.session:
        return redirect ('/')
    else:
        context = {
            'user': User.objects.get(id=request.session['user_id']),
        }
        return render (request, 'featured_story.html', context)

# LOADS MAIN PAGE 
def dashboard(request):
    # if check checks if there is a user logged in, if not it redirects
    if 'user_id' not in request.session:
        return redirect ('/')
    else:
        context = {
            'user': User.objects.get(id=request.session['user_id']),
            'contacts': ContactUser.objects.all(),
        }
        return render (request, 'main_page.html', context)
    
# LOADS RESEARCH PAGE 
def research(request):
    # if check checks if there is a user logged in, if not it redirects
    if 'user_id' not in request.session:
        return redirect ('/')
    else:
        context = {
            'user': User.objects.get(id=request.session['user_id']),
            'toyota_chassis': Chassis.objects.filter(make__contains="toyota"),
            'nissan_chassis': Chassis.objects.filter(make__contains="nissan"),
            'mazda_chassis': Chassis.objects.filter(make__contains="mazda"),
            'honda_chassis': Chassis.objects.filter(make__contains="honda"),
            'mitsubishi_chassis': Chassis.objects.filter(make__contains="mitsubishi"),
            'subaru_chassis': Chassis.objects.filter(make__contains="subaru")
        }
        return render (request, 'research.html', context)
    
# LOADS CHASSIS PAGE 
def chassis_page(request, car_id):
    # if check checks if there is a user logged in, if not it redirects
    if 'user_id' not in request.session:
        return redirect ('/')
    else:
        context = {
            'user': User.objects.get(id=request.session['user_id']),
            "chassis" : Chassis.objects.get(id=car_id),
            'all_chassis': Chassis.objects.all(),
        }
        
        return render (request, 'chassis_page.html', context)

# LOADS MESSAGE BOARD 
def message_board(request):
    # if check checks if there is a user logged in, if not it redirects
    if 'user_id' not in request.session:
        return redirect ('/')
    else:
        
        context = {
            'user': User.objects.get(id=request.session['user_id']),
            'post': Post.objects.order_by('-updated_at'),
            'others': User.objects.all()
        }
        return render (request, 'message_board.html', context)
    
# LOADS MESSAGE PAGE
def message_page(request, id):
    if 'user_id' not in request.session:
        return redirect ('/')
    else:
        current_post = Post.objects.get(id=id)
        liked_by = current_post.user_likes.all()
        context = {
            
            'user': User.objects.get(id=request.session['user_id']),
            'post': Post.objects.order_by('-updated_at'),
            'posts': Post.objects.get(id=id),
            'current_post': Post.objects.get(id=id),
            'liked_by' : liked_by 
        }
        return render (request, 'message_page.html', context)
    
# LOADS PROFILE PAGE    
def user_profile(request, id):
    if 'user_id' not in request.session:
        return redirect ('/')
    else:
        context = {
            'curr_user': User.objects.get(id=request.session['user_id']),
            'user': User.objects.get(id=id),
            'posts': Post.objects.all(),
            'chassis': Chassis.objects.all(),
            "author_id" : id,
            "others" : User.objects.all()
        }
        return render(request, 'profile_page.html', context)
    
# DELETES A POST
def delete(request, post_id):
    # Deleting a post with the information of the current logged in user 
    to_delete = Post.objects.get(id=post_id)
    if to_delete.author_id == request.session['user_id']:
        to_delete.delete()
    return redirect('/vroom/message_board')

# POSTS A MESSAGE 
def post_mess(request):
    Post.objects.create(title=request.POST['title'],content=request.POST['content'], author=User.objects.get(id=request.session['user_id']))
    return redirect('/vroom/message_board')

# COMMENTS ON A POST 
def post_comment(request, id):
    author = User.objects.get(id=request.session['user_id'])
    message = Post.objects.get(id=id)
    Comment.objects.create(comment=request.POST['comment'], author=author, message_post=message)
    return redirect(f'/vroom/message_page/{id}')

# DELETES A COMMENT 
def delete_comment(request, id):
    if "user_id" not in request.session:
        return redirect('/')
    else:
        destroyed = Comment.objects.get(id=id)
        destroyed.delete()
        return redirect('/vroom/message_board')
    
    
# DELETES A CHASSIS 
def delete_chassis(request, car_id):
    if "user_id" not in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        chassis = Chassis.objects.get(id=car_id)
        user.owns.remove(chassis)
        return redirect(f'/vroom/user_profile/{user.id}')

    
# LIKES A POST 
def add_like(request, id):
    liked_message = Post.objects.get(id=id)
    user_liking = User.objects.get(id=request.session['user_id'])
    liked_message.user_likes.add(user_liking)
    return redirect('/vroom/message_board')

# CONTACT FORM INFO FOR ADMIN VIEWING
def contact(request):
    errors = ContactUser.objects.validate(request.POST)
    if errors:
        for field, value in errors.items():
            messages.error(request, value, extra_tags='nope')
        return redirect('/vroom/about')
    else:
        ContactUser.objects.create(name=request.POST['name'], email=request.POST['email'], message=request.POST['message'])
    return redirect('/vroom/about')


# EDITS USER PROFILE 
def edit_profile(request, id):
    # REMEMBER TO ADD ANOTHER PARAMETER FOR THE FILES DIRECTORY WITH POST
    errors = User.objects.profile_validator(request.POST,request.FILES)
    if errors:
        for field, value in errors.items():
            messages.error(request, value, extra_tags='edit_not_approved')
        return redirect(f'/vroom/user_profile/{id}')
    else:
        curr_user = User.objects.get(id=id)
        curr_user.username = request.POST['username']
        curr_user.bio = request.POST['bio']
        curr_user.first_name = request.POST['first_name']
        curr_user.last_name = request.POST['last_name']
        curr_user.email = request.POST['email']
        picture = request.FILES['picture']
        fs = FileSystemStorage()
        user_picture = fs.save(picture.name, picture)
        url = fs.url(user_picture)
        curr_user.profile_pic = url
        curr_user.save()
        print('congrats something worked!')
        messages.success(request, "You have successfully updated!", extra_tags='edit_approved')

        return redirect(f'/vroom/user_profile/{id}')
    
    
   # ADDS A CHASSIS
def edit_chassis(request, id):
    errors = User.objects.chassis_validator(request.POST,request.FILES)
    if errors:
        for field, value in errors.items():
            messages.error(request, value, extra_tags='edit_not_approved')
        return redirect(f'/vroom/user_profile/{id}')
    else:
        curr_user = User.objects.get(id=id)
        curr_user.year = request.POST['year']
        curr_user.make = request.POST['make']
        curr_user.model = request.POST['model']
        car_pic = request.FILES['car_pic']
        fs = FileSystemStorage()
        user_car_pic = fs.save(car_pic.name, car_pic)
        url = fs.url(user_car_pic)
        curr_user.car_pic = url
        curr_user.save()
        print('congrats something worked!')
        messages.success(request, "You have successfully updated!", extra_tags='edit_approved')
        return redirect(f'/vroom/user_profile/{id}')
    
    
    # ADDS CHASSIS TO USER/GARAGE
def add_chassis(request, car_id):
        chassis = Chassis.objects.get(id=car_id)
        user = User.objects.get(id=request.session["user_id"])
        user.owns.add(chassis)
        messages.success(request, "Chassis was added to your garage!", extra_tags='chassis_added')
        
        return redirect(f'/vroom/chassis_page/{car_id}')
    
    
  


