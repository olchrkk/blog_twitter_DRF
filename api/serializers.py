from rest_framework import serializers
from blog.models import Post, Comment
from users.models import User


class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Post
        # fields = ['id', 'title', 'content', 'user', 'created', 'comment']
        fields = ['id', 'title', 'content', 'user', 'created']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'photo', 'city', 'country', 'bio']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Comment
        fields = ('id',  'content', 'user', 'post', 'created') 
