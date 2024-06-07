from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView, ListAPIView
from .models import Job, User, JobApplication
from django.db.models import Count
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import JobSerializer, JobApplicationSerializer, UserSerializer
from .utils import fetch_github_jobs, fetch_indeed_jobs, fetch_linkedin_jobs, fetch_ebay_jobs, store_jobs_in_db, send_new_jobs_email
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
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
        try:
            ebay_jobs = fetch_ebay_jobs()
        except ConnectionError:
            ebay_jobs = []

        jobs = github_jobs + indeed_jobs + ebay_jobs
        new_jobs = store_jobs_in_db(jobs)

        if new_jobs:
            user = request.user
            send_new_jobs_email(user, new_jobs)

        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class JobDetailsView(RetrieveAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description', 'company']
    ordering_fields = ['created_at', 'title', 'company', 'location']

class JobCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JobUpdateView(UpdateAPIView):
    queryset = Job.objects.all()
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

class UserRegistrationView(CreateAPIView):
    serializer_class = UserSerializer

class JobListPagination(PageNumberPagination):
    page_size = 10

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
            return JobApplication.objects.none()
        return JobApplication.objects.filter(user=user)

class UserRegistrationView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

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
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class JobRecommendationView(APIView):
        def get(self, request):
            user = request.user
            applied_companies = JobApplication.objects.filter(user=user).values_list('job__company', flat=True)
            recommended_jobs = Job.objects.filter(company__in=applied_companies)
            serializer = JobSerializer(recommended_jobs, many=True)
            return Response(serializer.data)

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

class JobAlertView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        alerts = Job.objects.filter(title__icontains='freelance')
        serializer = JobSerializer(alerts, many=True)
        return Response(serializer.data)

