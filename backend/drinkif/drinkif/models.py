from re import U
from django.db import models
from django.contrib.auth.models import User

class phrases(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    phrase_text = models.CharField(max_length=300)
    public = models.BooleanField(default=True)

    def dict(self):
        return {
            'id': self.pk,
            'creator': self.creator.username,
            'phrase_text': self.phrase_text,
            'public': self.public
        }

    def by_user(self,user):
        if self.public or self.creator == user:
            return self.dict()
        return None


    def __str__(self):
        return self.phrase_text

class ExtendedUser(models.Model):
    def user_data(self):
        avatar_url = f"https://avatars.dicebear.com/api/adventurer-neutral/{self.avatar_seed}.svg?scale=70"
        data = {
            'username': self.user.username,
            'id': self.user.id,
            'description':self.description ,
            'avatar':{
                'seed':self.avatar_seed,
                'url': avatar_url
            },
            'creation_date': self.user.date_joined,
            'isDeveloper': self.is_developer,
            }
        return data

    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='data')
    avatar_seed = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    friends = models.ManyToManyField(User, blank=True, related_name='friends')
    is_developer = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class FriendshipRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_request')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.sender.username} -> {self.receiver.username}"