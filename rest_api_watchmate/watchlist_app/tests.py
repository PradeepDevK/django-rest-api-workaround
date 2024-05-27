import json
from django.contrib.auth.models import User

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from watchlist_app.api import serializers
from watchlist_app import models

class StreamPlatformTestCase(APITestCase):
    
    def setUp(self):
        self.user  = User.objects.create_user(
            username = 'testcase2',
            password = 'testcase@123'
        )
        self.token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.stream = models.StreamPlatform.objects.create(
            name = 'Netflix',
            about = '#1 Straming Platform',
            website = 'https://www.netflix.com'
        )
    
    def test_streamplatform_create(self):
        data = {
            'name': 'Netflix',
            'about': '#1 Straming Platform',
            'website': 'https://www.netflix.com'
        }    
        url = reverse('streamplatform-list')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_streamplatform_list(self):
        url = reverse('streamplatform-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_streamplatform_detail(self):
        url = reverse('streamplatform-detail', args=(self.stream.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_streamplatform_update(self):
        data = {
            'name': 'Netflix',
            'about': '#1 Straming Platform - Updated',
            'website': 'https://www.netflix.com'
        }    
        url = reverse('streamplatform-detail', args=(self.stream.id,))
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_streamplatform_delete(self):
        url = reverse('streamplatform-detail', args=(self.stream.id,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        
class WatchlistTestCase(APITestCase):
    
    def setUp(self):
        self.user  = User.objects.create_user(
            username = 'testcase2',
            password = 'testcase@123'
        )
        self.token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.stream = models.StreamPlatform.objects.create(
            name = 'Netflix',
            about = '#1 Straming Platform',
            website = 'https://www.netflix.com'
        )
        
        self.watchlist = models.WatchList.objects.create(
            platform = self.stream,
            title = 'Example Movie',
            storyline = 'Example Story',
            active = True
        )
    
    def test_watchlist_create(self):
        data = {
            'platform': self.stream,
            'title': 'Example Movie',
            'storyline': 'Example Story',
            'active': True            
        }
        url = reverse('movie_list')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_watchlist_list(self):
        url = reverse('movie_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_watchlist_detail(self):
        url = reverse('movie_details', args=(self.watchlist.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.WatchList.objects.get().title, 'Example Movie')
        self.assertEqual(models.WatchList.objects.count(), 1)
        
    def test_watchlist_update(self):
        data = {
            'platform': self.stream,
            'title': 'Example Movie - Updated',
            'storyline': 'Example Story - Updated',
            'active': True            
        }
        url = reverse('movie_details', args=(self.watchlist.id,))
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_watchlist_delete(self):
        url = reverse('movie_details', args=(self.watchlist.id,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        

class ReviewTestCase(APITestCase):
    
    def setUp(self):
        self.user  = User.objects.create_user(
            username = 'testcase2',
            password = 'testcase@123'
        )
        self.token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.stream = models.StreamPlatform.objects.create(
            name = 'Netflix',
            about = '#1 Straming Platform',
            website = 'https://www.netflix.com'
        )
        
        self.watchlist = models.WatchList.objects.create(
            platform = self.stream,
            title = 'Example Movie',
            storyline = 'Example Story',
            active = True
        )
        
        self.watchlist2 = models.WatchList.objects.create(
            platform = self.stream,
            title = 'Example Movie 2',
            storyline = 'Example Story 2',
            active = True
        )
        
        self.review = models.Review.objects.create(
            review_user = self.user,
            rating = 5,
            description = 'Example Review',
            watchlist = self.watchlist2,
            active = True
        )
        
    def test_review_create(self):
        data = {
            'watchlist': self.watchlist,
            'review_user': self.user,
            'rating': 5,
            'description': 'Example Review',
            'active': True            
        }
        url = reverse('review_create', args=(self.watchlist.id,))
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Review.objects.count(), 2)        
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_review_create_unauthenticated(self):
        data = {
            'watchlist': self.watchlist,
            'review_user': self.user,
            'rating': 5,
            'description': 'Example Review',
            'active': True            
        }
        
        self.client.force_authenticate(user=None)
        url = reverse('review_create', args=(self.watchlist.id,))
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_review_update(self):
        data = {
            'watchlist': self.watchlist,
            'review_user': self.user,
            'rating': 4,
            'description': 'Example Review - Updated',
            'active': True            
        }
        url = reverse('review_detail', args=(self.review.id,))
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_review_list(self):
        url = reverse('review_list', args=(self.watchlist.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_review_detail(self):
        url = reverse('review_detail', args=(self.review.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_review_delete(self):
        url = reverse('review_detail', args=(self.review.id,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(models.Review.objects.count(), 0)
        
    def test_review_user(self):
        response = self.client.get('/watch/reviews/?username' + self.user.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        