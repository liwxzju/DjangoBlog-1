from django.views.generic import FormView, ListView, DetailView
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostForm
from .models import Post
from apps.follow.models import Follow
import markdown2


class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = 'community/post_create.html'
    form_class = PostForm
    success_url = '/'

    def get_login_url(self):
        # 复写此 url 获取到登录页面
        return reverse('usera:sign_in')

    def get_form_kwargs(self):
        kwargs = super(PostCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class IndexView(ListView):
    model = Post
    template_name = "community/index.html"
    context_object_name = "post_list"

    def get_queryset(self):
        post_list = Post.objects.all()
        for post in post_list:
            post.body = markdown2.markdown(post.body, extras=['fenced-code-blocks'], )
        return post_list


class PostDetailView(DetailView):
    model = Post
    template_name = 'community/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get_object(self, queryset=None):
        obj = super(PostDetailView, self).get_object()
        obj.body = markdown2.markdown(obj.body, extras=['fenced-code-blocks'], )
        return obj


class UserFollowsListView(ListView):
    model = Post
    template_name = 'community/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        print(self.request.user)
        # follow_list = Follow.objects.filter(trigger_user=self.request.user)
        follow_list = self.request.user.followed_objects.all()
        print(follow_list)
        object_list = []
        for follow in follow_list:
            object_list.append(follow.content_object)
            print(follow.content_object)
        return object_list
