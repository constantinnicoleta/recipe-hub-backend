from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Recipe(models.Model):
    """
    Represents a cooking recipe. Each recipe includes details such as
    a title,description,ingredients, instructions,
    an optional image,and an associated category.
    It is authored by a user
    and tracks timestamps for when it was created and last updated.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()
    image = CloudinaryField('image', blank=True, null=True)
    category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL,
        null=True, related_name='recipes')
    author = models.ForeignKey(
         User, on_delete=models.CASCADE, related_name='recipes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Category(models.Model):
    """
    Represents a category for grouping recipes.
    Examples include "Desserts" or "Main Courses."
    Each category has a name and an optional description.
    """
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    """
    Represents a comment made on a recipe.
    Each comment includes the content, the user who
    posted it, and the recipe it is associated with.
    It also tracks when the comment was created.
    """
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.recipe.title}"


class Like(models.Model):
    """
    Represents a 'like' on a recipe.
    Each like is associated with a user and a recipe,
    and it tracks when the like was created.
    """
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} likes {self.recipe.title}"


class Following(models.Model):
    """
    Represents a following relationship between users.
    Each record indicates that one user
    (the follower) is following another user (the following).
    It also tracks when the follow relationship was created.
    """
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"
