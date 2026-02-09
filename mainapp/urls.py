from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('image/', views.image_generate, name='image'),
    path('article/', views.article_generate, name='article'),
    path('download/', views.serve_generated_image, name='serve_generated_image'),  # ✅ NEW
    path('register/', views.register, name='register'),
    path('signin/', views.signin, name='signin'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('about/',views.about, name='about'),
    path('logout/', views.user_logout, name='logout'),
    path('history/', views.user_history, name='history'),

]
