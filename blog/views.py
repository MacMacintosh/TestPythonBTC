from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import DetailView

from .models import Post, Comment
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import PostForm, CommentForm
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import FormView, DeleteView, UpdateView, CreateView


class PostList(CreateView):
    def get(self, request):
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
        return render(request, 'blog/post_list.html', {'posts': posts})


class PostDetail(DetailView):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


class PostDraftList(DeleteView):
    def get(self, request):
        posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
        return render(request, 'blog/post_draft_list.html', {'posts': posts})


class PostPublish(UpdateView):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.publish()
        return redirect('post_detail', pk=pk)


class RemovePost(DeleteView):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return redirect('post_list')


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


class ApproveComment(UpdateView):
    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        comment.approve()
        return redirect('post_detail', pk=comment.post.pk)


class RemoveComment(DeleteView):
    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        return redirect('post_detail', pk=comment.post.pk)
