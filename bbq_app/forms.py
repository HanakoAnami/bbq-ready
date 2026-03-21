from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Event, BbqItem
from django.contrib.auth import get_user_model
from django.utils import timezone

class LoginForm(AuthenticationForm):

    username = forms.EmailField(
        label="メールアドレス",
        error_messages={
            "required": "メールアドレスを入力してください",
        }
    )

    password = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput,
        error_messages={
            "required": "パスワードを入力してください",
        }
    )

    error_messages = {
        "invalid_login": "メールアドレスまたはパスワードが正しくありません",
        "inactive": "このアカウントは利用できません",
    }


class SignupForm(UserCreationForm):
    nickname = forms.CharField(
        label="名前/ニックネーム",
        max_length=30, 
        required=True,
        error_messages={
            "required": "名前を入力してください",
        },
        widget=forms.TextInput(attrs={
            "placeholder": "名前 / ニックネーム"
        })
    )
    
    email = forms.EmailField(
        label="メールアドレス",
        required=True,
        error_messages={
            "required": "メールアドレスを入力してください",
        },
        widget=forms.EmailInput(attrs={
            "placeholder": "メールアドレス"
        })
    )

    class Meta:
        model = User
        fields = ("nickname", "email", "password1", "password2")
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields["password1"].widget.attrs["placeholder"] = "パスワード"
        self.fields["password2"].widget.attrs["placeholder"] = "パスワード再入力"
    
        self.fields["password1"].error_messages["required"] = "パスワードを入力してください"
        self.fields["password2"].error_messages["required"] = "パスワードを再入力してください"
     
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

    name = forms.CharField(
        label="イベント名",
        required=True,
        error_messages={
            "required": "イベント名を入力してください。"
        }
    )

    held_at = forms.DateTimeField(
        required=True,
        error_messages={
            "required": "開催日時を入力してください。"
        },
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local"},
            format="%Y-%m-%dT%H:%M"
        )
    )

    class Meta:
        model = Event
        fields = ("name", "held_at", "location")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["held_at"].input_formats = ["%Y-%m-%dT%H:%M"]

    def clean_held_at(self):
        held_at = self.cleaned_data.get("held_at")

        # 新規作成のときだけ過去日を禁止
        if not self.instance.pk:
            if held_at and held_at < timezone.now():
                raise forms.ValidationError("過去の日付は登録できません。")

        return held_at
        

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
    name = forms.CharField(
        label="新しいユーザー名",
        max_length=30,
        required=True,
        error_messages={
            "required": "ユーザー名を入力してください。"
        },
        widget=forms.TextInput(attrs={
            "placeholder": "新しいユーザー名"
        })
    )
    
    
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


class EmailUpdateForm(forms.Form):
    email = forms.EmailField(
        label="新しいメールアドレス",
        required=True,
        error_messages={
            "required": "メールアドレスを入力してください。",
            "invalid": "正しいメールアドレスを入力してください。"
        },
        widget=forms.EmailInput(attrs={
            "placeholder": "example@mail.com"
        })
    )
    
    def clean_email(self):
        email =self.cleaned_data["email"].lower()
        
        #すでに登録されているかチェック
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("このメールアドレスはすでに登録されています。")
        
        return email
    

class CustomPasswordChangeForm(PasswordChangeForm):

    error_messages = {
        "password_incorrect": "現在のパスワードが正しくありません。",
        "password_mismatch": "新しいパスワードが一致していません。",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["old_password"].error_messages = {
            "required": "現在のパスワードを入力してください。"
        }

        self.fields["new_password1"].error_messages = {
            "required": "新しいパスワードを入力してください。"
        }

        self.fields["new_password2"].error_messages = {
            "required": "確認用パスワードを入力してください。",
        }
        
     


