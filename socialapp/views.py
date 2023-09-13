from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from .models import Post
from .forms import PostForm, CommentForm
from django.views.generic import UpdateView, DeleteView

#View for the home page showing posts
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

#view for detail view of a post
class PostDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm()
        context = {
            'post': post,
            'form': form,
        }

        return render(request, 'socialapp/post_detail.html', context)
    
#view for editing a post    
class PostEditView(UpdateView):
    model = Post
    fields = ['content']
    template_name = 'socialapp/post_edit.html'
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('post_detail', kwargs={'pk': pk})

#view for deleting a post

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'socialapp/post_delete.html'
    success_url = reverse_lazy('post_list')