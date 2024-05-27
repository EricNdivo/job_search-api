from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView, ListAPIView
from .models import Job
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import JobSerializer, JobApplicationSerializer, UserSerializer, JobApplication
from .utils import fetch_github_jobs, fetch_indeed_jobs, fetch_linkedin_jobs
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import serializers, generics
from rest_framework.pagination import PageNumberPagination
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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class JobUpdateView(UpdateAPIView):
    queryset = Job.objects.all
    serializer_class = JobSerializer

class JobDeleteView(DestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

class JobListByLocationView(ListAPIView):
    serializer_class = JobSerializer

    def get_queryset(self):
        location = self.request.query_params.get('location', None)
        if location:
            return Job.objects.filter(location_icontains=location)
        return Job.objects.all()

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer

class JobListPagination(PageNumberPagination):
    page_size = 10

class JobListView(APIView):
    def get(self, request):
        paginator = JobListPagination()
        jobs = Job.objects.all()
        result_page = paginator.paginate_queryset(jobs, request)
        serializer = JobSerializer(result_page, many=True)
        return paginator.get_paginated_response(serialier.data)

class JobApplicationCreateView(CreateAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer

class JobApplicationListView(ListAPIView):
    serializer_class = JobApplicationSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return JobAppliation.objects.none()
        return JobApplication.objects.filter(user=user)
