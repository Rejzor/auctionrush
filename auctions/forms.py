from django import forms


class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()


class DeadlineDateForm(forms.Form):
    deadline_date = forms.DateTimeField(input_formats=['%d.%m.%Y %H:%M'], help_text="(DD.MM.YYYY HH:mm)")