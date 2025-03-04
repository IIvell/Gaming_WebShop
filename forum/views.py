from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def forum(request):
    # This view is accessible by both logged-in and unauthenticated users.
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'forum/forum.html', {'posts': posts})

@login_required
def create_post(request):
    # This view requires authentication.
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Automatically set the logged-in user as the author
            post.save()
            messages.success(request, "Post created successfully.")
            return redirect('forum:forum')  # Redirect to forum or another page
    else:
        form = PostForm()

    return render(request, 'forum/create_post.html', {'form': form})

def post_detail(request, post_id):
    # This view is accessible by both logged-in and unauthenticated users.
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()

    # If the user is logged in, they can comment on the post
    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.user = request.user  # Set the user who created the comment
            comment.save()
            return redirect('forum:post_detail', post_id=post.id)
    else:
        comment_form = CommentForm()

    return render(request, 'forum/post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})

@login_required
def edit_post(request, post_id):
    # This view requires authentication.
    post = get_object_or_404(Post, id=post_id)

    # Ensure only the post owner can edit
    if request.user != post.author:
        messages.error(request, "You can only edit your own posts.")
        return redirect('forum:forum')

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully.")
            return redirect('forum:post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'forum/edit_post.html', {'form': form, 'post': post})

@login_required
def delete_post(request, post_id):
    # This view requires authentication.
    post = get_object_or_404(Post, id=post_id)

    # Allow admins to delete any post, but users can only delete their own
    if request.user != post.author and not request.user.is_staff:
        messages.error(request, "You can only delete your own posts.")
        return redirect('forum:forum')

    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted successfully.")
        return redirect('forum:forum')

    return render(request, 'forum/delete_post.html', {'post': post})
