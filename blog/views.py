from django.shortcuts import render,HttpResponseRedirect
from .forms import Signup,LoginForm,AddPost
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout
from .models import Post
from django.contrib.auth.models import Group


# Create your views here.
def home(request):
    posts = Post.objects.all()
    return render(request , 'blog/home.html',{'posts':posts})

def about(request):
    return render(request,'blog/about.html')

def contact(request):
    return render(request,'blog/contact.html')

def dashboard(request):
    if request.user.is_authenticated:
        posts  = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        grps = user.groups.all()
        ip = request.session.get('ip' , 0)       
        return render(request , 'blog/dashboard.html',{'posts': posts ,'full_name':full_name ,'groups':grps , 'ip':ip})
    else:
        return HttpResponseRedirect('/login/')

def user_signup(request):
    if request.method == 'POST':
        form = Signup(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulation!! You become an Author.')
            user = form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)
    else:
        form = Signup()
    # form = Signup()
    return render(request , 'blog/signup.html',{'form':form})

def user_login(request):
     if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data.get('username')
                upass = form.cleaned_data.get('password')
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in Successfully!!')
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = LoginForm()
        return render(request, 'blog/login.html', {'form': form})
     else:
         return HttpResponseRedirect('/dashboard/')

def Logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = AddPost(request.POST)
            if form.is_valid():
                title = form.cleaned_data.get('title')
                desc = form.cleaned_data.get('desc')
                pst = Post(title=title,desc=desc)
                pst.save()
                form = AddPost()
        else:
            form = AddPost()
        return render(request , 'blog/addpost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')

def edit_post(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            form = AddPost(request.POST , instance=pi)
            if form.is_valid():
                form.save()
        else:
            pi = Post.objects.get(pk=id)
            form = AddPost(instance=pi)
        return render(request , 'blog/editpost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')


def delete_post(request,id):
    if  request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            pi.delete()
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')


