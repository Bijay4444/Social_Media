"""socialapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('',views.PostListView.as_view(), name='post_list'),
    path('post/<int:pk>', views.PostDetailView.as_view(), name='post_detail'),
    path('post/edit/<int:pk>', views.PostEditView.as_view(), name='post_edit'),
    path('post/delete/<int:pk>', views.PostDeleteView.as_view(), name='post_delete'),
    path('post/<int:post_pk>/comment/edit/<int:pk>', views.CommentEditView.as_view(), name='comment_edit'),
    path('post/<int:post_pk>/comment/delete/<int:pk>', views.CommentDeleteView.as_view(), name='comment_delete'),
    path('post/<int:pk>/like', views.AddLike.as_view(), name='like'),
    path('post/<int:pk>/dislike', views.AddDislike.as_view(), name='dislike'),
    path('profile/<int:pk>', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/<int:pk>', views.ProfileEditView.as_view(), name='profile_edit'),
    path('profile/<int:pk>/followers/add', views.AddFollower.as_view(), name='add_follower'),
    path('profile/<int:pk>/followers/remove', views.RemoveFollower.as_view(), name='remove_follower'),
    path('search/', views.UserSearch.as_view(), name='profile_search'),
]
