from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms
from ammblog_app.models import BlogPost

class _BaseForm(object):
   def clean(self):
       for field in self.cleaned_data:
           if isinstance(self.cleaned_data[field], basestring):
               self.cleaned_data[field] = self.cleaned_data[field].strip()
       return self.cleaned_data


class BaseModelForm(_BaseForm, forms.ModelForm):
   pass


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Email'}))
    first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Last Name'}))
    username = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder': 'Username'}))
    password1 = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password Confirmation'}))

    class Meta:
        fields = ['email', 'username', 'first_name', 'last_name', 'password1', 'password2']
        model = User


class AuthenticateForm(AuthenticationForm):
    username = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password'}))


class BlogPostForm(BaseModelForm):
    content = forms.CharField(required=True,
                              widget=forms.widgets.Textarea(attrs={'class': 'blogText'}),
                              error_messages={'required': 'Field can''t be empty!'})

    def is_valid(self):
        form = super(BlogPostForm, self).is_valid()
        for f in self.errors.iterkeys():
            if f != '__all__':
                self.fields[f].widget.attrs.update({'class': 'error blogText'})
        return form

    class Meta:
        model = BlogPost
        exclude = ('user',)
