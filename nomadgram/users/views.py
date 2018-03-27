from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers
from nomadgram.notifications import views as notification_views

class ExploreUsers(APIView):
    def get(self, request, format=None):
        last_five = models.User.objects.all().order_by('-date_joined')[:5]
        serializer = serializers.ListUserSerailizer(last_five, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class FollowUser(APIView):
    def post(self, request, user_id, format=None):
        try:
            user_to_follow = models.User.objects.get(id=user_id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        request.user.following.add(user_to_follow)
        request.user.save()

        notification_views.create_notification(request.user, user_to_follow, 'follow')
        return Response(status=status.HTTP_200_OK)


class UnFollowUser(APIView):
    def post(self, request, user_id, format=None):
        try:
            user_to_follow = models.User.objects.get(id=user_id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        request.user.following.remove(user_to_follow)
        request.user.save()
        return Response(status=status.HTTP_200_OK)


class UserProfile(APIView):
    def get(self, request, username, format=None):
        try:
            found_user = models.User.objects.get(username=username)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.UserProfileSerializer(found_user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserFollowers(APIView):
    def get(self, request, username, format=None):
        try:
            found_user = models.User.objects.get(username=username)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user_followers = found_user.followers.all()
        serializer = serializers.CountImageSerializer(user_followers, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserFollowing(APIView): # class based view
    def get(self, request, username, format=None):
        try:
            found_user = models.User.objects.get(username=username)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user_following = found_user.following.all()
        serializer = serializers.CountImageSerializer(user_following, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

''' function based view
def UserFollowingFBV(request, username):
    if request.method == 'GET':
        try:
            found_user = models.User.objects.get(username=username)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user_following = found_user.following.all()
        serializer = serializers.ListUserSerailizer(user_following, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
'''


class Search(APIView):
    def get(self, request, format=None):
        username = request.query_params.get('username', None)
        if username is not None:
            users = models.User.objects.filter(username__istartswith=username)

            serializer = serializers.ListUserSerailizer(users, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
