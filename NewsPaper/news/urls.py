from django.urls import path
from .views import NewsList, NewsDetail, NewsSearch, NewsCreate, ArticlesCreate, NewsUpdate, ArticlesUpdate, NewsDelete, ArticlesDelete


urlpatterns = [
    path('', NewsList.as_view()),
    path('news/', NewsList.as_view(), name='news_list'),
    path('news/create/', NewsCreate.as_view(), name='create_news'),
    path('news/<int:pk>/update/', NewsUpdate.as_view(), name='news_update'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),

    path('articles/', NewsList.as_view(), name='atricles_list'),
    path('articles/create/', ArticlesCreate.as_view(), name='create_article'),
    path('articles/<int:pk>/update/', ArticlesUpdate.as_view(), name='articles_update'),
    path('articles/<int:pk>/delete/', ArticlesDelete.as_view(), name='articles_delete'),

    path('news/<int:pk>', NewsDetail.as_view(), name='new_detail'),
    path('search/', NewsSearch.as_view(), name='news_search'),
]