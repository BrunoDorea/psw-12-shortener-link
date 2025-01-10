from django.db import models
from secrets import token_urlsafe
from django.utils import timezone


class Links(models.Model):
    redirect_link = models.URLField()
    token = models.CharField(max_length=122, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration_time = models.DurationField(null=True, blank=True)
    max_uniques_cliques = models.PositiveIntegerField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.redirect_link

    def save(self, *args, **kwargs):
        if not self.token:
            while True:
                self.token = token_urlsafe(16)
                if Links.objects.filter(token=self.token).exists():
                    break
        super().save(*args, **kwargs)

    def expired(self):
        return (
            True if timezone.now() > (self.created_at + self.expiration_time) else False
        )


class Clicks(models.Model):
    link = models.ForeignKey(Links, on_delete=models.CASCADE)
    ip = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)
