from django.urls import path
from django.conf.urls.static import static 
from django.conf import settings 
from Auth.views import SendPasswordResetEmailView,PointListView, UserChangePasswordView, UserLoginView, UserProfileView, UserRegistrationView, UserPasswordResetView,UserGetView,DeleteUserView,LineStringList,UpdateUserView , SegmentList , WaterLevelAPIView, NotificationList , HistoryList,SfaxWeatherView,ParametreWeatherAPIView , ParametrAPIView,ParametresAPIView,ZoneView,SegmentListCreateView,NotificationDetail
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    path('All_user/', UserGetView.as_view(), name='users'),
    path('delete/<int:id>/', DeleteUserView.as_view(), name='delete-user'),
    path('update/<int:pk>/', UpdateUserView.as_view(), name='update-user'),
    path('points/', PointListView.as_view(), name='point-list'),
    path('points/<int:pk>/', PointListView.as_view(), name='point-detail'),
    path('linestrings/', LineStringList.as_view(), name='linestring-list'),
    path('line_delete/<int:pk>/', LineStringList.as_view(), name='point-detail'),
    path('segment/', SegmentList.as_view(), name='point-detail'),
    path('segments/<int:pk>/', SegmentList.as_view(), name='point-detail'),
    path('linestring/water-levels/<int:pk>/', WaterLevelAPIView.as_view(), name='water-levels'),
    path('notification/', NotificationList.as_view(), name='water-levels'),
    path('history/<int:id>/', HistoryList.as_view(), name='water-levels'),
    path('history/', HistoryList.as_view(), name='water-levels'),
    path('sfax-weather/', SfaxWeatherView.as_view()),
    path('parametre/<int:pk>/', ParametreWeatherAPIView.as_view(), name='update-user'),
    path('parametreweather/<int:pk>/', ParametrAPIView.as_view(), name='update-user'),
    path('parame/', ParametresAPIView.as_view(), name='point-detail'),
    path('zone/<int:pk>/', ZoneView.as_view(), name='point-detail'),
    path('line-strings/<int:pk>/segments/', SegmentListCreateView.as_view(), name='segment-list-create'),
    path('notif/<int:notification_id>/', NotificationDetail.as_view(), name='notification-detail'),
    path('noti/<int:id>/', NotificationDetail.as_view(), name='water-levels'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


