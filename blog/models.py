from django.db import models
from users.models import User



class Post(models.Model):
    content = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='posts')
    created = models.DateTimeField(auto_now_add=True, blank=True)
    likes = models.ManyToManyField(User, blank=True, related_name='liked_posts')

    def __str__(self):
        return self.title

    def likesCount(self):
        return len([like for like in self.likes.all()]) if [like for like in self.likes.all()] else 0

    class Meta:
        ordering = ['-created']
    
class Comment(models.Model):
    content = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    created = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    likes = models.ManyToManyField(User, blank=True, related_name='liked_comments')

    def __str__(self):
        return self.content

    def likesCount(self):
        return len([like for like in self.likes.all()])
