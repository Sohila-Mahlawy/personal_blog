from django.shortcuts import render, redirect, get_object_or_404  # Import get_object_or_404 here
from .models import BlogPost, User, Comment
from django.contrib.auth import authenticate, login as auth_login, logout
from .forms import BlogPostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse



# View to display all posts, most recent first
def welcome(request):
    posts = BlogPost.objects.all().order_by('-publication_date')  # Fetch all posts, most recent first
    for post in posts:
        # Use `like_set` to filter by `user` in the related `Like` model
        post.is_liked_by_user = post.like_set.filter(user=request.user).exists() if request.user.is_authenticated else False 
    return render(request, 'welcome/index.html', {'posts': posts})


# Login view
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('index')
        else:
            return render(request, 'welcome/login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'welcome/login.html')

# Register view
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')        
        if User.objects.filter(username=username).exists():
            return render(request, 'welcome/register.html', {'error': 'Username already taken'})
        
        user = User.objects.create_user(username=username, password=password, email=email)
        auth_login(request, user)
        return redirect('index')
    
    return render(request, 'welcome/register.html')

# Logout view
def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def add_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            return redirect('index')
    else:
        form = BlogPostForm()
    return render(request, 'welcome/add_blog_post.html', {'form': form})

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog_post = post
            comment.author = request.user
            comment.save()

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Check if it's an AJAX request
                return JsonResponse({
                    'author': comment.author.username,
                    'content': comment.content,
                    'publication_date': comment.publication_date.strftime('%Y-%m-%d %H:%M:%S'),
                })

    return redirect('index')
    


@login_required
def delete_blog_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)

    # Check if the logged-in user is the author or a superuser
    if post.author == request.user or request.user.is_superuser:
        post.delete()
        return redirect('index')  # Redirect to the index page after deletion
    else:
        return redirect('index')  # Optionally show an error message if needed


@login_required
def edit_blog_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)

    # Check if the user is the author of the post or a superuser
    if post.author != request.user and not request.user.is_superuser:
        return redirect('index')  # Redirect to the homepage if the user is not authorized

    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)  # Pre-fill form with the existing post data
        if form.is_valid():
            form.save()  # Save the changes to the post
            return redirect('index')  # Redirect to the homepage after editing
    else:
        form = BlogPostForm(instance=post)  # Pre-fill form with the existing post data

    return render(request, 'welcome/edit_blog_post.html', {'form': form, 'post': post})


# new

@login_required
def like_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    liked = False

    if request.user in post.likes.all():
        # If user already liked the post, unlike it
        post.likes.remove(request.user)
    else:
        # Otherwise, like the post
        post.likes.add(request.user)
        liked = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Check if it's an AJAX request
        return JsonResponse({'liked': liked, 'like_count': post.likes.count()})
    return redirect('index')