from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path("search/", views.search_questions, name="search"),
    path("reset_votes/", views.reset_votes, name="reset_votes"),
    path("crash/", views.crash, name="crash"),
    path("<int:question_id>/comment/", views.add_comment, name="add_comment"),

]