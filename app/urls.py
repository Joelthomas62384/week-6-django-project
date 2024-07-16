from django.urls import path
from . import views

urlpatterns = [
    path("",views.home,name="home"),
    path("login",views.login_view, name="login"),
    path("signup",views.signup_view, name="signup"),
    path("activate/<uid>/<token>",views.activate,name="activate"),
    path("logout",views.logout_app,name="logout"),
    path('about',views.About,name="about"),


    # Admin Panel
    path('page/admin',views.Admin_page,name="admin_page"),
    path('search',views.search,name="search"),
    path('delete/<id>',views.delete_user,name='delete_user'),
    path('create-user',views.create_user,name='create_user'),
    path('edit-user/<id>',views.edit_user,name="edit_user"),
    path('verify/<id>',views.verify,name="verify_user")


    
]
