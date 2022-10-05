from django.db import models

# Create your models here.


class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Plan(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="event")
    name = models.CharField(max_length=50)
    start_at = models.DateTimeField()
    description = models.TextField()

    def __str__(self):
        return self.name
