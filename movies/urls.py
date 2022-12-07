from django.urls import path

from .views import MovieView, MovieDetailView, AddReview, ActorView, FilterMovieView, JsonFilterMovieView


urlpatterns = [
    path('', MovieView.as_view()),
    path('filter/', FilterMovieView.as_view(), name='filter'),
    path('json-filter/', JsonFilterMovieView.as_view(), name='json_filter'),
    path('<slug:slug>/', MovieDetailView.as_view(), name='movie_detail'),
    path('review/<int:pk>/', AddReview.as_view(), name='add_review'),
    path('actor/<str:slug>/', ActorView.as_view(), name='actor_detail'),
]
