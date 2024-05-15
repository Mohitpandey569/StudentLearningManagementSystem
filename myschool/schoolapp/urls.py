from django.urls import path , include
from  .import views


# app_name = 'app_users'
urlpatterns = [
    path('',views.home,name="home"),
    path('courses',views.single,name="courses"),
    path('courses/filter-data',views.filter_data,name="filter-data"),
    path("search",views.search,name='search'),
    path("course/<slug:slug>",views.courseDetails,name='courseDetails'),
    path("error",views.errorpage,name="error"),
    path("contact",views.contact,name="contact"),
    path("aboutus",views.aboutus,name="aboutus"),
    path('accounts/register',views.register,name="register"),
    path('accounts/',include('django.contrib.auth.urls')),
    path('doLogin',views.doLogin,name='doLogin'),
    path("accounts/profile",views.profile,name="profile"),
    path("account/profile/update",views.profile_update,name="profile_update"), 
    path('checkout/<slug:slug>',views.checkout,name='checkout') ,
    path('mycourse',views.mycourse,name='mycourse'),
    path('verify_payment',views.verify_payment,name ='verify_payment')  
 
]