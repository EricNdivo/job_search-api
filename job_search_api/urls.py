from django.urls import path
from jobs.views import (
    JobListView, JobDetailsView, JobCreateView, JobUpdateView, 
    JobDeleteView, JobListByLocationView, UserRegistrationView, 
    JobApplicationCreateView, JobApplicationListView, UserLoginView, 
    JobRecommendationView, JobAnalyticsView, JobAlertView
)

urlpatterns = [
    path('jobs/', JobListView.as_view(), name='job-list'),
    path('jobs/<int:pk>/', JobDetailsView.as_view(), name='job-detail'),
    path('jobs/create/', JobCreateView.as_view(), name='job-create'),
    path('jobs/update/<int:pk>/', JobUpdateView.as_view(), name='job-update'),
    path('jobs/delete/<int:pk>/', JobDeleteView.as_view(), name='job-delete'),
    path('jobs/location/', JobListByLocationView.as_view(), name='job-location'),
    # path('jobs/search/', JobSearchView.as_view(), name='job-search'),
    path('jobs/analytics/', JobAnalyticsView.as_view(), name='job-analytics'),
    path('jobs/recommendations/', JobRecommendationView.as_view(), name='job-recommendations'),
    path('jobs/alerts/', JobAlertView.as_view(), name='job-alerts'),
    path('users/register/', UserRegistrationView.as_view(), name='user-register'),
    path('users/login/', UserLoginView.as_view(), name='user-login'),
    path('applications/', JobApplicationListView.as_view(), name='application-list'),
    path('applications/create/', JobApplicationCreateView.as_view(), name='application-create'),
]
