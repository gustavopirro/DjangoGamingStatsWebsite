from django.conf import settings
from django.db import models
from django.utils import timezone



class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    totalReactions = models.IntegerField(default=0)
    likeCount = models.IntegerField(default=0)
    dislikeCount = models.IntegerField(default=0)
    cover = models.ImageField(blank=True, default=None)


    def like_percentage(self):
        if self.totalReactions == 0:
            return 0
        return (self.likeCount / self.totalReactions) * 100
    
    def dislike_percentage(self):
        if self.totalReactions == 0:
            return 0
        return (self.dislikeCount / self.totalReactions) * 100

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)   

class PostReaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name="post_reactions")
    created_date = models.DateTimeField(auto_now=True)
    reaction_type = models.CharField(max_length=20)