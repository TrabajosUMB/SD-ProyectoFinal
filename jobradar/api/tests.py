from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import JobOffer

class AuthenticationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.login_url = reverse('token_obtain_pair')

    def test_user_can_login(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

class JobTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.job = JobOffer.objects.create(
            title='Test Job',
            company='Test Company',
            location='Test Location',
            description='Test Description',
            modality='Remote',
            category='Technology',
            url='http://test.com'
        )

    def test_get_jobs_list(self):
        url = reverse('jobs-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_job(self):
        url = reverse('jobs-list')
        data = {
            'title': 'New Job',
            'company': 'New Company',
            'location': 'New Location',
            'description': 'New Description',
            'modality': 'Hybrid',
            'category': 'Engineering',
            'url': 'http://newjob.com'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(JobOffer.objects.count(), 2)

class ScraperTests(TestCase):
    def test_scraper_format(self):
        from .scraper import format_job_data
        raw_data = {
            'title': ' Test Job  ',
            'company': '  Test Company ',
            'location': ' Test Location ',
            'description': ' Test Description ',
            'url': 'http://test.com'
        }
        formatted_data = format_job_data(raw_data)
        self.assertEqual(formatted_data['title'], 'Test Job')
        self.assertEqual(formatted_data['company'], 'Test Company')

