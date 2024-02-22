from django.urls import path,include
from .views import  TrouverModelParId, TrouverTailleurParId, VoterTailleur, ajouter_tailleur, send_message, user_signup, user_login , ImageViewSet, ModelsTenueViewSet, ClientViewSet, TailleurViewSet, CommandeViewSet, RecetteViewSet, DepenseViewSet, CatalogueModel
from rest_framework import routers

# creation des dossier d'image lors de l'enregistrement
router = routers.DefaultRouter()
router.register(r'images', ImageViewSet)
router.register(r'modelstenue', ModelsTenueViewSet)
router.register(r'clients', ClientViewSet)
router.register(r'tailleurs', TailleurViewSet)
router.register(r'commandes', CommandeViewSet)
router.register(r'recettes', RecetteViewSet)
router.register(r'depenses', DepenseViewSet)
router.register(r'tailleurs', TailleurViewSet, basename='tailleur')

# Ici les routes ou endpoints
urlpatterns = [
    #Les routes de login et de signup
    path('signup/', user_signup, name='user_signup'),
    path('signin/', user_login, name='user_login'),
   #path('validate_tailleur/<int:user_id>/', validate_tailleur, name='validate_tailleur'),

    # Les routes de l'image
    path('images/', include(router.urls)),
    path('getallImages/', ImageViewSet.as_view({'get': 'getall'}), name='image-getall'),
    path('getbyid/<int:id>/', ImageViewSet.as_view({'get': 'getbyid'}), name='image-getbyid'),
    path('update/<int:id>/', ImageViewSet.as_view({'put': 'update'}), name='image-update'),
    path('delete/<int:id>/', ImageViewSet.as_view({'delete': 'delete'}), name='image-delete'),

    # Les routes du Models
    path('modelstenue/', include(router.urls)),
    path('getallModels/', ModelsTenueViewSet.as_view({'get': 'getall'}), name='modelstenue-getall'),
    path('getbyid/<int:id>/', ModelsTenueViewSet.as_view({'get': 'getbyid'}), name='modelstenue-getbyid'),
    path('update/<int:id>/', ModelsTenueViewSet.as_view({'put': 'update_custom'}), name='modelstenue-update'),
    path('delete/<int:id>/', ModelsTenueViewSet.as_view({'delete': 'delete'}), name='modelstenue-delete'),

    #Les routes du client
    path('clients/getall/', ClientViewSet.as_view({'get': 'getall'}), name='client-getall'),
    path('getbyid/<int:id>/', ClientViewSet.as_view({'get': 'getbyid'}), name='client-getbyid'),
    path('update/<int:id>/', ClientViewSet.as_view({'put': 'update_custom'}), name='client-update'),
    path('delete/<int:id>/', ClientViewSet.as_view({'delete': 'delete_custom'}), name='client-delete'),
    path('clients/tailleurs/<int:id>/', TrouverTailleurParId.as_view(), name='trouver_tailleur_par_id'),
    path('models_tenue/<int:id>/', TrouverModelParId.as_view(), name='trouver_model_tenue_par_id'),
    path('tailleurs/<int:tailleur_id>/voter/', VoterTailleur.as_view(), name='voter_tailleur'),
    path('addTailleurToMyList/<int:tailor_id>/', ajouter_tailleur, name='addTailleur'),

    #Les routes du Tailleur
    path('tailleurs/', TailleurViewSet.as_view({'get': 'getAllTailleur'}), name= 'tailleur-getall'),
    path('createcatalogue/', CatalogueModel.as_view(), name='creerCatalogueModels'),
    path('addClientToList/<int:client_id>/', TailleurViewSet.as_view({'get': 'ajouter_client'}), name='addCilent'),

    # Les routes
    path('commandes/get-client-orders/', CommandeViewSet.as_view({'get': 'get_client_orders'}), name='client-orders'),
    path('commandes/<int:id>/getcommandbyid/', CommandeViewSet.as_view({'get': 'getcommandbyid'}), name='get-command-by-id'),
    path('commandes/<int:id>/delete_custom/', CommandeViewSet.as_view({'delete': 'delete_custom'}), name='delete-command'),

    # La recette
    path('recettes/getall/', RecetteViewSet.as_view({'get':'getall'}), name='tailleur-recette'),

    # La depense
    path('depenses/getall', DepenseViewSet.as_view({'get': 'getall'}), name='tailleur_depenses'),

    # Envoie de message
    path('send-message/<int:recipient_id>/', send_message, name='send_message'),
]
