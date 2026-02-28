from django.db import models
from django.conf import settings

class Event(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="events")
    name = models.CharField("イベント名", max_length=30)
    held_at = models.DateTimeField("開催日時", null=True, blank=True)
    location = models.CharField("開催場所", max_length=50)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

#イベント参加者    
class Participant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="participants")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    

#持ち物テンプレ    
class BbqItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True)
    category = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class EventItem(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="event_items")
    bbq_item = models.ForeignKey(BbqItem, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, null=True, blank=True, on_delete=models.CASCADE, related_name="invitations")
    is_selected = models.BooleanField(default=False)
    status = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
 


