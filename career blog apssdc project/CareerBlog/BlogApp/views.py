from django.shortcuts import render,redirect
from .models import BlogPost
from django.http import HttpResponse 
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignupForm 
from .forms import SigninForm
from .forms import BlogPostForm


def home(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    posts = BlogPost.objects.all()

    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))
    if category:
        posts = posts.filter(category=category)

    posts = posts.order_by('-published_date')
    categories = BlogPost.objects.values_list('category', flat=True).distinct()

    return render(request, 'home.html', {'posts': posts, 'query': query, 'categories': categories, 'selected_category': category})


def post_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    return render(request, 'post_detail.html', {'post': post})

def signin(request):
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():
            uname = request.POST['username']
            pwd =  request.POST['password']
            user = authenticate(request,username=uname, password=pwd)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {uname}!")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid credentials.")
    else:
        form = SigninForm()
    return render(request, 'signin.html', {'form': form})

@login_required
def signout(request):
    logout(request)
    messages.success(request, "You have been signed out.")
    return render(request, 'signout.html')


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically authenticate the user after signup
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')  # `password1` is used in UserCreationForm
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)  # Log the user in
                messages.success(request, "Account created and logged in successfully!")
                return redirect('home')  # Redirect to home page
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})
    


@login_required
def add_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Post added successfully!")
            return redirect('home')
    else:
        form = BlogPostForm()
    return render(request, 'add_post.html', {'form': form})

