from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views import View
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.views.generic import UpdateView, DeleteView

# View for the home page showing posts


class PostListView(LoginRequiredMixin, View):
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

# view for detail view of a post


class PostDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm()
        comments = Comment.objects.filter(post=post).order_by('-created_at')

        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }

        return render(request, 'socialapp/post_detail.html', context)

    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()

        comments = Comment.objects.filter(post=post).order_by('-created_at')

        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }

        return render(request, 'socialapp/post_detail.html', context)


# view for editing a post
class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['content']
    template_name = 'socialapp/post_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('post_detail', kwargs={'pk': pk})
    
    #function to check if the user is the author of the post
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


# view for deleting a post
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'socialapp/post_delete.html'
    success_url = reverse_lazy('post_list')
    
    #function to check if the user is the author of the post
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


# view for editing a comment
class CommentEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['content']
    template_name = 'socialapp/comment_edit.html'

    def get_success_url(self):
        post_pk = self.kwargs['post_pk']
        return reverse_lazy('post_detail', kwargs={'pk': post_pk})
    
    #function to check if the user is the author of the post
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


# view for deleting a comment
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'socialapp/comment_delete.html'

    def get_success_url(self):
        post_pk = self.object.post.pk
        return reverse_lazy('post_detail', kwargs={'pk': post_pk})
    
    #function to check if the user is the author of the post
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
