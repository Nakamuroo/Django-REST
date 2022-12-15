from django.urls import path, include
from . import views

urlpatterns = [
    path(r'auth/', include('rest_framework.urls')),
    # path(r'auth/', include('djoser.urls.authtoken')),

    path('books/create/', views.BookCreate.as_view()),
    path('books/', views.BookListView.as_view()),
    path('books/<int:pk>/', views.book_detail),
    path('books/update/<int:pk>/', views.BookUpdate.as_view()),

    path('authors/', views.author_list.as_view()),
    path('authors/create/', views.AuthorCreate.as_view()),
    path('authors/<int:pk>/', views.AuthorDetail.as_view()),
]
