from django.db import models
from django.contrib.auth.models import User

class Recipe(models.Model):
    """ Represents a user-created recipe with a title, description, 
    ingredients, instructions, category, and timestamps. """
    title = models.CharField(max_length=255)
    description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, related_name='recipes')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Category(models.Model):
    """ Defines categories for organizing recipes. """
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Following(models.Model):
    """ Establishes a follower-following relationship between users. """
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')  # Ensures unique follow relationships

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"