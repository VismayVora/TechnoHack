from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from django.conf.urls import include,url

router = DefaultRouter()
router.register(r'guardians', views.GuardianDetails)
router.register(r'checkins', views.CheckInAPI)

urlpatterns = [
    url('', include(router.urls)),
    path('register/', views.RegisterAPI.as_view(), name="register"),
    path('login/', views.LoginAPI.as_view(), name="login"),
    path('logout',views.logout,name="logout"),
    path('news',views.news,name="news"),
    path('nearbysearch',views.nearby_search,name="Nearby Search"),
    path('location',views.LocationAPI.as_view(),name="location"),
    path('audit-form',views.AuditFormAPI.as_view(),name="audit-form"),
    path('alert',views.sos_alert,name="sos_alert"),
    path('share-location',views.sharelocation,name="share-location"),
    path('fake-call',views.fakecall,name="fake-call")
]