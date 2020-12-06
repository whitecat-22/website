from django import forms
from django.core.mail import EmailMessage
from django.forms import ModelForm, TextInput, Textarea
from blog.models import Comment, Blog     # Reply
from markdownx.fields import MarkdownxFormField
from markdownx.widgets import MarkdownxWidget


class ContactForm(forms.Form):
    name = forms.CharField(label='Full Name', max_length=30)
    email = forms.EmailField(label='Email Address',)
    subject = forms.CharField(label='Subject', max_length=30)
    message = forms.CharField(label='Message', widget=forms.Textarea)

    def __init__(self, *args, **kwrgs):
        super().__init__(*args, **kwrgs)

        self.fields['name'].widget.attrs['class'] = 'form-control-9'
        self.fields['name'].widget.attrs['placeholder'] = 'Please enter your name.'

        self.fields['email'].widget.attrs['class'] = 'form-control-11'
        self.fields['email'].widget.attrs['placeholder'] = 'Please enter your email address.'

        self.fields['title'].widget.attrs['class'] = 'form-control-11'
        self.fields['title'].widget.attrs['placeholder'] = 'Please enter your title.'

        self.fields['message'].widget.attrs['class'] = 'form-control-9'
        self.fields['message'].widget.attrs['placeholder'] = 'Please enter your message.'

    def send_email(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        title = self.cleaned_data['title']
        message = self.cleaned_data['message']

        subject = 'お問い合わせ {}'.format(title)
        message = '送信者名： {0}\nメールアドレス： {1}\nメッセージ：　{2}'.format(name, email, message)
        from_email = 'gattionobianco22@gmail.com'
        to_list = [
            'gattinobianco22@gmail.com'
        ]
        cc_list = [
            email
        ]

        message = EmailMessage(subject=subject, body=message, from_email=from_email, to=to_list, cc=cc_list)
        message.send()


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text')
        widgets = {
            'author': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Please enter your name.',
            }),
            'text': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Please enter your comments.',
            }),
        }
        labels = {
            'author': '',
            'text': '',
        }


#class ReplyForm(ModelForm):
#    class Meta:
#        model = Reply
#        fields = ('author', 'text')
#        widgets = {
#            'author': TextInput(attrs={
#                'class': 'form-control',
#                'placeholder': 'Please enter your name.',
#            }),
#            'text': Textarea(attrs={
#                'class': 'form-control',
#                'placeholder': 'Please enter your comments.',
#            }),
#        }
#        labels = {
#            'author': '',
#            'text': '',
#        }


class BlogCreateForm(forms.ModelForm):
#    text = MarkdownxFormField()

    class Meta:
        model = Post
#        fields = ('title', 'category', 'tag', 'content', 'is_public')
        fields = '__all__'
        widgets = {
            'text' : MarkdownxWidget(attrs={'class': 'textarea'})
        }

    def __init__(self. *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
