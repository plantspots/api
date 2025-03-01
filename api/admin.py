from django.contrib import admin
from api.models import Tier, User, RequestType, Request, RequestImage

# Register your models here.
admin.site.register(Tier)
admin.site.register(User)
admin.site.register(RequestType)
admin.site.register(Request)
admin.site.register(RequestImage)