from django.shortcuts import get_object_or_404
from rest_framework import generics
from .serializers import CommentSerializer
from main.models import Board, Post, Comment


class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        board = get_object_or_404(Board, name=self.kwargs['board'])
        post = get_object_or_404(Post, no=self.kwargs['no'], board=board)
        return post.comments.all()

    def perform_create(self, serializer):
        board = get_object_or_404(Board, name=self.kwargs['board'])
        post = get_object_or_404(Post, no=self.kwargs['no'], board=board)
        try:
            parent_no = self.kwargs['parent']
            parent = get_object_or_404(Comment, no=parent_no)
            serializer.save(post=post,parent=parent)
        except KeyError:
            serializer.save(post=post)






