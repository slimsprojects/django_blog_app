from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView, CategoryListView, AddCategoryView, CategoriesView, ProfilePostListView, ProfileCategoryListView, LikeView
from . import views 

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('categories', CategoriesView, name='categories'),
    path('categories/<str:cats>/', CategoryListView, name='category'),
    path('add_category/', AddCategoryView.as_view(), name='add-category'),
    path('about/', views.about, name='blog-about'),

    path('profile/', ProfilePostListView, name='profile'),
    path('profile/<str:cats>/', ProfileCategoryListView, name='profile-cat'),
    path('like/<int:pk>', LikeView, name='like-post'),
]