from re import template
from unicodedata import name
from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.contrib import admin
from django.contrib.auth import views as auth_views
urlpatterns=[
    path('about/',views.about,name='about'),
    path('homepage/', views.HomePage.as_view(),name='home'),
    path('post-create/',views.PostCreate.as_view(),name='post-create'),
    path('login/',views.LoginUser.as_view(),name='login'),
    path('signup/',views.UserRegister.as_view(),name='signup'),
    path('userpost/',views.UserPosts.as_view(),name='userpost'),
    path('delete_post/<int:pk>',views.PostDelete.as_view(),name='delete_post'),
    path('signout/',LogoutView.as_view(next_page='home'),name='signout'),
    path('post-catagory/<str:cats>',views.PostCatagory,name='post-catagory'),
    path('post-update/<int:pk>',views.PostUpdate.as_view(),name='post-update'),
    path('post-detail/<int:pk>',views.PostDetail.as_view(),name='post-detail'),
    path('profile/',views.profile,name='profile'),
    path('add-comment/<int:pk>',views.AddPostComment.as_view(),name='add-comment'),
    path('view-comment/<int:pk>',views.PostComment.as_view(),name='view-comment'),
    path('users/',views.UserView.as_view(),name='users'),
    path('like-post/',views.like_post,name='like-post'),
    path('unlike-post',views.unlike_post,name='unlike-post'),
    path('delete-user/<int:pk>',views.DeleteUser.as_view(),name='delete-user'),
    path('edit-user/<int:pk>',views.UpdateUserStatus.as_view(),name='edit_user'),
    path('add-user/',views.RegisterAdmin.as_view(),name='add-user'),
    path('add-reply/<int:pk>',views.ReplyForComment.as_view(),name='add-reply'),
    path('view-reply/<int:pk>',views.ReplyLists.as_view(),name='view-reply'),
    path('password/',views.ChangePassword.as_view(),name='change-password'),
    path('pass_success',views.pass_success,name='chang-success'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)