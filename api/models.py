from django.db import models

# Create your models here.
class Tier(models.Model):
    rank = models.IntegerField(blank=False, null=False, unique=True)
    name = models.CharField(max_length=256, blank=False, null=False)
    color = models.CharField(max_length=256, blank=False, null=False)

    def __str__(self):
        return f"{self.rank} | {self.name}"

    class Meta:
        ordering = ['rank']

class User(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    last_updated = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    username = models.CharField(max_length=256, blank=False, null=False, unique=True)
    password = models.CharField(max_length=256, blank=False, null=False)
    email = models.CharField(max_length=256, blank=False, null=False, unique=True)
    phone = models.CharField(max_length=256, blank=False, null=False, unique=True)
    hash = models.CharField(max_length=256, blank=False, null=False, unique=True)
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return f"{self.username} | {self.email} | {self.phone}"
    
    class Meta:
        ordering = ['created']

class RequestType(models.Model):
    type = models.CharField(max_length=256, blank=False, null=False)
    color = models.CharField(max_length=256, blank=False, null=False)
    identification_number = models.IntegerField(blank=False, null=False, unique=True)

    def __str__(self):
        return f"{self.identification_number} | {self.type}"
    
    class Meta:
        ordering = ['type']

class Request(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    last_updated = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    title = models.TextField(blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    type = models.ForeignKey(RequestType, on_delete=models.CASCADE, blank=False, null=False)
    closed = models.DateTimeField(null=True, blank=False, default=None)
    email_contact = models.BooleanField(null=False, blank=False)
    phone_contact = models.BooleanField(null=False, blank=False)

    def __str__(self):
        return f"{self.title}"
    
    class Meta:
        ordering = ['created']

class RequestImage(models.Model):
    added = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    request = models.ForeignKey(Request, blank=False, null=False, related_name="images")
    image = models.TextField(blank=False, null=False)

    def __str__(self):
        return f"Image from Request #{self.request.pk}"
    
    class Meta:
        ordering = ['added']