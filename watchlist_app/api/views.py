from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets

from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status 
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
#from django_filters import rest_framework as filters
from rest_framework import filters

from watchlist_app import models 
from watchlist_app.api import serializers 
from watchlist_app.api import permissions 
from watchlist_app.api import throttling 
from watchlist_app.api import pagination 

class StreamPlatformVS(viewsets.ModelViewSet):
    serializer_class = serializers.StreamPlatformSerializer
    queryset = models.StreamPlatform.objects.all()
    permission_classes = [permissions.IsAdminOrReadOnly]
    

# class StreamPlatformVS(viewsets.ViewSet):
    
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(watchlist)
#         return Response(serializer.data)
    
#     def create(self, request):
#         serializer = StreamPlatformSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

class UserReview(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    # permission_classes = [IsAuthenticated,]
    # throttle_classes = [ReviewListThrottle,AnonRateThrottle]

    # def get_queryset(self):      # http://127.0.0.1:8000/watch/reviews/abdalllah22
    #     username = self.kwargs['username']
    #     return Review.objects.filter(review_user__username=username)

    def get_queryset(self):      # http://127.0.0.1:8000/watch/reviews/?username=abdalllah22
        username = self.request.query_params.get('username', None)
        return models.Review.objects.filter(review_user__username=username)


class ReviewCreate(generics.CreateAPIView):
    serializer_class =  serializers.ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ throttling.ReviewCreateThrottle]

    def get_queryset(self):
        return models.Review.objects.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        movie = models.WatchList.objects.get(pk=pk)

        review_user = self.request.user
        review_queryset = models.Review.objects.filter(WatchList= movie, review_user=review_user )

        if review_queryset.exists():
            raise ValidationError("You have already reviewed this movie")

        if movie.number_rating == 0:
            movie.avg_rating = serializer.validated_data['rating']
        else:
            movie.avg_rating = (movie.avg_rating + serializer.validated_data['rating'] )/2
        
        movie.number_rating = movie.number_rating + 1
        movie.save()
        
        serializer.save(WatchList = movie, review_user=review_user)

class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    permission_classes = [IsAuthenticated,]
    throttle_classes = [throttling.ReviewListThrottle,AnonRateThrottle]
    # filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['review_user__username', 'active']

    def get_queryset(self):
        pk = self.kwargs['pk']
        return models.Review.objects.filter(WatchList=pk)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    permission_classes = [permissions.ReviewUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle] # this is to make throttle in one file instaed of two files
    throttle_scope = 'review-detail'

# class ReviewList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

# class ReviewDetail(mixins.RetrieveModelMixin,
#                   mixins.UpdateModelMixin,
#                   mixins.DestroyModelMixin,
#                   generics.GenericAPIView):

#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def patch(self, request, *args, **kwargs):
#         return self.partial_update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs) 
    


class StreamPlatformAV(APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]

    def get(self, request):
        platform = models.StreamPlatform.objects.all()
        serializer = serializers.StreamPlatformSerializer(platform, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.StreamPlatformSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class StreamPlatformDetailAV(APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            platform = models.StreamPlatform.objects.get(pk= pk)
        except models.StreamPlatform.DoesNotExist:
            return Response({
                'message': 'Platform not found',
            },status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.StreamPlatformSerializer(platform)
        return Response(serializer.data)
    
    def put(self, request, pk):
        platform = models.StreamPlatform.objects.get(pk= pk)
        serializer = serializers.StreamPlatformSerializer(platform, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        platform = models.StreamPlatform.objects.get(pk= pk)
        platform.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)

class WatchListGV(generics.ListAPIView):
    queryset = models.WatchList.objects.all()
    serializer_class = serializers.WatchListSerializer
    
    # pagination_class = pagination.WatchListPagination
    pagination_class = pagination.WatchListLOPagination
    # pagination_class = pagination.WatchListCPagination     # return regrad to created filed


    # permission_classes = [IsAuthenticated,]
    
    # filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['title', 'platform__name']

    # filter_backends = [filters.SearchFilter]
    # search_fields = ['title', 'platform__name']

    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['avg_rating']

    
    

class WatchListAV(APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]

    def get(self, request):
        movies = models.WatchList.objects.all()
        serializer = serializers.WatchListSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.WatchListSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class WatchDetailAV(APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]
    
    def get(self, request, pk):
        try:
            movie = models.WatchList.objects.get(pk= pk)
        except models.WatchList.DoesNotExist:
            return Response({
                'message': 'Movie not found',
            },status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.WatchListSerializer(movie)
        return Response(serializer.data)
    
    def put(self, request, pk):
        movie = models.WatchList.objects.get(pk= pk)
        serializer = serializers.WatchListSerializer(movie,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        movie = models.WatchList.objects.get(pk= pk)
        movie.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)











# @api_view(['GET','POST'])
# def movie_list(request):
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data)

#     if request.method == 'POST':
#         serializer = MovieSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)



# @api_view(['GET','DELETE','PUT'])
# def movie_details(request, pk):
#     if request.method == 'GET':
#         try:
#             movie = Movie.objects.get(pk= pk)
#         except Movie.DoesNotExist:
#             return Response({
#                 'message': 'Movie not found',
#             },status=status.HTTP_404_NOT_FOUND)
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)
    
#     if request.method == 'PUT':
#         movie = Movie.objects.get(pk= pk)
#         serializer = MovieSerializer(movie,data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     if request.method == 'DELETE':
#         movie = Movie.objects.get(pk= pk)
#         movie.delete()
#         return Response(status= status.HTTP_204_NO_CONTENT)