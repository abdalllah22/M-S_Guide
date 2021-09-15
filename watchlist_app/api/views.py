from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets

from rest_framework.response import Response
from rest_framework import status 

from watchlist_app.models import WatchList, StreamPlatform, Review
from watchlist_app.api.serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer



class StreamPlatformVS(viewsets.ModelViewSet):
    serializer_class = StreamPlatformSerializer
    queryset = StreamPlatform.objects.all()
    

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


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        movie = WatchList.objects.get(pk=pk)

        serializer.save(WatchList = movie)


class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(WatchList=pk)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


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
    def get(self, request):
        platform = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platform, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StreamPlatformSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class StreamPlatformDetailAV(APIView):
    def get(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk= pk)
        except StreamPlatform.DoesNotExist:
            return Response({
                'message': 'Platform not found',
            },status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(platform)
        return Response(serializer.data)
    
    def put(self, request, pk):
        platform = StreamPlatform.objects.get(pk= pk)
        serializer = StreamPlatformSerializer(platform, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        platform = StreamPlatform.objects.get(pk= pk)
        platform.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)

class WatchListAV(APIView):

    def get(self, request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WatchListSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class WatchDetailAV(APIView):
    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk= pk)
        except WatchList.DoesNotExist:
            return Response({
                'message': 'Movie not found',
            },status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)
    
    def put(self, request, pk):
        movie = WatchList.objects.get(pk= pk)
        serializer = WatchListSerializer(movie,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        movie = WatchList.objects.get(pk= pk)
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