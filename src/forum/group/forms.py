from django import forms

from .models import Group


class GroupForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = ["name", "description"]
        widgets = {
            "description": forms.Textarea(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            widget = self.fields[field_name].widget
            widget.attrs.update({
                "class": "form-control my-3",
                "style": "resize: none;",
            })