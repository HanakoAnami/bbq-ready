from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    name = models.CharField("イベント名", max_length=30)
    held_at = models.DateTimeField("開催日時", null=True, blank=True)
    location = models.CharField("開催場所", max_length=50)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)
    
    def __str__(self):
        return self.name

#持ち物テンプレ    
class BbqItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True)
    category = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return self.name
 
 #イベント用にコピーされた持ち物（チェック状態を保つように）   
class EventItem(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    bbq_item = models.ForeignKey(BbqItem, on_delete=models.CASCADE)
    
    is_selected = models.BooleanField(default=False)#必要かチェック
    status = models.IntegerField(default=1)#ステータス内容まだ決めてない
    
    def __str__(self):
        return f"{self.event} - {self.bbq_item.name}"
    