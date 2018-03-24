from rest_framework.views import APIView
from rest_framework.response import Response
from . import models, serializers

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

def get_created_at(image):
    return image.created_at