from django.conf import settings
from django.db import models
from django.http import request
from blog.models import PostReaction
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import Post, PostForm, CommentForm, Comment
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import logging


logger = logging.getLogger(__name__)

def post_list(request): 
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    if posts:
        logger.debug("Post found")
        return render(request, 'blog/post_list.html', {'posts':posts})
    else:
        logger.error("Post list not found")

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
     if request.method == "POST":
         form = PostForm(request.POST)
         if form.is_valid():
             post = form.save(commit=False)
             post.author = request.user
             post.save()
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