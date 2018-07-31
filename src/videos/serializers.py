from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import routers, serializers, viewsets, permissions

from comments.serializers import CommentSerializer
from django.contrib.auth import get_user_model
from .models import Video, Category
from rest_framework.reverse import reverse



class CategoryUrlHyperlinkedIdentityField(serializers.HyperlinkedIdentityField):
    #lookup_field = 'slug'
    #pass

    def get_url(self, obj, view_name, request, format):
        kwargs = {
        'slug':obj.slug
        }
        return reverse(view_name, kwargs=kwargs, request=request, format=format)



class CategorySerializer(serializers.HyperlinkedModelSerializer):
    url = CategoryUrlHyperlinkedIdentityField(view_name='category_detail_api')

    class Meta:
        model = Category
        fields = [
        'url',
        'id',
        'slug',
        'title',
        'description',
        'image',
        ]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class VideoSerializer(serializers.HyperlinkedModelSerializer):
    # category_title = serializers.CharField(source='category.title',read_only=True)
    # category_image = serializers.CharField(source='category.get_image_url',read_only=True)
    category = CategorySerializer(many=False, read_only=True)
    comment_set = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Video
        fields = [
        'url',  
        'id',
        'slug',
        'title',
        'order',
        'embed_code',
        'share_message',
        'timestamp',
        'category',
        # 'category_image',
        # 'category_title',
        'comment_set',
        ]

class VideoViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Video.objects.all()
    serializer_class = VideoSerializer