from rest_framework import serializers
from snippets.models import Snippet,Author, LANGUAGE_CHOICES, STYLE_CHOICES
from django.contrib.auth.models import User

class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name = 'snippet-highlight',format = 'html')
    class Meta:
        model = Snippet
	fields = ('url','id','owner','highlight','title', 'code', 'linenos', 'language', 'style') 

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
	fields = ('id','name','age','snippet')

#class AuthorSerializer(serializers.Serializer):
#    id = serializers.IntegerField(read_only = True)
#    name = serializers.CharField(required=False, allow_blank=True, max_length=100)
#    age = serializers.CharField(required=False, allow_blank=True, max_length=100)
#    snippet = SnippetSerializer(required = True)

class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many = True,queryset = Snippet.objects.all())

    class Meta:
         model = User
	 fields = ('id','username','snippets')
