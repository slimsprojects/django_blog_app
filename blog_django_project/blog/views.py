from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User 
from .models import Post, Category
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# from django import forms
# from django.forms import ModelForm
# from crispy_forms.helper import FormHelper


# Create your views here.
def home(request):
    context = {
        'posts': Post.objects.all() 
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name ='blog/home.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    # figure out how to use with function based views (only works with class based)
    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(PostListView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context 

#View list of posts of selected category
def CategoryListView(request, cats):
    category_posts = Post.objects.filter(category=cats).order_by('-date_posted')

    paginator = Paginator(category_posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    cat_menu = Category.objects.all()

    return render(request, 'blog/category_list.html', {'cats': cats.title(), 'category_posts':category_posts, 'page_obj':page_obj, 'cat_menu':cat_menu})

# View list of all categories within app
def CategoriesView(request):
    context = {
        'categories': Category.objects.all(),
        'cat_menu': Category.objects.all()
    }

    return render(request, 'blog/categories.html', context)

# View to add new category
class AddCategoryView(CreateView):
    model = Category
    template_name = 'blog/add_category.html'
    fields = '__all__'

    ##
    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(AddCategoryView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context 


class UserPostListView(ListView):
    model = Post
    template_name ='blog/user_posts.html' 
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

    ##
    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(UserPostListView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context 


class PostDetailView(DetailView):
    model = Post

    ##
    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(PostDetailView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context 


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'category','content']
    #category = forms.ChoiceField(choices=choice_list)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    ##
    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(PostCreateView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context 


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'category', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False 

    ##
    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(PostUpdateView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context 


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
    ##
    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(PostDeleteView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context 


def about(request):
    cat_menu = Category.objects.all()

    return render(request, 'blog/about.html', {'title':'About', 'cat_menu':cat_menu})


