from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login
from rest_framework import status, viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes,action
from rest_framework.permissions import AllowAny
from .models import CustomUser, Image, ModelsTenue, Client, Tailleur, Commande, Recette, Depense, Catalogue
from .serializers import CustomUserSerializer, ImageSerializer, MessageSerializer, ModelsInfoSerializer, ModelsTenueSerializer, ClientSerializer, TailleurSerializer, CommandeSerializer, RecetteSerializer, DepenseSerializer, CatalogueSerializer, TailleurInfoSerializer, VoterTailleurSerializer
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login
from datetime import timedelta
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser, Client
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import user_passes_test

# La fonction utilise des décorateurs et fait la création de comptes
@api_view(['POST'])
#@permission_classes([AllowAny])
def user_signup(request):
    serializer = CustomUserSerializer(data=request.data)
    print("La donnee est ", request.data)
    if serializer.is_valid():
        user = serializer.save()
       # response_data['pass'] = user.password
        response_data = {'message': "User saved successfully"}
        
        # Générer le token
        refresh = RefreshToken.for_user(user)
        response_data['access_token'] = str(refresh.access_token)
        print('Le token est : ', response_data['access_token'])

        # Récupérer l'attribut idRoles
        id_roles = user.idRoles

        # Créer une réponse personnalisée en fonction de idRoles
        if id_roles == 2:
            user.is_valid = False
            user.save()
            # Si idRoles est 2, c'est un client
            response_data = {
                'user': {
                'id': user.id,
                'lastname': user.lastname,
                'firstname': user.firstname,
                }
            }
            response_data['catalogue'] = {
                'model_favoris': Client.modelfavoris.objects.filter(idClient=user.id).values(),  # Remplacez ModelFavoris par le vrai lastname du modèle
                'mesuration': Client.mesuration.objects.filter(idUser=user).values(),  # Remplacez Mesuration par le vrai lastname du modèle
                'liste_tailleurs': user.liste_tailleurs.all().values(),  # Exemple pour récupérer la liste de tailleurs
            }
        elif id_roles == 1:
            # Si idRoles est 1, c'est un tailleur
            user.is_approved = False
            user.save()

            response_data['user'] = {
                'id': user.id,
                'lastname': user.lastname,
                'firstname': user.firstname,
                
            }
            response_data['catalogue'] = {
                'liste_clients': user.liste_clients.all().values(),  # Exemple pour récupérer la liste de clients
            }

        return Response(response_data, status=status.HTTP_201_CREATED)
    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# La fonction utilise des décorateurs et fait la connexion
@api_view(['POST'])
#@permission_classes([AllowAny])
def user_login(request):
    print(request.data)

    CLIENT_ROLE = 2
    TAILLEUR_ROLE = 1

    tel = request.data.get('phoneNumber')
    password = request.data.get('password')

    user = get_object_or_404(CustomUser, phoneNumber=tel)
    stored_password = user.password 

    # Vérifier le mot de passe
    verified = password == stored_password

    print("Le mot de passe stocké : ", stored_password)

    if verified:
        login(request, user)
        refresh = RefreshToken.for_user(user)
        refresh.access_token.set_exp(lifetime=timedelta(seconds=3600))

        response_data = {
            'access_token': str(refresh.access_token),
            'user': {
                'id': user.id,
                'lastname': user.lastname,
                'firstname': user.firstname,
                'phone' :user.phoneNumber,
                'adresse': user.address,
                'genre': user.gender,
                'email' : user.email,
                'birthday': user.birthday
            },
            'message': f"{user.lastname} {user.firstname} is connected "
        }

        # Récupérer l'attribut idRoles
        id_roles = user.idRoles

        # Créer une réponse personnalisée en fonction de idRoles
        if id_roles == CLIENT_ROLE:
            # Si idRoles est 2, c'est un client
            response_data['info_client'] = {
                'model_favoris': Client.modelfavoris.objects.filter(idClient=user.id).values(),
                'mesuration': Client.mesuration.objects.filter(idUser=user.id).values(),
                'liste_tailleurs': user.liste_tailleurs.all().values(),
            }
        elif id_roles == TAILLEUR_ROLE:
            # Si idRoles est 1, c'est un tailleur
            response_data['info_tailleur'] = {
                'liste_clients': user.liste_clients.all().values(),
                'address': user.address,
            }

        return JsonResponse(response_data, status=status.HTTP_200_OK)

    return JsonResponse({"message": "Échec de connexion"}, status=status.HTTP_401_UNAUTHORIZED)

def getAllPosition(role_id):
   users = CustomUser.objects.filter(idRoles=role_id)
   position = [user.address for user in users]
   return position


# La vue de l'image
class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    @action(detail=False, methods=['GET'])
    def getall(self, request):
        # Récupérer toutes les images
        images = self.queryset
        serializer = self.serializer_class(images, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'])
    def getbyid(self, request, id=None):
        # Récupérer une image par son ID
        image = self.get_object()
        serializer = self.serializer_class(image)
        return Response(serializer.data)

   # @action(detail=True, methods=['PUT'])
    def update(self, request, id=None):
        # Mettre à jour une image par son ID
        image = self.get_object()
        serializer = self.serializer_class(image, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_BAD_REQUEST)

    @action(detail=True, methods=['DELETE'])
    def delete(self, request, id=None):
        # Supprimer une image par son ID
        image = self.get_object()
        image.delete()
        return Response({'message': 'Image supprimée avec succès'}, status=status.HTTP_NO_CONTENT)



class ImageCreateView(APIView):
    def post(self, request, format=None):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            image_file = request.data.get('image_file')

            # Vérification de l'extension du fichier
            allowed_extensions = ('.jpg', '.jpeg', '.png', '.gif')
            if not image_file.name.lower().endswith(allowed_extensions):
                return Response({'message': 'Seules les extensions JPG, JPEG, PNG et GIF sont autorisées.'}, status=status.HTTP_BAD_REQUEST)

            # Vérification de la taille du fichier (10 Mo maximum)
            if image_file.size > 10 * 1024 * 1024:  # 10 Mo en octets
                return Response({'message': 'La taille du fichier ne peut pas dépasser 10 Mo.'}, status=status.HTTP_BAD_REQUEST)

            # Si les vérifications passent, sauvegardez l'image
            serializer.save()
            return Response(serializer.data, status=status.HTTP_CREATED)

        return Response(serializer.errors, status=status.HTTP_BAD_REQUEST)

# La vue de la Modele
class ModelsTenueViewSet(viewsets.ModelViewSet):
    queryset = ModelsTenue.objects.all()
    serializer_class = ModelsTenueSerializer

    @action(detail=False, methods=['GET'])
    def getall(self, request):
        # Récupérer toutes les tenues (modèles)
        tenues = self.queryset
        serializer = self.serializer_class(tenues, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'])
    def getbyid(self, request, id=None):
        # Récupérer une tenue (modèle) par son ID
        tenue = self.get_object()
        serializer = self.serializer_class(tenue)
        return Response(serializer.data)

    @action(detail=True, methods=['PUT'])
    def update_custom(self, request, id=None):
        # Mettre à jour une tenue (modèle) par son ID
        tenue = self.get_object()
        serializer = self.serializer_class(tenue, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_BAD_REQUEST)

    @action(detail=True, methods=['DELETE'])
    def delete(self, request, id=None):
        # Supprimer une tenue (modèle) par son ID
        tenue = self.get_object()
        tenue.delete()
        return Response({'message': 'Tenue supprimée avec succès'}, status=status.HTTP_NO_CONTENT)
    

# La vue du client
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    @action(detail=True, methods=['GET'])
    def getbyid(self, request, id=None):
        client = self.get_object()
        serializer = self.serializer_class(client)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def getall(self, request):
        clients = self.queryset
        serializer = self.serializer_class(clients, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['PUT'])
    def update_custom(self, request, id=None):
        client = self.get_object()
        serializer = self.serializer_class(client, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['DELETE'])
    def delete_custom(self, request, id=None):
        client = self.get_object()
        client.delete()
        return Response({'message': 'Client supprimé avec succès'}, status=status.HTTP_204_NO_CONTENT)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import CustomUser

# Ajoute du tailleur à la liste des taileur chez le client
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ajouter_tailleur(request):
    try:
        client = request.user
        tailleur_id = request.data.get('tailleur_id')
        tailleur = CustomUser.objects.get(id=tailleur_id, idRoles=1)  # Assurez-vous que l'utilisateur est un tailleur

        # Vérifiez si le tailleur est déjà dans la liste du client
        if client.liste_tailleurs.filter(id=tailleur_id).exists():
            return Response({"message": "Le tailleur est déjà dans votre liste."}, status=status.HTTP_400_BAD_REQUEST)

        # Ajoutez le tailleur à la liste du client
        client.liste_tailleurs.add(tailleur)
        client.save()

        return Response({"message": "Le tailleur a été ajouté à votre liste avec succès."}, status=status.HTTP_201_CREATED)

    except CustomUser.DoesNotExist:
        return Response({"message": "Le tailleur n'existe pas."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# La vue du Tailleur
class TailleurViewSet(viewsets.ModelViewSet):
    queryset = Tailleur.objects.all()
    serializer_class = TailleurSerializer

    #Les 4 fonctions qui suivent sont le CRUD du Tailleur
    @action(detail=True, methods=['GET'])
    def getTaillerById(self, request, id=None):
        tailleur = self.get_object()
        serializer = self.serializer_class(tailleur)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def getAllTailleur(self,request):
        tailleur = self.queryset
        serializer = self.serializer_class(tailleur, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['PUT'])
    def updateTailleur(self, request, id=None):
        tailleur = self.get_object()
        serializer = self.serializer_class(tailleur, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['DELETE'])
    def deleteTailleur(self, request, id=None):
        tailleur = self.get_object()
        tailleur.delete()
        return Response({'message': 'Tailleur supprimé avec succès'}, status=status.HTTP_NO_CONTENT)

    # creation du catalogue par le tailleur
    @api_view(['POST'])
    def creerCatalogue(request):
        serializer = ModelsTenueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Ajouter client à la liste des client 
    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def ajouter_client(request, client_id):
        try:
            client = CustomUser.objects.get(id=client_id, idRoles=2)  # Vérifier que l'utilisateur est un client
            tailor = request.user  # Le tailleur est l'utilisateur authentifié

            # Vérifier si le client est déjà dans la liste du tailleur
            if client in tailor.liste_clients.all():
                return Response({"message": "Le client est déjà dans votre liste"}, status=status.HTTP_400_BAD_REQUEST)

            # Ajouter le client à la liste du tailleur
            tailor.liste_clients.add(client)
            return Response({"message": "Le client a été ajouté à votre liste"}, status=status.HTTP_201_CREATED)

        except CustomUser.DoesNotExist:
            return Response({"message": "Client non trouvé"}, status=status.HTTP_404_NOT_FOUND) 
        
    # Fonction pour la création d'un catalogue avec choix d'image
    @api_view(['POST'])
    @permission_classes([IsAuthenticated])  # Assurez-vous que le tailleur est authentifié
    def creer_catalogue_avec_image(request):
        # Récupérer les données de la requête
        model_id = request.data.get('model_id', None)
        description = request.data.get('description', '')

        # Vérifier si le modèle existe
        try:
            model_tenue = ModelsTenue.objects.get(pk=model_id)
        except ModelsTenue.DoesNotExist:
            return Response({"message": "Le modèle spécifié n'existe pas"}, status=status.HTTP_404_NOT_FOUND)

        # Créer le catalogue
        catalogue_data = {
            'tailleur': request.user.id,
            'name': model_tenue.name,
            'description': description,
            'idImage': model_tenue.image.id,
        }
        serializer = CatalogueSerializer(data=catalogue_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# La vue du catalogue
class CatalogueModel(generics.CreateAPIView):
    queryset = Catalogue.objects.all()
    serializer_class = CatalogueSerializer

    @action(detail=False, methods=['POST'])
    def creer_catalogue(self, request):
        serializer = CatalogueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(tailleur=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

# La vue de la commande
class CommandeViewSet(viewsets.ModelViewSet):
    queryset = Commande.objects.all()
    serializer_class = CommandeSerializer

    @action(detail=False, methods=['GET'])
    def get_client_orders(self, request):
        user = self.request.user
        client_orders = Commande.objects.filter(idClient=user)
        serializer = self.serializer_class(client_orders, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['PUT'])
    def update_custom(self, request, id=None):
        commande = self.get_object()
        serializer = self.serializer_class(commande, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_BAD_REQUEST)
    
    @action(detail=True, methods=['GET'])
    def getcommandbyid(self, request, id=None):
        commande = self.get_object()
        serializer = self.serializer_class(commande)
        return Response(serializer.data)

    @action(detail=True, methods=['DELETE'])
    def delete_custom(self, request, id=None):
        commande = self.get_object()
        commande.delete()
        return Response({'message': 'Commande supprimée avec succès'}, status=status.HTTP_NO_CONTENT)



# La vue de la recette
class RecetteViewSet(viewsets.ModelViewSet):
    queryset = Recette.objects.all()
    serializer_class = RecetteSerializer

    @action(detail=False, methods=['GET'])
    def getall(self, request):
        recettes = Recette.objects.all()
        serializer = self.serializer_class(recettes, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['POST'])
    def enregistrerRecette(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def voirRecette(self, request):
        recette = Recette.objects.all()
        serializer = self.serializer_class(recette, many=True)
        return Response(serializer.data)


# La vue de la dépense
class DepenseViewSet(viewsets.ModelViewSet):

    queryset = Depense.objects.all()
    serializer_class = DepenseSerializer

    @action(detail=False, methods=['POST'])
    def enregistrerDepense(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def voirDepense(self, request):
        depenses = Depense.objects.all()
        serializer = self.serializer_class(depenses, many=True)
        return Response(serializer.data)
    
class TrouverTailleurParId(generics.RetrieveAPIView):
    queryset = Tailleur.objects.all()
    serializer_class = TailleurInfoSerializer
    lookup_field = 'id'

class TrouverModelParId(generics.RetrieveAPIView):

    queryset = ModelsTenue.objects.all()
    serializer_class = ModelsInfoSerializer
    lookup_field = 'id'

class VoterTailleur(APIView):
    def put(self, request, tailleur_id):
        try:
            tailleur = Tailleur.objects.get(id=tailleur_id)
        except Tailleur.DoesNotExist:
            return Response({"message": "Tailleur non trouvé"}, status=status.HTTP_404_NOT_FOUND)

        serializer = VoterTailleurSerializer(data=request.data)
        if serializer.is_valid():
            votes = serializer.validated_data['votes']
            tailleur.votes += votes
            tailleur.save()
            return Response({"message": f"Votes mis à jour pour le tailleur {tailleur.lastname}"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# 
# views.py

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request, recipient_id):
    try:
        recipient = CustomUser.objects.get(id=recipient_id)

        # Vérifiez si le destinataire est dans la liste appropriée
        if request.user.is_tailleur and recipient in request.user.clients.all():
            # Le tailleur ne peut envoyer un message qu'à un client de sa liste
            serializer = MessageSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save(sender=request.user, recipient=recipient)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.user.is_client and recipient in request.user.tailleurs.all():
            # Le client ne peut envoyer un message qu'à un tailleur de sa liste
            serializer = MessageSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save(sender=request.user, recipient=recipient)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Destinataire non autorisé"}, status=status.HTTP_403_FORBIDDEN)

    except CustomUser.DoesNotExist:
        return Response({"message": "Destinataire non trouvé"}, status=status.HTTP_404_NOT_FOUND)
