from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import routers, serializers, viewsets, permissions

from django.contrib.auth import get_user_model

from .models import Comment

User = get_user_model()

class ChildCommentSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = Comment
        fields = [
        "id",
        "user",
        'text',
        ]

class CommentSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    children = serializers.SerializerMethodField(read_only=True)

    def get_children(self, instance):
        # queryset = instance.get_children()
        # or
        queryset = Comment.objects.filter(parent__pk=instance.pk)
        serializer = ChildCommentSerializer(queryset,context={"request":instance}, many=True)
        return serializer.data

    class Meta:
        model = Comment
        fields = [
        'url',
        'id',
        'children',
        'user',
        # 'video',
        'text',
        ]

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
