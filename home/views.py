from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser, FileUploadParser
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
import rest_framework.permissions
from rest_framework.authtoken.models import Token

from .models import Book, Author, User
from .serializers import BookSerializer, AuthorSerializer, UserSerializer


class BookCreate(generics.ListCreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    queryset = Book.objects.all()
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = BookSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class BookUpdate(generics.UpdateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    queryset = Book.objects.all()
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = BookSerializer


class AuthorCreate(generics.ListCreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    queryset = Author.objects.all()
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = AuthorSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class BookListView(generics.ListAPIView):
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author__name', 'title', 'genre']

    def get_queryset(self):
        return Book.objects.all()


@csrf_exempt
def book_detail(request, pk):
    """
    Retrieve, update or delete a code book.
    """
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = BookSerializer(book)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = BookSerializer(book, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        book.delete()
        return HttpResponse(status=204)


@csrf_exempt
def author_list(request):
    """
    List all code books, or create a new book.
    """
    if request.method == 'GET':
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = AuthorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def author_detail(request, pk):
    """
    Retrieve, update or delete a code book.
    """
    try:
        author = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = BookSerializer(author)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = BookSerializer(author, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        author.delete()
        return HttpResponse(status=204)
