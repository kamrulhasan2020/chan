from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from .models import Board, Post


class HomeView(ListView):
    model = Board
    template_name = 'main/home.html'
    context_object_name = 'Boards'


class BoardView(ListView):
    model = Post
    template_name = 'main/board.html'
    context_object_name = 'Posts'

    def get_queryset(self):
        board_name = self.kwargs['board']
        self.board = get_object_or_404(Board, name=board_name)
        return self.board.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['board'] = self.board
        return context


class PostView(DetailView):
    model = Post
    context_object_name = 'Post'
    template_name = 'main/post.html'

    def get_object(self):
        board = get_object_or_404(Board, name=self.kwargs['board'])
        self.post = get_object_or_404(Post, no=self.kwargs['no'], board=board)
        return self.post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Comments'] = self.post.comments.all()
        return context

