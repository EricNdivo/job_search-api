from django.contrib import admin
from django.urls import path, include
from jobs.views import JobListView, JobDetailsView, JobDetailView, JobCreateView, JobUpdateView, JobDeleteView, JobApplicationCreateView, JobApplicationListView
from rest_framework.authtoken.views import obtain_auth_token
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
    path('jobs/applications/', JobApplicationListView.as_view(),name='job-applications')

]
