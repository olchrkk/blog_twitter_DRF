from django.urls import path
from . import views


urlpatterns = [
    path('posts/', views.PostsAll.as_view(), name='api-posts'),
    path('comments/', views.CommentList.as_view(), name='api-comments'),
    # path('user/profiles/', views.UserProfileList.as_view(), name='api-user-profiles'),
    path('posts/user/<int:id>/', views.PostsByUser.as_view(), name='api-user-posts'),
    path('comments/post/<int:id>/', views.CommentByPost.as_view(), name="api-comment-post"),
    path('comments/user/<int:id>/', views.CommentByUser.as_view(), name="api-comment-user"),
    path('comments/', views.CommentList.as_view(), name='api-comments'),
    path('comments/<int:pk>/', views.CommentDetail.as_view(), name='api-comment'),
    path('posts/', views.PostsAll.as_view(), name='api-posts'),
    path('posts/user/<int:id>', views.PostsByUser.as_view(), name='api-user-posts'),
    # path('user/profile/<int:pk>/', views.UserProfilesDetail.as_view(), name='api-user-profile'),
    # path('user/profiles/', views.UserProfileList.as_view(), name='api-user-profiles'),
]
