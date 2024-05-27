from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView
from .models import Job
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import JobSerializer
from .utils import fetch_github_jobs, fetch_indeed_jobs, fetch_linkedin_jobs

class JobListView(APIView):
    def get(self, request):
        try:
            github_jobs = fetch_github_jobs()
        except ConnectionError:
            github_jobs = []
        try:
            indeed_jobs = fetch_indeed_jobs()
        except ConnectionError:
            indeed_jobs = []
        try:
            linkedin_jobs = fetch_linkedin_jobs()
        except ConnectionError:
            linkedin_jobs = []
        
        jobs = github_jobs + indeed_jobs + linkedin_jobs
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class JobDetailsView(RetrieveAPIView):
    queryset = Job.objects.all
    serializer_class = JobSerializer
    filter_backends = ['title', 'description', 'company']
    search_fields = ['title', 'description', 'company']
    ordering_fields = ['created_at', 'title', 'company', 'location']

class JobDetailView(APIView):
    def get(self, request, pk):
        try:
            job = Job.objects.get(pk=pk)
        except Job.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = JobSerializer(job)
        return Response(serializer.data)       

class JobCreateView(CreateAPIView):
    queryset = Job.objects.all
    serializer_class = JobSerializer

class JobUpdateView(UpdateAPIView):
    queryset = Job.objects.all
    serializer_class = JobSerializer

class JobDeleteView(DestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer