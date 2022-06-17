from django import forms
from .models import BlogPost, Blocked


class AddBlockedForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddBlockedForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Blocked
        exclude = ('user_blocker',)


class AddPostsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddPostsForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = BlogPost
        exclude = ('writer',)

