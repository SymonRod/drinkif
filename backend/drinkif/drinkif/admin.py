from django.contrib import admin
from drinkif import models

admin.site.register(models.ExtendedUser)
admin.site.register(models.phrases)
admin.site.register(models.FriendshipRequest)