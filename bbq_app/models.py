from django.db import models
from django.conf import settings

class Event(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="events")
    name = models.CharField("イベント名", max_length=30)
    held_at = models.DateTimeField("開催日時", null=True, blank=True)
    location = models.CharField("開催場所", max_length=50, blank=True)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)
    
    def __str__(self):
        return self.name
    

#イベント参加者    
class Participant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="participants")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="participant"
    )
    name = models.CharField("表示名", max_length=30)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)    
    
    def __str__(self):
        return f"{self.event.name} - {self.name}"
    

#持ち物テンプレ    
class BbqItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bbq_items")
    name = models.CharField("持ち物名", max_length=50, blank=True)
    category = models.CharField("カテゴリ", max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
class EventItem(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="event_items")
    bbq_item = models.ForeignKey(BbqItem, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, null=True, blank=True, on_delete=models.CASCADE, related_name="invitations")
    is_selected = models.BooleanField(default=False)
    status = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Invitation(models.Model):
    class Status(models.IntegerChoices):
        ACTIVE = 1, "有効"
        REVOKED = 2, "無効"
        USED = 3, "使用済"
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="invitations")
    token = models.CharField(max_length=300, unique=True)
    guest_name = models.CharField(max_length=30, blank=True)
    status = models.IntegerField(default=0) 
    revoked_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 


