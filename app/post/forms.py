from django import forms

from .models import MainPost, Answer


class MainPostForm(forms.ModelForm):

    class Meta:
        model = MainPost
        fields = ['title', 'content']
        widgets = {
            "content": forms.Textarea()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            widget = self.fields[field_name].widget
            widget.attrs.update({
                "class": "form-control my-3",
                "style": "resize: none;",
            })
        

class AnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ['content']
        widgets = {
            "content": forms.Textarea()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields
        for field_name in self.fields:
            widget = self.fields[field_name].widget
            widget.attrs.update({
                "class": "form-control my-3",
                "style": "resize: none;",
            })
