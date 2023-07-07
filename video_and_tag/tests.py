from django.test import TestCase
from users.models import CustomUser
from django.apps import apps
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from video_and_tag.models import Tag, Video
from video_and_tag.serializers import TagSerializer, VideoSerializer
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
class TagTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.tag1 = Tag.objects.create(name='tag1')
        self.tag2 = Tag.objects.create(name='tag2')
        self.user = CustomUser.objects.create_user(username='testuser', password='Yasin2324@133',email='testuser@gmail.com')
        self.client.force_authenticate(user=self.user)

    def test_get_all_tags(self):
        response = self.client.get(reverse('tag-list'))
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_tag(self):
        response = self.client.get(reverse('tag-detail', kwargs={'pk': self.tag1.id}))
        tag = Tag.objects.get(id=self.tag1.id)
        serializer = TagSerializer(tag)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_new_tag(self):
        data = {'name': 'new tag'}
        response = self.client.post(reverse('tag-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class VideoTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='testuser2', password='Yasin2324@1332',email='testuser2@gmail.com')
        self.video1 = Video.objects.create(user=self.user, title='video1', description='description1')
        self.video2 = Video.objects.create(user=self.user, title='video2', description='description2')
        self.tag1 = Tag.objects.create(name='tag1')
        self.tag2 = Tag.objects.create(name='tag2')
        self.video1.tags.add(self.tag1)
        self.video2.tags.add(self.tag2)
        self.client.force_authenticate(user=self.user)

    def test_get_all_videos(self):
        response = self.client.get(reverse('video-list'))
        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_video(self):
        response = self.client.get(reverse('video-detail', kwargs={'pk': self.video1.id}))
        video = Video.objects.get(id=self.video1.id)
        serializer = VideoSerializer(video)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_new_video_with_tags(self):
        data = {'title': 'new video', 'description': 'new description', 'tags': [{'name': 'tag1'}, {'name': 'tag2'}]}
        response = self.client.post(reverse('video-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['tags'], [{'id': self.tag1.id, 'name': 'tag1'}, {'id': self.tag2.id, 'name': 'tag2'}])

    def test_update_video_tags(self):
        data = {'tags': [{'name': 'tag1'}, {'name': 'tag2'}, {'name': 'tag3'}]}
        response = self.client.patch(reverse('video-detail', kwargs={'pk': self.video1.id}), data, format='json')
        self.assertEqual(response)