from rest_framework import serializers
from video_and_tag.models import Video,Tag
from django.utils import timezone

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'
        read_only_fields = (["uploaded_at"])

    def create(self, validated_data):
        obj = super().create(validated_data)

        obj.uploaded_at = timezone.now()
        obj.save()
        return obj
    def update(self, instance, validated_data):
        #old_created_at = instance.created_at
        obj = super().update(instance, validated_data)
        obj.save()
        return obj
