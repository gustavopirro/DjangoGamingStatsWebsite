from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages

from blog.models import PostReaction
from .forms import Post, PostForm, CommentForm, Comment
from users.forms import CustomUserChangeForm

import logging


logger = logging.getLogger(__name__)


######### USER METHODS #########


@login_required
def user_edit(request, pk):
    UserModel = get_user_model()
    user = get_object_or_404(UserModel, pk=pk)
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance = user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = CustomUserChangeForm(instance=user)
    return render(request, 'blog/user_edit.html', {'form': form})

@login_required
def user_list(request):
    UserModel = get_user_model()
    try:
        users = UserModel.objects.all().order_by('birth_date')
    except:
        logger.error('Could not get user')

    return render(request, 'blog/users_list.html', {'users': users})

@login_required
def user_remove(request, pk):
    UserModel = get_user_model()
    user = get_object_or_404(UserModel, pk=pk)

    try:
        user.delete()
        messages.success(request, 'User deleted')
    except:
        logger.error('Could not delete user')
        messages.error('Could not delete user')

    return redirect('user_list')


######### POST METHODS #########


def post_list(request):
    try:
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    except:
        logger.error("Could not retrieve post list")
    return render(request, 'blog/post_list.html', {'posts':posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if not post:
        logger.info(f'Post does id:{pk} not exist')
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
    if request.method == "POST":
         form = PostForm(request.POST)
         if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            try:
                post.save()
                messages.success(request, 'Post created')
            except:
                logger.error('Something went wrong while trying to create new post')
                messages.error('Could not create post')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
     post = get_object_or_404(Post, pk=pk)
     if request.method == "POST":
         form = PostForm(request.POST, instance=post)
         if form.is_valid():
             post = form.save(commit=False)
             post.author = request.user
             post.save()
             return redirect('post_detail', pk=post.pk)
     else:
         form = PostForm(instance=post)
     return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')


######### COMMENT METHODS #########


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)


######### REACTION METHODS #########


@login_required
def add_reaction(request,reaction_type, pk):
    exists_in_db = check_if_reacted(request, pk)

    if exists_in_db:
        old_reaction_type = PostReaction.objects.get(post_id=pk, user_id=request.user.pk).reaction_type
        change_reaction(request, old_reaction_type, reaction_type, pk=pk)
        return redirect('post_list')

    post = get_object_or_404(Post, pk=pk)
    user = request.user

    new_reaction = PostReaction(user=user, post=post, reaction_type=reaction_type)
    new_reaction.save()

    if reaction_type == 'like':
        post.likeCount += 1
        post.totalReactions += 1
        post.save()
    else:
        post.dislikeCount += 1
        post.totalReactions += 1
        post.save()

    return redirect('post_list')

@login_required
def change_reaction(request,old_reaction_type, new_reaction_type, pk):
    user_id = request.user
    post = get_object_or_404(Post, pk=pk)
    post_user_info = PostReaction.objects.get(post_id=post.pk, user_id=user_id)

    if old_reaction_type=='like' and new_reaction_type=='dislike':
        post.likeCount -= 1
        post.dislikeCount += 1
        post.save()

        post_user_info.reaction_type = 'dislike'
        post_user_info.save()
    elif old_reaction_type=='dislike' and new_reaction_type=='like':
        post.dislikeCount -= 1
        post.likeCount += 1
        post.save()  

        post_user_info.reaction_type = 'like'
        post_user_info.save()     
    elif old_reaction_type=='like' and new_reaction_type=='like':
        post.likeCount -= 1
        post.totalReactions -= 1
        post.save()
        post_user_info.delete()
    else:
        post.dislikeCount -= 1
        post.totalReactions -= 1
        post.save()
        post_user_info.delete()

@login_required
def check_if_reacted(request, pk):
    post_id = get_object_or_404(Post, pk=pk).pk
    user_id = request.user.pk

    post_user = PostReaction.objects
    exists_in_db = post_user.filter(post_id=post_id, user_id=user_id).exists()

    if exists_in_db:
        post_user_info = PostReaction.objects.get(post_id=post_id, user_id=user_id)
        return post_user_info
    else:
        return False 