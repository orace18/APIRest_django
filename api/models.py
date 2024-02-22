from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from argon2 import PasswordHasher

# Model pour le role
class Role(models.Model):
    type = models.CharField(max_length=255)

# Model pour le constructeur
class CustomUserManager(BaseUserManager):
    def create_user(self, phoneNumber, password, idRoles, email, birthday, address, gender, lastname, firstname):
        role = Role.objects.get(id=idRoles)
        user = self.model(
            phoneNumber=phoneNumber,
            idRoles=role,
            email=email,
            birthday=birthday,
            address=address,
            gender=gender,
            lastname=lastname,
            firstname=firstname,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
# Creation d'un superuser mais on a pas besoins de ça vraiment
    def create_superuser(self, phoneNumber, password, idRoles, email, birthday, address, gender, lastname, firstname):
        role = Role.objects.get(id=idRoles)
        user = self.create_user(
            phoneNumber=phoneNumber,
            password=password,
            idRoles=role,
            email=email,
            birthday=birthday,
            address=address,
            gender=gender,
            lastname=lastname,
            firstname=firstname,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user 

# Model de l'utilisateur
class CustomUser(AbstractBaseUser):
    phoneNumber = models.CharField(max_length=255, unique=True)
    idRoles = models.ForeignKey(Role, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255)
    birthday = models.DateField()
    address = models.JSONField()
    gender = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    firstname = models.CharField(max_length=255)
    is_valid = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phoneNumber'
    REQUIRED_FIELDS = ['idRoles', 'email', 'birthday', 'address', 'gender', 'lastname', 'firstname']

# Definition de la classe pour gérer tout ce qui concerne le mot de passe
class CustomUserPasswordHasher(PasswordHasher):
    def verify(self, encoded, password):
        return super().verify(encoded, password)

    def encode(self, password):
        return super().hash(password)

    def must_update(self, encoded):
        return super().check_needs_rehash(encoded)
    
# Model de l'image
class Image(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    categorie = models.CharField(max_length=50)
    image_file = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name

# Model de la Modele
class ModelsTenue(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ForeignKey(Image, on_delete=models.CASCADE)  # Relation avec le modèle Image
    categorie = models.CharField(max_length=50)
    temps_execution = models.CharField(max_length=50) # Stocke la durée en jours (peut être obtenue en heures ou minutes)
    prix = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

# Model du client
class Client(models.Model):
    id = models.AutoField(primary_key=True)
    idUser = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Supposons que vous avez un modèle User pour les utilisateurs
    mesuration = models.CharField(max_length=255)
    modelfavoris = models.ManyToManyField(ModelsTenue)

    def __str__(self):
        return self.idUser.id  # Ou tout autre champ que vous souhaitez afficher

# Model du Tailleur
class Tailleur(models.Model):
    id = models.AutoField(primary_key=True)
    idUser = models.CharField(max_length=255)
    nomAtelier = models.CharField(max_length=255)
    Adresse = models.CharField(max_length=255)
    competance = models.CharField(max_length=255)
    catalogueModel = models.ManyToManyField(ModelsTenue)
    votes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nomAtelier

# Model pour la création de catalogue
class Catalogue(models.Model):

    tailleur = models.ForeignKey(Tailleur, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    idImage = models.ForeignKey(Image,on_delete=models.CASCADE)
    # Autres champs de votre modèle

    def __str__(self):
        return self.name

# Model de la commande
class Commande(models.Model):
    idClient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='commandes_client')
    etat = models.CharField(max_length=255)
    dateCommande = models.DateField()
    dateLivraison = models.DateField()
    cout = models.DecimalField(max_digits=10, decimal_places=2)
    titre = models.CharField(max_length=255)
    idModel = models.ForeignKey(ModelsTenue, on_delete=models.CASCADE)
    idTailleur = models.ForeignKey(Tailleur, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.titre

# Model de la recette
class Recette(models.Model):
    idTailleur = models.ForeignKey(Tailleur, on_delete=models.CASCADE)
    objet = models.CharField(max_length=255)
    recetteMontant = models.CharField(max_length=255)
    recetteDate = models.DateField()

    def __str__(self):
        return self.objet

# Model de la depense
class Depense(models.Model):
    idTailleur = models.ForeignKey(Tailleur, on_delete=models.CASCADE)
    objet = models.CharField(max_length=255)
    depenseMontant = models.CharField(max_length=255)
    depenseDate = models.DateField()

    def __str__(self):
        return self.objet
    
# Performence des models par rapport à un tailleur pour une année
class Performance(models.Model):
    tailleur = models.ForeignKey(Tailleur, on_delete=models.CASCADE)
    mois_annee = models.DateField()
    tenues_confectionnees = models.PositiveIntegerField()
    argent_genere = models.DecimalField(max_digits=10, decimal_places=2)
    clients_rentables = models.ManyToManyField(Client)
    models_vogues = models.ManyToManyField(ModelsTenue)

    def __str__(self):
        return f"Performance de {self.tailleur} pour {self.mois_annee}"

class Vote(models.Model):
    tailleur = models.ForeignKey(Tailleur, on_delete=models.CASCADE)
    is_voted = models.BooleanField()
    nbr_etoile = models.IntegerField()

    def __str__(self):
        return f'Le tailleur {self.tailleur} est voté avec {self.nbr_etoile}'

# Model du message
class Message(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(CustomUser, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

# M V T