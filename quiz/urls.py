from quiz import views
from django.urls import include, path

app_name = 'quiz'

urlpatterns = [
    path('start', views.start, name='start'),
    path('start-game/<int:pk>/', views.start_game, name='start-game'),
    path('game/<int:pk>/', views.game, name='game'),
    path('results', views.results, name='reults'),
    path('question', views.question, name='questions'),
    path('player-not-found', views.question, name='player-not-found')

]