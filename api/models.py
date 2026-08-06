from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    email = models.EmailField(max_length=254)
    REQUIRED_FIELDS=['email']
    def __str__(self):
        return self.username
    
class Post(models.Model):
    x = [
        ('FUN','Funny'),
        ('TECH','Technical'),
        ('OTHER','Other'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author   = models.ForeignKey(User,on_delete=models.CASCADE,related_name='posts')
    title = models.CharField(max_length=50,null=False,blank=False)
    category = models.CharField(choices=x,max_length=50)
    content  = models.TextField(blank=False,null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title    

class PostLike(models.Model):
    class LikeType(models.TextChoices):
        LIKE = 'LIKE', 'Like'
        DISLIKE = 'DISLIKE', 'Dislike'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    value = models.CharField(max_length=10, choices=LikeType.choices) # LIKE أو DISLIKE
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 💡 هذا هو السحر! يمنع نفس المستخدم من عمل أكثر من تفاعل واحد لنفس البوست
        unique_together = ('user', 'post')
        
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at'] # ترتيب التعليقات من الأحدث للأقدم

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.id}"