from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Event, BbqItem
from django.contrib.auth import get_user_model

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
        fields = ("name", "held_at", "location")
        widgets =  {
            "held_at": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M"
            )
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["held_at"].input_formats = ["%Y-%m-%dT%H:%M"]
        

class BbqItemForm(forms.ModelForm):
    class Meta:
        model = BbqItem
        fields = ["name", "category"]
        labels = {
            "name": "持ち物名",
            "category": "カテゴリー",
        }
        
class ForgottenItemForm(forms.ModelForm):
    class Meta:
        model =BbqItem
        fields = ["name", "category"]
        labels = {"name": "持ち物名", "category": "カテゴリー",}
    
    
        
class UserNameForm(forms.Form):
    name = forms.CharField(label="新しいユーザー名", max_length=30, required=True)
    
class UserEmailForm(forms.Form):
    email = forms.EmailField(label="新しいメールアドレス", required=True)
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
    
    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        
        #同じメールアドレスを使っている人がいないかチェック(=username)
        qs = User.objects.filter(username=email).exclude(id=self.user.id)
        if qs.exists():
            raise forms.ValidationError("このメールアドレスはすでに登録されています。")
        return email
    
User = get_user_model()

class EmailUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)
        labels = {"email": "新しいメールアドレス"}
        widgets = {"email": forms.EmailInput(attrs={"placeholder": "example@email.com"})}
     


