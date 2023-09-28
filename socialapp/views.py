from django.shortcuts import render, redirect
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views import View
from .models import Post, Comment, UserProfile, Notification, ThreadModel
from .forms import PostForm, CommentForm, ThreadForm
from django.views.generic import UpdateView, DeleteView

# View for the home page showing posts

class PostListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logged_in_user = request.user
        posts = Post.objects.filter(
                author__profile__followers__in=[logged_in_user.id]
            ).order_by('-created_at')
        form = PostForm()

        context = {
            'post_list': posts,
            'form': form,
        }

        return render(request, 'socialapp/post_list.html', context)

    def post(self, request, *args, **kwargs):
        logged_in_user = request.user
        posts = Post.objects.filter(
                author__profile__followers__in=[logged_in_user.id]
            ).order_by('-created_at')
        form = PostForm(request.POST, request.FILES)

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
        notification = Notification.objects.create(notification_type = 2, from_user = request.user, to_user=post.author, post= post )
        

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

#view for replying to a comment in a post
class CommentReplyView(LoginRequiredMixin, View):
    def post(self, request, post_pk, pk, *args, **kwargs):
        post = Post.objects.get(pk=post_pk)
        parent_comment = Comment.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.parent = parent_comment
            new_comment.save()
        
        notification = Notification.objects.create(notification_type = 2, from_user = request.user, to_user=parent_comment.author, comment = new_comment )
        

        return redirect('post_detail', pk=post_pk)

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

# view for adding a like to a comment
class AddCommentLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)

        # checking if comment is already disliked by the user
        is_dislike = False

        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break
        
        # removing dislike if already disliked
        if is_dislike:
            comment.dislikes.remove(request.user)

        # logic for adding like
        is_like = False

        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            comment.likes.add(request.user)
            notification = Notification.objects.create(notification_type = 2, from_user = request.user, to_user=comment.author, comment = comment )
        

        if is_like:
            comment.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
        

# view for adding a dislike to a comment
class AddCommentDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
            comment = Comment.objects.get(pk=pk)

            # checking if comment is already liked by the user
            is_like = False

            for like in comment.likes.all():
                if like == request.user:
                    is_like = True
                    break
            
            # removing like if already liked
            if is_like:
                comment.likes.remove(request.user)

            # logic for adding dislike
            is_dislike = False

            for dislike in comment.dislikes.all():
                if dislike == request.user:
                    is_dislike = True
                    break

            if not is_dislike:
                comment.dislikes.add(request.user)

            if is_dislike:
                comment.dislikes.remove(request.user)

            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)

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

# view for showing the profile of a user
class ProfileView(View):
    def get(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        user = profile.user
        posts = Post.objects.filter(author=user).order_by('-created_at')
        followers = profile.followers.all()

        if len(followers) == 0:
            is_following = False

        for follower in followers:
            if follower == request.user:
                is_following = True
                break
            else:
                is_following = False

        number_of_followers = len(followers)
        
        context = {
            'user': user,
            'profile': profile,
            'posts': posts,
            'number_of_followers': number_of_followers,
            'is_following': is_following,
        }
        
        return render(request, 'socialapp/profile.html', context)

#view for editing the profile of a user    
class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserProfile
    fields = ['name', 'bio', 'birth_date', 'address', 'profile_pic']
    template_name = 'socialapp/profile_edit.html'
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('profile', kwargs={'pk': pk})
    
    #function to check if the user is the author of the post
    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user
    
#views for follower management
class AddFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.add(request.user)
        
        notification = Notification.objects.create(notification_type = 3, from_user = request.user, to_user=profile.user )
        
        
        return redirect('profile', pk=profile.pk)
    
class RemoveFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.remove(request.user)
        
        return redirect('profile', pk=profile.pk)
    
class AddLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)

        # checking if post is already disliked by the user
        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break
        
        # removing dislike if already disliked
        if is_dislike:
            post.dislikes.remove(request.user)

        # logic for adding like
        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            post.likes.add(request.user)
            notification = Notification.objects.create(notification_type = 1, from_user = request.user, to_user=post.author, post= post )
        

        if is_like:
            post.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
        
    
class AddDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
            post = Post.objects.get(pk=pk)

            # checking if post is already liked by the user
            is_like = False

            for like in post.likes.all():
                if like == request.user:
                    is_like = True
                    break
            
            # removing like if already liked
            if is_like:
                post.likes.remove(request.user)

            # logic for adding dislike
            is_dislike = False

            for dislike in post.dislikes.all():
                if dislike == request.user:
                    is_dislike = True
                    break

            if not is_dislike:
                post.dislikes.add(request.user)

            if is_dislike:
                post.dislikes.remove(request.user)

            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)

class UserSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('query')
        profile_list = UserProfile.objects.filter(
            Q(user__username__icontains=query) 
        )
        
        context = {
            'profile_list': profile_list,
        }
        
        return render(request, 'socialapp/search.html', context)
    
class ListFollowers(View):
    def get(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        followers = profile.followers.all()
        
        context = {
            'profile': profile,
            'followers': followers,
        }
        
        return render(request, 'socialapp/followers_list.html', context)

#view for notifications
class PostNotification(View):
    def get(self, request, notification_pk, post_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        post = Post.objects.get(pk=post_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('post_detail', pk=post_pk)
    
class FollowNotification(View):
    def get(self, request, notification_pk, profile_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        profile = UserProfile.objects.get(pk=profile.pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('profile', pk=profile_pk)
    
class RemoveNotification(View):
    def delete(self, request, notification_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        notification.user_has_seen = True
        
        notification.save()

        return HttpResponse('Success', content_type='text/plain')

#view for inboxes    
class ListThreads(View):
    def get(self, request, *args, **kwargs):
        threads = ThreadModel.objects.filter(Q(user=request.user) | Q(receiver=request.user))

        context = {
            'threads': threads
        }

        return render(request, 'socialapp/inbox.html', context)

class CreateThread(View):
    def get(self, request, *args, **kwargs):
        form = ThreadForm()

        context = {
            'form': form
        }

        return render(request, 'socialapp/create_thread.html', context)

    def post(self, request, *args, **kwargs):
        form = ThreadForm(request.POST)

        username = request.POST.get('username')

        try:
            receiver = User.objects.get(username=username)
            if ThreadModel.objects.filter(user=request.user, receiver=receiver).exists():
                thread = ThreadModel.objects.filter(user=request.user, receiver=receiver)[0]
                return redirect('thread', pk=thread.pk)
            elif ThreadModel.objects.filter(user=receiver, receiver=request.user).exists():
                thread = ThreadModel.objects.filter(user=receiver, receiver=request.user)[0]
                return redirect('thread', pk=thread.pk)

            if form.is_valid():
                thread = ThreadModel(
                    user=request.user,
                    receiver=receiver
                )
                thread.save()

                return redirect('thread', pk=thread.pk)
        except:
            return redirect('create-thread')