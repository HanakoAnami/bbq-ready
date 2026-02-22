from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Event

class SignupForm(UserCreationForm):
    nickname = forms.CharField(label="名前/ニックネーム", max_length=30, required=True)
    email = forms.EmailField(label="メールアドレス", required=True)

    class Meta:
        model = User
        fields = ("nickname", "email", "password1", "password2")
    
    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        #usernameにemailを入れて運用、usernameの重複をチェックする
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("このメールアドレスは既に登録されています。")
        return email
        
    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data["email"].lower()
        nickname = self.cleaned_data["nickname"]
        user.username = email
        user.email = email
        user.first_name = nickname
    
        if commit:
            user.save()
        return user
    
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ("name", "date", "time", "location")

     


