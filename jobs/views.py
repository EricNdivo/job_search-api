from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView, ListAPIView
from .models import Job
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import JobSerializer, JobApplicationSerializer, UserSerializer, JobApplication
from .utils import fetch_github_jobs, fetch_indeed_jobs, fetch_linkedin_jobs
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import serializers, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
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

class JobCreateView(APIView):
    permmission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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
class UserRegstrationView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Responsse({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=usernme):
            return Response({'error':'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(username=username, password=password)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error':'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class JobRecommendationView(APIView):
    def get(self, request):
        user = request.user
        recommended_jobs = self.get_recommended_jobs_for_user(user)
        serializer = JobSerializer(recommeded_jobs, many=True)
        return Response(serializer.data)

    def get_recommended_jobs_for_user(self, user):
        return Job.objects.all()

class JobSearchView(ListAPIView):
    serializer_class = JobSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description', 'company']

    def get_queryset(self):
        query = self.request.query_params.get('q',None)
        if query:
            return Job.objects.filter(title_icontains=query)
        return Job.objects.all()


class JobAnalyticsView(APIView):
    def get(self, request):
        total_jobs = Job.objects.count()
        total_applications = JobApplication.objects.count()
        
        jobs_per_company = Job.objects.values('company').annotate(count=Count('company'))
        jobs_per_location = Job.objects.values('location').annotate(count=Count('location'))
        applications_per_job = JobApplication.objects.values('job').annotate(count=Count('job'))
        applications_per_user = JobApplication.objects.values('user').annotate(count=Count('user'))
        
        data = {
            'total_jobs': total_jobs,
            'total_applications': total_applications,
            'jobs_per_company': list(jobs_per_company),
            'jobs_per_location': list(jobs_per_location),
            'applications_per_job': list(applications_per_job),
            'applications_per_user': list(applications_per_user)
        }
        return Response(data, status=status.HTTP_200_OK)
