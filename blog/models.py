from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Blog(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog')
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="images")

    def __str__(self):
        return self.title
    
