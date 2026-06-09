from django.urls import path
from dashboard import views


urlpatterns = [
    path('', views.home, name='home'),
    
   path('upload-attendance/', views.upload_attendance, name='upload_attendance'),
    path('upload-work-submission/', views.upload_work_submission, name='upload_work_submission'),
    path('upload-performance-review/', views.upload_performance_review, name='upload_performance_review'),
    path('upload-leave-data/', views.upload_leave_data, name='upload_leave_data'),
    path('upload-engagement-survey/', views.upload_engagement_survey, name='upload_engagement_survey'),
    path('upload-skill-matrix/', views.upload_skill_matrix, name='upload_skill_matrix'),

    path('attendance-analytics/', views.attendance_analytics, name='attendance_analytics'),
    path('work-submission-analytics/', views.work_submission_analytics, name='work_submission_analytics'),
    path('upload-performance-review/', views.upload_performance_review, name='upload_performance_review'),
    path('performance-review-analytics/', views.performance_review_analytics, name='performance_review_analytics'),

]

