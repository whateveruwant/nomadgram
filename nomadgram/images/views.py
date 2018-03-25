from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers


def get_created_at(image):
    return image.created_at


class Feed(APIView):
    def get(self, request, format=None):
        user = request.user
        following_users = user.following.all()
        image_list = []
        # print(following_users)
        for following_user in following_users:
            # print(following_user.images.all())
            user_images = following_user.images.all()[:2]
            for image in user_images:
                image_list.append(image)
        # print(image_list)
        sorted_list = sorted(image_list, key=get_created_at, reverse=True)
        # print(sorted_list)
        serializer = serializers.ImageSerializer(sorted_list, many=True)
        return Response(serializer.data)


class LikeImage(APIView):
    def post(self, request, image_id, format=None):
        # print(image_id)
        try:
            found_image = models.Image.objects.get(id=image_id)
        except models.Image.DoesNotExist:
            return Response(status=404)
        
        # print(image)

        try:
            preexisiting_like = models.Like.objects.get(
                creator=request.user,
                image=found_image
            )
            return Response(status=status.HTTP_304_NOT_MODIFIED)
        except models.Like.DoesNotExist:
            new_like = models.Like.objects.create(
                creator=request.user,
                image=found_image
            )
            new_like.save()
            return Response(status=status.HTTP_201_CREATED)


class UnLikeImage(APIView):
    def delete(self, request, image_id, format=None):
        try:
            found_image = models.Image.objects.get(id=image_id)
        except models.Image.DoesNotExist:
            return Response(status=404)

        try:
            preexisiting_like = models.Like.objects.get(
                creator=request.user,
                image=found_image
            )
            preexisiting_like.delete()
            return Response(status=status.HTTP_202_NO_CONTENT)
        except models.Like.DoesNotExist:
            return Response(status=status.HTTP_304_NOT_MODIFIED)

class CommentOnImage(APIView):
    def post(self, request, image_id, format=None):
        # print(request.data)
        try:
            found_image = models.Image.objects.get(id=image_id)
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(creator=request.user, image=found_image)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Comment(APIView):
    def delete(self, request, comment_id, format=None):
        try:
            comment = models.Comment.objects.get(id=comment_id, creator=request.user)
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)