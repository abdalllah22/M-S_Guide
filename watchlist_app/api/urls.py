from django.urls import path , include
from rest_framework.routers import DefaultRouter


# from watchlist_app.api.views import movie_details, movie_list
from watchlist_app.api.views import (WatchListAV, WatchDetailAV, 
                                    StreamPlatformAV, StreamPlatformDetailAV,
                                    ReviewList, ReviewDetail, ReviewCreate,
                                    StreamPlatformVS)

router = DefaultRouter()
router.register('stream', StreamPlatformVS, basename='streamplatform')

urlpatterns = [
    path('list/', WatchListAV.as_view(), name='movie-list' ),
    path('<int:pk>', WatchDetailAV.as_view(), name='movie-details' ),
    
    # path('stream/', StreamPlatformAV.as_view(), name='stream-list' ),
    # path('stream/<int:pk>', StreamPlatformDetailAV.as_view(), name='stream-detail' ),
    path('', include(router.urls)),
    
    
    # path('review', ReviewList.as_view(), name='review-list' ),
    # path('review/<int:pk>', ReviewDetail.as_view(), name='review-detail' ),
    
    path('stream/<int:pk>/review-create', ReviewCreate.as_view(), name='review-create' ),
    path('stream/<int:pk>/review', ReviewList.as_view(), name='review-list' ),
    path('stream/review/<int:pk>', ReviewDetail.as_view(), name='review-detail' ),
    
    
]