from django.shortcuts import render
from django.views.generic import TemplateView, DeleteView
from .models import Post
from .models import Comment
from users.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.utils.html import escape
from django.urls import reverse_lazy


class LikePostView(TemplateView):
    def post(self, request):
        post_id = request.POST['user_id']
        current_post = Post.objects.get(id=post_id)
        likes = [user for user in current_post.likes.all()]
        if request.user in likes:
            current_post.likes.remove(request.user)
        else:
            current_post.likes.add(request.user)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class LikeCommentView(TemplateView):
    def post(self, request):
        comment_id = request.POST['comment_id']
        current_comment = Comment.objects.get(id=comment_id)
        likes = [user for user in current_comment.likes.all()]
        if request.user in likes:
            current_comment.likes.remove(request.user)
        else:
            current_comment.likes.add(request.user)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class PostView(TemplateView):
    template_name = 'post.html'

    @method_decorator(login_required)
    def get(self, request, id):
        post = Post.objects.get(id=id)
        comments = Comment.objects.filter(post__id=id)
        followed_users = [user for user in request.user.follows.all()]
        commentsCount = comments.count()

        params = {
            'post': post,
            'comments': comments,
            'followed_users': followed_users,
            'commentsCount': commentsCount
        }
        return render(request, self.template_name, params)

    def post(self, request):
        content = escape(request.POST["new_post"])
        Post.objects.create(user=request.user, content=content)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # def delete(self, request, id):
    #     post = Post.objects.get(id=id)
    #     if request.user == post.user:
    #         post.delete()
    #         return HttpResponseRedirect(reverse('index'))
    #     else:
    #         return HttpResponseForbidden()

    # def dele(self, request, id):
    #     Comment.objects.filter(id=request.POST.get("id", "")).delete()

    #     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # def add_like(self, request, id):
    #     new_like = Post.objects.get()
    #     new_like.likes += 1
    #     new_like.save()

    #     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class CreateCommentView(TemplateView):

    def post(self, request):
        new_comment = request.POST["new_comment"]
        post_num = Post.objects.get(id=request.POST["post_id"])
        Comment.objects.create(content=new_comment,
                               user=request.user, post=post_num)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class CommentView(TemplateView):

    def post(self, request):
        comment = Comment.objects.get(id=request.POST["comment_id"])
        comment.delete()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class IndexView(TemplateView):
    template_name = 'main.html'

    @method_decorator(login_required)
    def get(self, request):
        followed_users = [user.id for user in request.user.follows.all()]

        followed_users_posts = Post.objects.filter(
            user__id__in=followed_users).order_by('-id')
        posts_recent_all = Post.objects.all().order_by(
            '-id').exclude(id__in=followed_users_posts)
        posts = (list(followed_users_posts) + list(posts_recent_all))[:6]

        last_users = User.objects.all().order_by('-id').exclude(id__in=followed_users).exclude(
            id=request.user.id)[:6]

        params = {
            'posts_recent': posts,
            'last_users': last_users
        }

        return render(request, self.template_name, params)


class SearchView(TemplateView):
    template_name = 'main.html'

    @method_decorator(login_required)
    def post(self, request):
        content = request.POST['content']

        posts_by_title = Post.objects.filter(title__icontains=content)
        posts_by_content = Post.objects.filter(content__icontains=content)
        posts = posts_by_title | posts_by_content
        # followed_users = [user.id for user in request.user.profile.first().follows.all()]
        # last_users = User.objects.all().order_by('-id').exclude(id__in=followed_users).exclude(id=request.user.id)[:3]
        params = {
            'posts_recent': posts,
            # 'last_users': last_users
            # 'comments': comments
        }
        return render(request, self.template_name, params)


class FeedView(TemplateView):
    template_name = 'feed.html'

    @method_decorator(login_required)
    def get(self, request):
        followed_users = [user.id for user in request.user.follows.all()]
        followed_users_posts = Post.objects.filter(
            user__id__in=followed_users).order_by('-id')
        posts_recent_all = Post.objects.all().order_by(
            '-id').exclude(id__in=followed_users_posts)
        posts = (list(followed_users_posts) + list(posts_recent_all))

        params = {
            'posts_recent': posts,
            # 'last_users': last_users
            # 'comments': comments
        }
        return render(request, self.template_name, params)


class SuggestionsView(TemplateView):
    template_name = "suggestions.html"

    @method_decorator(login_required)
    def get(self, request):
        followed_users = [user.id for user in request.user.follows.all()]
        last_users = User.objects.all().order_by(
            '-id').exclude(id__in=followed_users).exclude(id=request.user.id)

        params = {
            'last_users': last_users
        }
        return render(request, self.template_name, params)
