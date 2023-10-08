from rest_framework.views import APIView
from rest_framework.views import Response
from . import serializers
from blog.models import Post, Comment
# from accounts.models import UserProfile
from .permissions import IsOwnerOrReadOnly
from rest_framework import permissions
from rest_framework import generics
from rest_framework.response import Response
from users.models import User

class CommentByPost(APIView):  

    def get(self, request, id):          
        comment_by_post = Comment.objects.filter(post__id=id)
        serializer = serializers.CommentSerializer(comment_by_post, many=True)
        
        return Response(serializer.data)  
    

class CommentByUser(APIView):  

    def get(self, request, id):          
        comment_by_user = Comment.objects.filter(user__id=id)
        serializer = serializers.CommentSerializer(comment_by_user, many=True)
        
        return Response(serializer.data)


class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer


class PostsAll(APIView):

    def get(self, request):
        all_posts = Post.objects.all()
        serializer = serializers.PostSerializer(all_posts, many=True)

        return Response(serializer.data)


class PostsByUser(APIView):

    def get(self, request, id):
        posts_by_user = Post.objects.filter(user__id=id)
        serializer = serializers.PostSerializer(posts_by_user, many=True)

        return Response(serializer.data)


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer = serializers.UserSerializer


    def get(self, request, id):
        profile_by_id = User.objects.filter(user__id=id)
        serializer = serializers.UserSerializer(profile_by_id, many=True)

        return Response(serializer.data)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
