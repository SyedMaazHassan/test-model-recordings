from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path('signup', views.signup, name="signup"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('upload-file', views.upload_file, name="upload-file"),
    path('abc', views.abc, name="abc"),
    path('abc2', views.abcc, name="abc2"),
    path('test', views.test, name="test")
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
