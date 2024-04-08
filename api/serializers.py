from rest_framework import serializers, generics
from .models import CustomUser, Image, Message, ModelsTenue, Client, Tailleur, Commande, Recette, Depense, Catalogue

# Serialiser du l'user
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

# Serialiser de l'image
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'
        
# Serialiser de la Modeles
class ModelsTenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelsTenue
        fields = '__all__'

# Serialiser du Client
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

# Serialiser du Tailleur
class TailleurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tailleur
        fields = '__all__'


class CatalogueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalogue
        fields = '__all__'
# Serialiser de la commade
class CommandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commande
        fields = '__all__'

# Serialiser de la Recette
class RecetteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recette
        fields = '__all__'

# Serialiser de la recette
class DepenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Depense
        fields = '__all__'

class TailleurInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tailleur
        fields = ['nom','nom_atellier','adresse','tel']

class ModelsInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelsTenue
        fields = ['nom', 'description', 'categorie', 'temps_execution', 'prix']

class VoterTailleurSerializer(serializers.Serializer):
    votes = serializers.IntegerField()

# Le serializer du message
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'recipient', 'content', 'timestamp', 'is_read']

