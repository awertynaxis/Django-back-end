from django.urls import path
from master.views import signup_user, login_user, logoutuser, \
    MasterSkillsListView, DetailedSkillView, AddServiceView, CreateMasterView, AddMasterTelegramInfoView
    # master_skills_list_view, detail_skill_list_view, add_service_view, create_master_view, add_master_telegram_info_view

urlpatterns = [
    path('services/', MasterSkillsListView.as_view(), name='skill_list'),
    path('detail/', DetailedSkillView.as_view(), name='detail_skill'),
    path('addservice/', AddServiceView.as_view(), name='add_service'),
    path('createmaster/', CreateMasterView.as_view(), name='create_master'),
    path('addmastertelegram/', AddMasterTelegramInfoView.as_view(), name='add_master_telegram'),
    path('signup/', signup_user, name='signupuser'),
    path('login/', login_user, name='loginuser'),
    path('logout/', logoutuser, name='logoutuser'),
]
