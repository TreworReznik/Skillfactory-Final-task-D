from django_filters import FilterSet
from .models import Post, Category
from django.forms import DateInput, TextInput, Select
import django_filters


class PostFilter(FilterSet):

    article_title = django_filters.CharFilter(
        field_name='article_title',
        lookup_expr='icontains',
        label='Title',
        widget=TextInput(attrs={'class': 'form-control'})
    )
    post_category = django_filters.ModelChoiceFilter(
        field_name='post_category__name_category_post',
        queryset=Category.objects.all(),
        label='Category',
        widget=Select(attrs={'class': 'form-control'})
    )
    date_of_creation = django_filters.DateTimeFilter(
        field_name='date_of_creation',
        lookup_expr='gt',
        label='Date',
        localize=True,
        widget=DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}))