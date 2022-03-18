from django.urls import path
from . import views

app_name    = "restaurant"
urlpatterns = [
    #↓はトップページを表示する
    path('', views.index, name="index"),
    #↓個別ページを表示する(特定店舗に対してレビューを投稿・閲覧させるため)
    path('<int:pk>/', views.single, name="single"),

    #飲食店投稿フォーム
    path('restaurant_create/', views.restaurant_create, name="restaurant_create"),

    #お問い合わせフォーム
    path('contact/', views.contact, name="contact"),

]
