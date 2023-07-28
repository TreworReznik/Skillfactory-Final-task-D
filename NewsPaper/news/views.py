from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Subscriber
from .filters import PostFilter
from .forms import CreateForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect


class NewsList(ListView):
    model = Post
    ordering = '-date_of_creation'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'


class NewsSearch(NewsList):
    model = Post
    template_name = 'search.html'
    context_object_name = 'search'
    paginate_by = 10


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = CreateForm
    model = Post
    template_name = 'create_news.html'
    context_object_name = 'create_news'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.category_type = 'NW'

        return super().form_valid(form)


class ArticlesCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = CreateForm
    model = Post
    template_name = 'create_article.html'
    context_object_name = 'create_article'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.category_type = 'AR'

        return super().form_valid(form)


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = CreateForm
    model = Post
    template_name = 'create_news.html'


class ArticlesUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = CreateForm
    model = Post
    template_name = 'create_article.html'


class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')


class ArticlesDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('atricles_list', )


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscriber.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscriber.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories = Category.objects.annotate(
        subscribed=Exists(Subscriber.objects.filter(
            user=request.user,
            category=OuterRef('pk'),
        ))).order_by('name_category_post')
    return render(
        request,
        'subscribe.html',
        {'categories': categories},)
