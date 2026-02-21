from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    name = models.CharField("イベント名", max_length=30)
    date = models.DateField("開催日")
    time = models.TimeField("開催時間")
    location = models.CharField("開催場所", max_length=50)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)
    
    def __str__(self):
        return self.name
    
class BbqItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bbq_item = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return self.name
    
class EventItem(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    bbq_item = models.ForeignKey(BbqItem, on_delete=models.CASCADE)
    
    is_selected = models.BooleanField(default=False)#必要かチェック
    status = models.IntegerField(default=1)#ステータス内容まだ決めてない
    
    def __str__(self):
        return f"{self.event} - {self.bbq_item}"
    