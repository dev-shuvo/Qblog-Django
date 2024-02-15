from django import forms
from .models import Post
from django.utils.safestring import mark_safe
from django.core.validators import FileExtensionValidator


class PostForm(forms.ModelForm):
    thumbnail = forms.FileField(
        widget=forms.ClearableFileInput(),
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"])],
    )

    class Meta:
        model = Post
        fields = [
            "title",
            "thumbnail",
            "category",
            "post",
            "slug",
        ]
        labels = {
            "title": "Title",
            "thumbnail": "Thumbnail",
            "category": "Category",
            "post": "Post",
            "slug": "Slug",
        }

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field != "post":
                self.fields[field].widget.attrs["class"] = "form-control"

            self.fields["thumbnail"].label = mark_safe(
                f'<label class="form-label">Thumbnail</label>'
            )
            self.fields[field].label = mark_safe(
                f'<label class="form-label">{self.fields[field].label}</label>'
            )
