from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from jobs.views import (
    JobListView,
    JobDetailView,
    JobDetailsView,
    JobCreateView,
    JobUpdateView,
    JobDeleteView,
    JobListByLocationView,
    JobApplicationCreateView,
    JobApplicationListView,
    JobRecommendationView,
    JobSearchView,
    JobAnalyticsView,
    UserRegistrationView,
    UserLoginView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/jobs/', JobListView.as_view(), name='job-list'),
    path('api/jobs/<int:pk>/', JobDetailsView.as_view(), name='job-details'),
    path('jobs/<int:pk>/', JobDetailView.as_view(), name='job-detail-view'),
    path('job-details/<int:pk>/', JobDetailsView.as_view(), name='job-detail'),
    path('jobs/create/', JobCreateView.as_view(), name='job-creation'),
    path('jobs/update/<int:pk>/', JobUpdateView.as_view(), name='job-update'),
    path('jobs/delete/<int:pk>/', JobDeleteView.as_view(), name='job-delete'),
    path('jobs/applications/', JobApplicationListView.as_view(),name='job-applications'),
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/',UserLoginView.as_view(), name='user-login'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('jobs/location', JobListByLocationView.as_view(),name='job-list-by-location'),
    path('jobs/apply/', JobApplicationCreateView.as_view(), name='job-apply'),
    path('jobs/search/',JobSearchView.as_view(), name='job-search'),
    path('jobs/recommendations/', JobRecommendationView.as_view(), name='job-recommendations'),
    path('jobs/analytics/', JobAnalyticsView.as_view(),name='job-analytics'),




]
