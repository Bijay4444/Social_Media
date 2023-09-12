from django.shortcuts import render, redirect
from django.views import View
from .models import Post
from .forms import PostForm, CommentForm


class PostListView(View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-created_at')
        form = PostForm()

        context = {
            'post_list': posts,
            'form': form,
        }

        return render(request, 'socialapp/post_list.html', context)

    def post(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-created_at')
        form = PostForm(request.POST)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()

        return redirect('post_list')

class PostDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm()
        context = {
            'post': post,
            'form': form,
        }

        return render(request, 'socialapp/post_detail.html', context)
    
    
