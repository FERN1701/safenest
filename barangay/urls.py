
from django.urls import path
from . import views

from django.conf import settings

from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path, include
#for Routing

urlpatterns = [
    path('',views.home,name = 'home'),
    path('create-account/',views.signup,name = 'signup'),
    path('email/verifications/',views.verify_email,name = 'verify_email'),
    path('barangay/',views.officials,name = 'officials'),
    path('barangay/users/',views.system_users,name = 'system_users'),
    path('barangay/users/roles/',views.user_roles_system,name = 'user_roles_system'),
    path('barangay/users/roles/<int:pk>/edit/',views.user_roles_edit,name = 'user_roles_edit'),
    path('barangay/users/roles/<int:pk>/deleted/',views.user_roles_delete,name = 'user_roles_delete'),
    path('barangay/users/<int:pk>/deleted/',views.user_system_delete,name = 'user_system_delete'),
    path('barangay/users/profile/',views.profile_users,name = 'profile_users'),
    path('barangay/about/',views.aboutus,name = 'aboutus'),

    path('barangay/history/',views.history,name = 'history'),
    path('barangay/alert/',views.emailalert,name = 'emailalert'),
    path('barangay/twillio/',views.twillio,name = 'twillio'),
    path('logout/',views.logoutUser, name='logoutUser'),
    path('barangay/user/',views.users,name = 'users'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)