from .models import Post
from .serializer import PostSerializer
from .postpermission import PostDeletePermission
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status


class PostOperationView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [PostDeletePermission, IsAuthenticated]

    def get(self, request):
        post_id = request.query_params.get('id')
        search_by = request.query_params.get('search')

        if post_id:
            try:
                post = Post.objects.get(pk=post_id)
            except Post.DoesNotExist:
                return Response({"message": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = PostSerializer(post)

            return Response(serializer.data, status=status.HTTP_200_OK)
            
        elif search_by:
            posts = Post.objects.filter(title__contains=search_by)

            serializer = PostSerializer(posts, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Something went worng"}, status=status.HTTP_400_BAD_REQUEST)
        
    def post(self, request):
        data = request.data
        x= request.user.id
        print(x)
        data['author'] = x

        # post_user = User.objects.get(username='admin')

        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request):
        id = request.query_params.get("id")

        try:
            post = Post.objects.get(pk=id)
        except Post.DoesNotExist:
            return Response({"error":"Post does not exist."}, status=status.HTTP_404_NOT_FOUND)
        # Checking user permission to perform this action

        post.delete()

        return Response({"message": "Post deleted"}, status=status.HTTP_200_OK)
