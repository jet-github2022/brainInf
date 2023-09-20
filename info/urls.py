from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('post/<str:pk>', views.blog, name="post"),
    path('about', views.about, name="about"),
    path('contact', views.contact, name="contact"),
    path('signup', views.signUp, name="signup"),
    path('login', views.loginUser, name="login"),
    path('logout', views.logoutUser, name="logout"),
    path('news', views.news, name="news"),
    path('mail', views.mail, name="mail"),
    # path('activate/<uidb64>/<token>', views.activate, name='activate')
]