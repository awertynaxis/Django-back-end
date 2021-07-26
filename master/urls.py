from django.urls import re_path, path
from master.views import signup_user, login_user, logoutuser, \
    master_skills_list_view, detail_skill_list_view, add_service_view, create_master_view, add_master_telegram_info_view

urlpatterns = [
    path('services/', master_skills_list_view, name='skill_list'),
    path('detail/', detail_skill_list_view, name='detail_skill'),
    path('addservice/', add_service_view, name='add_service'),
    path('createmaster/', create_master_view, name='create_master'),
    path('addmastertelegram/', add_master_telegram_info_view, name='add_master_telegram'),
    path('signup/', signup_user, name='signupuser'),
    path('login/', login_user, name='loginuser'),
    path('logout/', logoutuser, name='logoutuser'),
]
