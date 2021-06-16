from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User 
from .models import Post, Category
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
# from django import forms
# from django.forms import ModelForm
# from crispy_forms.helper import FormHelper


# Create your views here.
def home(request):
    context = {
        'posts': Post.objects.all() 
    }
    return render(request, 'blog/home.html', context)

# Home View/ Main TL post View
class PostListView(ListView):
    model = Post
    template_name ='blog/home.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 7

    # figure out how to use with function based views (only works with class based)
    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(PostListView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context 

# View list of posts of selected category
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


# View for Posts by User
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


# View for Posts of Current Profile
def ProfilePostListView(request):
    user = request.user
    profile_posts = Post.objects.filter(author=user).order_by('-date_posted')
    paginator = Paginator(profile_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    cat_menu = Category.objects.all()

    my_cats = []
    for post in profile_posts:
        if post.category in my_cats:
            pass
        else:
            my_cats.append(post.category)

    return render(request, 'blog/profile.html', {'user':user, 'profile_posts':profile_posts, 'page_obj':page_obj, 'cat_menu':cat_menu, 'my_cats':my_cats})


# View for Profile Posts by category
def ProfileCategoryListView(request, cats):
    prof_category_posts = Post.objects.filter(author=request.user, category=cats).order_by('-date_posted')
    profile_posts = Post.objects.filter(author=request.user).order_by('-date_posted')

    paginator = Paginator(prof_category_posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    cat_menu = Category.objects.all()

    my_cats = []
    for post in profile_posts:
        if post.category in my_cats:
            pass
        else:
            my_cats.append(post.category)

    return render(request, 'blog/prof_cat_list.html', {'cats': cats.title(), 'prof_category_posts':prof_category_posts, 'page_obj':page_obj, 'cat_menu':cat_menu, 'my_cats':my_cats})


# View for liking post
def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked_var = False 
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked_var = False 
    else:
        post.likes.add(request.user)
        liked_var = True

    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))


# View for reporting post
def ReportView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))

    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))


# View for Detail View of Post
class PostDetailView(DetailView):
    model = Post

    ##
    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(PostDetailView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu

        total_like_var = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = total_like_var.total_likes()
        context["total_likes"] = total_likes

        liked_var = False
        if total_like_var.likes.filter(id=self.request.user.id).exists():
            liked_var = True
        context["liked_var"] = liked_var

        return context 


# View to Create New Post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'category','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    ##
    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(PostCreateView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context 


# View to Update Post
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


# View to Delete Post
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


# View About Page
def about(request):
    cat_menu = Category.objects.all()

    return render(request, 'blog/about.html', {'title':'About', 'cat_menu':cat_menu})


