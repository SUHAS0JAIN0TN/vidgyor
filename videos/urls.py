from . import views
from django.urls import path
from django.conf.urls.static import static
# from free_food import settings
from django.conf import settings

urlpatterns = [
        path('',views.index,name='index'),
        path('login/',views.login,name='login'),
        path('signup/',views.signup,name='signup'),
        path('video-list/',views.main_page,name='main_page'),
        # path('simp-api/',views.simp_api,name='simp_api'),
        path('video-list/',views.video_list,name='video_list'),
        # path('give-food/',views.simp1,name='simp1'),
        path('logout/',views.logout,name='logout'),
]+static(settings.STATIC_URL, document_root=settings.STATIC_DIR)+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)