from django.urls import path
from .views import mechanic_job_list, mechanic_job_update
from . import views

urlpatterns = [
    path('mechanic/', mechanic_job_list, name='mechanic_job_list'),
    path('mechanic/<int:job_id>/', mechanic_job_update, name='mechanic_job_update'),
    path('checklist/<int:job_id>/', views.mechanic_checklist, name='mechanic_checklist'),
    path('pdf/<int:job_id>/', views.job_card_pdf, name='job_card_pdf'),
    path('notifications/', views.get_notifications, name='get_notifications'),
    path('mark-read/<int:notification_id>/', views.mark_notification_read)
]
