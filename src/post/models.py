from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add = True)
    post_comment = models.IntegerField(null=True,blank=True)
    author = models.ForeignKey('auth.User',on_delete=models.CASCADE,null= True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    
class PostPermission(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    can_delete_post = models.BooleanField(default=True)
    can_edit_post = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return str(self.user.username)