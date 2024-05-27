from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from unittest.mock import patch
from .models import Job
from .serializers import JobSerializer

class JobListViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('job-list') 

        @patch('jobs.views.fetch_github_jobs')
        @patch('jobs.views.fetch_indeed_jobs')
        @patch('jobs.views.fetch_linkedin_jobs')
        def test_get_jobs(self, mock_fetch_linkedin_jobs, mock_fetch_indeed_jobs, mock_fetch_github_jobs):
            mock_fetch_github_jobs.return_value = [{'id': 1, 'title': 'Github Job', 'company': 'Github', 'description': 'Job description from Github'}]
            mock_fetch_indeed_jobs.return_value = [{'id': 2, 'title': 'Indeed Job', 'company': 'Indeed', 'description': 'Job description from Indeed'}]
            mock_fetch_linkedin_jobs.return_value = [{'id': 3, 'title': 'Indeed Job', 'company': 'LinkedIn', 'description': 'Job description from LinkedIn'}]

            response = self.client.get(self, url)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 3)
            self.assertEqual(response.data[0]['title'], 'Github Job')
            self.assertEqual(response.data[1]['title'], 'Indeed Job')
            self.assertEqual(response.data[2]['title'], 'LinkedIn Job')


class JobDetailsViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.job = Job.objects.create(title='Test Job', description='Test Description', company='Test Company')
        self.url = reverse('job-details', args=[self.job.pk])

    def test_get_job_detail(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        self.assertEqual(response.data['title'], self.job.title) 
        self.assertEqual(response.data['description'], self.job.description)
        self.assertEqual(response.data['company'], self.job.company)

class JobDetailViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.job = Job.objects.create(title='Test Job', description='Test Description', company='Test Company')
        self.url = reverse('job-detail-view', args=[self.job.pk]) 

    def test_get_existing_job(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.job.title) 
        self.assertEqual(response.data['description'], self.job.description)
        self.assertEqual(response.data['company'], self.job.company)

    def test_get_nonexistent_job(self):
        non_existent_pk = self.job.pk + 1
        url = reverse('job-detail-view', args=[non_existent_pk])    

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


