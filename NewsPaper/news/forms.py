from django.forms import ModelForm, CharField, Select, Textarea, ModelChoiceField, TextInput
from .models import Post, Author, Category
from django.core.exceptions import ValidationError


class CreateForm(ModelForm):
    article_title = CharField(label='Title',
        min_length=5,
        max_length=128,
        widget=TextInput(
        attrs={'class': 'form-control'})
        )
    author = ModelChoiceField(widget=Select(
        attrs={'class': 'form-select'}),
        queryset=Author.objects.all()
        )
    text = CharField(
        min_length=20,
        widget=Textarea(
        attrs={'class': 'form-control'})
        )
    post_category = ModelChoiceField(widget=Select(
        attrs={'class': 'form-select'}),
        queryset=Category.objects.all()
        )

    class Meta:
        model = Post
        fields = ['article_title', 'text', 'author','post_category']

    def clean(self):
        cleaned_data = super().clean()
        self.article_title = cleaned_data.get('article_title')
        self.text = cleaned_data.get('text')
        self.author = cleaned_data.get('author')
        if self.article_title == self.text:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )

        return cleaned_data



