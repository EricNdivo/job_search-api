from django.contrib import admin
from django.urls import path, include
from jobs.views import JobListView, JobDetailsView, JobDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/jobs/', JobListView.as_view(), name='job-list'),
    path('api/jobs/<int:pk>/', JobDetailsView.as_view(), name='job-details'),
]
