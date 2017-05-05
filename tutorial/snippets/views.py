from rest_framework import renderers,viewsets
from copy import deepcopy
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from snippets.models import Snippet,Author
from snippets.serializers import SnippetSerializer,AuthorSerializer,UserSerializer
from rest_framework import generics
from rest_framework.decorators import api_view,detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from rest_framework import permissions
from snippets.permissions import IsOwnerOrReadOnly

@csrf_exempt
def author_list(request):
    """
    List all code authors, or create a new author.
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
    try:
        author = Author.objects.get(pk=pk)
    except Author.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = AuthorSerializer(author)
	return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
	serializer = AuthorSerializer(author, data=data)
	if serializer.is_valid():
	    serializer.save()
	    return JsonResponse(serializer.data)
	return JsonResponse(serializer.errors, status=400)
    
    elif request.method == 'DELETE':
        author.delete()
        return HttpResponse(status=204)


@csrf_exempt
def snippet_detail(request, pk):
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
	return JsonResponse(serializer.data)
    
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
	serializer = SnippetSerializer(snippet, data=data)
	if serializer.is_valid():
	    serializer.save()
	    return JsonResponse(serializer.data)
	return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
	return HttpResponse(status=204)

@csrf_exempt
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
	serializer = SnippetSerializer(data=data)
#	data = {}
#	serializer1 = AuthorSerializer(data=data)
#	if serializer1.is_valid():
#	    serializer1.save()
	if serializer.is_valid():
	    serializer.save()
	    return JsonResponse(serializer.data, status=201)
	return JsonResponse(serializer.errors, status=400)

class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)


@api_view(['GET'])
def api_root(request,format = None):
    return Response({
        'snippets':reverse('snippet-list',request = request,format = format)
	})

class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self,request,*args,**kwargs):
        snippet = self.get_object()
	return Response(snippet.highlighted)

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
