from django.http import HttpResponse
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.http import JsonResponse
import datetime as D
from collections import Counter
from django.core import serializers
import string
import random

def memberloggedin(view):
    def mod_view(request):
        if 'username' in request.session:
            username = request.session['username']
            try: user = Member.objects.get(username=username)
            except Member.DoesNotExist: raise Http404('Member does not exist')
            return view(request, user)
        else:
            return render(request,'matchingSite/not_logged_in.html',{})
    return mod_view

def index(request):
    return render(request,'matchingSite/index.html')

def register(request):
    return render(request, 'matchingSite/register.html')

@csrf_exempt
def registerinfo(request):
    if 'username' in request.POST and 'pass' in request.POST and 'gender' in request.POST and 'dob' in request.POST and 'firstname' in request.POST and 'secondname' in request.POST and 'email' in request.POST and 'hobbies' in request.POST :
        u = request.POST['username']
        p = request.POST['pass']
        g = request.POST['gender']
        d = request.POST['dob']
        f = request.POST['firstname']
        l = request.POST['secondname']
        e = request.POST['email']
        h = request.POST.getlist('hobbies')

        user = Member(username = u)
        user.set_password(p)
        user.first_name = f
        user.last_name = l
        user.email = e
        user.gender = g
        user.dob = d
        user.save()

        for x in h:
            user.hobbies.add(int(x))

        profile = Profile()
        profile.desciption = ""
        profile.profile_picture = 'default.png'
        profile.save()
        user.profile = profile
        user.save()
        send_mail('MatchMe','Congrats, you have succesffuly sgined up to MatchMe, Your username is:  ' + u,'mematch98@gmail.com',[e],fail_silently=False)
        context = {'username': u}
        return render(request,'matchingSite/user-registered.html', context)
    else:
        raise Http404('POST data missing')

@csrf_exempt
def not_logged_in(request):
    return render(request,'matchingSite/not_logged_in.html')

@csrf_exempt
def login(request):
    if not ('username' in request.POST and 'password' in request.POST):
        return render(request,'matchingSite/login.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        try: member = Member.objects.get(username=username)
        except Member.DoesNotExist: raise Http404('User does not exist')
        if member.check_password(password):
            # users useraname and password
            request.session['username'] = username
            request.session['password'] = password
            context = {
               'loggedin': True
            }
            response = render(request, 'matchingSite/navigation.html', context)
            # last login cookie
            now = D.datetime.utcnow()
            max_age = 24 * 60 * 60  #one day
            delta = now + D.timedelta(seconds=max_age)
            format = "%a, %d-%b-%Y %H:%M:%S GMT"
            expires = D.datetime.strftime(delta, format)
            response.set_cookie('last_login',now,expires=expires)
            return response
        else:
            raise Http404('Wrong password')

@memberloggedin
@csrf_exempt
def logout(request, user):
    request.session.flush()
    return render(request,'matchingSite/index.html/')

@memberloggedin
@csrf_exempt
def matched_users(request, user):
    currentusername = request.session['username']
    matchusers = Member.objects.filter(hobbies__in=user.hobbies.all()).exclude(username=currentusername)
    matchuserscounted = Counter(matchusers)
    return render(request,'matchingSite/matched_users.html/', dict(users = matchuserscounted))

@csrf_exempt
@memberloggedin
def filter(request, user):
    print("RUNNING")
    gender = request.POST['gender']
    if gender == "M":
        gender = "F"
    else:
        gender ="M"

    matchusers = Member.objects.filter(hobby__in=user.hobbies.all()).exclude(username=user.username).exclude(gender=gender)
    matchuserscounted = Counter(matchusers)
    matchesuserlist = list(matchuserscounted)
    return HttpResponse(matchesuserlist)

@memberloggedin
@csrf_exempt
def navigation(request, user):
    return render(request, 'matchingSite/navigation.html/')

@memberloggedin
@csrf_exempt
def view_profile(request, user):
    currentusername = request.session['username']
    currentuser = Member.objects.get(username=currentusername)
    currentusersprofile = currentuser.profile
    print(currentusersprofile.profile_picture)
    context = {
        "username" : currentuser.username,
        "firstname" : currentuser.first_name,
        "lastname" : currentuser.last_name,
        "dob" : currentuser.dob,
        "gender" : currentuser.gender,
        "email" : currentuser.email,
        "hobbies" : currentuser.hobbies.all(),
        "img" : currentusersprofile.profile_picture,
        "description" : currentusersprofile.description
    }
    return render(request, 'matchingSite/view_profile.html/', context)

@memberloggedin
@csrf_exempt
def view_profiles(request, user):
    viewuser = request.GET['uview']
    vieweduser = Member.objects.get(username=viewuser)
    vieweduserprofile = vieweduser.profile
    context={
    "username" : vieweduser.username,
    "dob" : vieweduser.dob,
    "gender" : vieweduser.gender,
    "hobbies" : vieweduser.hobbies.all(),
    "img" : vieweduserprofile.profile_picture,
    "description" : vieweduserprofile.description
}
    return render(request, 'matchingSite/view_profiles.html/', context)

@memberloggedin
@csrf_exempt
def fav(request, user):
    viewuser = request.GET['uview']
    vieweduser = Member.objects.get(username=viewuser)
    currentuser = user.username
    viewuseremail = vieweduser.email
    send_mail('MatchMe', viewuser + ', ' + currentuser + 'has favourited your profile','mematch98@gmail.com',[viewuseremail],fail_silently=False)
    return render(request, 'matchingSite/navigation.html')

@memberloggedin
@csrf_exempt
def edit_profile(request, user):
    return render(request, 'matchingSite/edit_profile.html/')

@memberloggedin
@csrf_exempt
def edit_profile_info(request, user):
    if 'imgfile' in request.FILES:
        i = request.FILES['imgfile']
    else:
        i = 'default.png'
        print(i)
    des = request.POST['description']
    u = request.POST['username']
    g = request.POST['gender']
    d = request.POST['dob']
    f = request.POST['firstname']
    l = request.POST['secondname']
    e = request.POST['email']
    h = request.POST.getlist('hobbies')

    user.username = u
    user.first_name = f
    user.last_name = l
    user.email = e
    user.gender = g
    user.dob = d
    user.save()

    for x in h:
        user.hobbies.add(int(x))

    profile = user.profile
    profile.profile_picture = i
    profile.description = des
    profile.save()
    user.profile = profile
    user.save()
    return render(request, 'matchingSite/view_profile.html/', {})

@memberloggedin
@csrf_exempt
def change_password(request, user):
    if not ('pass' in request.POST):
        return render(request,'matchingSite/change_password.html')
    else:
         p = request.POST['pass']
         currentusername = request.session['username']
         user.set_password(p)
         user.save()
         return render(request, 'matchingSite/view_profile.html')

@csrf_exempt
def forgot_password(request):
    return render(request, 'matchingSite/forgot_password.html/', {})

@csrf_exempt
def forgot_password_info(request):
    u = request.POST['username']
    user = Member.objects.get(username = u)
    e = user.email
    p = password_generator()
    user.set_password(p)
    user.save()
    send_mail('MatchMe',u + ', You have asked us to send you a temporary password, Your password is:  ' + p + '. Please ensure you change this on the edit profile page as soon as you next login. ','mematch98@gmail.com',[e],fail_silently=False)
    return render(request, 'matchingSite/login.html/')

def password_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
