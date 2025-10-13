from django.urls import path, include
from .views import (
    landing_page, student_dashboard,
    login_view, signup_view, logout_view
)
from rest_framework import routers
from .views import SchoolViewSet, StudentProfileViewSet, SchoolPostViewSet, StudentChatViewSet

router = routers.DefaultRouter()
router.register(r'schools', SchoolViewSet)
router.register(r'students', StudentProfileViewSet)
router.register(r'posts', SchoolPostViewSet)
router.register(r'chats', StudentChatViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', landing_page, name='landing_page'),
    path('dashboard/', student_dashboard, name='student_dashboard'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
]