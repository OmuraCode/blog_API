from django.db import models

from posts.models import Post


class Like(models.Model):
    owner = models.ForeignKey('auth.user', related_name='likes', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['owner', 'post']
                            # id7  like  14 post
                            # id7  like  15 post
                            # id7  like  14 post нельзя


class Favorite(models.Model):
    owner = models.ForeignKey('auth.user', related_name='favorites', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='favorites', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['owner', 'post']