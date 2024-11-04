# blog/urls.py
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('tag/<slug:tag_slug>/', views.blog_list, name='blog_list_by_tag'),  # Blog list filtered by tag
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.blog_detail, name='blog_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('search/', views.search, name='blog_search'),  # Search route
    path('category/<slug:category_slug>/', views.blog_list, name='blog_list_by_category'),
]
