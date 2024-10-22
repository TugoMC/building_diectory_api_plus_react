from django.utils import timezone
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError



class Professional(models.Model):
    # Informations personnelles
    full_name = models.CharField(max_length=255, verbose_name="Nom complet")
    profile_photo = models.ImageField(
        upload_to="photos/", null=True, blank=True, verbose_name="Photo de profil"
    )
    email = models.EmailField(unique=True, verbose_name="Email", db_index=True)
    phone = models.CharField(max_length=20, verbose_name="Téléphone", db_index=True)

    CITY_CHOICES = [
        ("Abidjan", "Abidjan"),
        ("Yamoussoukro", "Yamoussoukro"),
        ("Bouaké", "Bouaké"),
        ("Daloa", "Daloa"),
        ("San-Pédro", "San-Pédro"),
        ("Korhogo", "Korhogo"),
        ("Gagnoa", "Gagnoa"),
        ("Soubré", "Soubré"),
        ("Man", "Man"),
        ("Anyama", "Anyama"),
        ("Abengourou", "Abengourou"),
        ("Grand-Bassam", "Grand-Bassam"),
        ("Divo", "Divo"),
        ("Agboville", "Agboville"),
        ("Katiola", "Katiola"),
        ("Bondoukou", "Bondoukou"),
        ("Ferkessédougou", "Ferkessédougou"),
        ("Adzopé", "Adzopé"),
        ("Oumé", "Oumé"),
        ("Dabou", "Dabou"),
        ("Sinfra", "Sinfra"),
        ("Bingerville", "Bingerville"),
        ("Duekoué", "Duekoué"),
        ("Dimbokro", "Dimbokro"),
        ("Séguéla", "Séguéla"),
        ("Aboisso", "Aboisso"),
        ("Daoukro", "Daoukro"),
        ("Odienné", "Odienné"),
        ("Bangolo", "Bangolo"),
        ("Biankouma", "Biankouma"),
        ("Sassandra", "Sassandra"),
        ("Bouna", "Bouna"),
        ("Touba", "Touba"),
        ("Zoukougbeu", "Zoukougbeu"),
        ("Bouaflé", "Bouaflé"),
        ("Mankono", "Mankono"),
        ("Kounahiri", "Kounahiri"),
    ]
    
    city = models.CharField(max_length=100, choices=CITY_CHOICES, verbose_name="Ville")

    COMMUNE_CHOICES = [
    ("Abengourou", "Abengourou"),
    ("Abobo", "Abobo"),
    ("Aboisso", "Aboisso"),
    ("Adiaké", "Adiaké"),
    ("Adjamé", "Adjamé"),
    ("Agboville", "Agboville"),
    ("Agnibilékrou", "Agnibilékrou"),
    ("Akoupé", "Akoupé"),
    ("Anyama", "Anyama"),
    ("Arrah", "Arrah"),
    ("Assuéfry", "Assuéfry"),
    ("Attécoubé", "Attécoubé"),
    ("Ayémé", "Ayémé"),
    ("Azaguié", "Azaguié"),
    ("Bako", "Bako"),
    ("Bangolo", "Bangolo"),
    ("Bassawa", "Bassawa"),
    ("Bédiala", "Bédiala"),
    ("Béoumi", "Béoumi"),
    ("Bettié", "Bettié"),
    ("Biankouma", "Biankouma"),
    ("Bingerville", "Bingerville"),
    ("Bin-Houyé", "Bin-Houyé"),
    ("Bloléquin", "Bloléquin"),
    ("Bocanda", "Bocanda"),
    ("Bodokro", "Bodokro"),
    ("Bondoukou", "Bondoukou"),
    ("Bongouanou", "Bongouanou"),
    ("Bonon", "Bonon"),
    ("Bonoua", "Bonoua"),
    ("Booko", "Booko"),
    ("Bouaflé", "Bouaflé"),
    ("Bouaké", "Bouaké"),
    ("Bouna", "Bouna"),
    ("Boundiali", "Boundiali"),
    ("Brobo", "Brobo"),
    ("Buyo", "Buyo"),
    ("Cocody", "Cocody"),
    ("Dabakala", "Dabakala"),
    ("Dabou", "Dabou"),
    ("Daloa", "Daloa"),
    ("Daoukro", "Daoukro"),
    ("Dianra", "Dianra"),
    ("Didiévi", "Didiévi"),
    ("Dimbokro", "Dimbokro"),
    ("Divo", "Divo"),
    ("Djékanou", "Djékanou"),
    ("Djibrosso", "Djibrosso"),
    ("Ferkessédougou", "Ferkessédougou"),
    ("Fresco", "Fresco"),
    ("Grand-Bassam", "Grand-Bassam"),
    ("Guéyo", "Guéyo"),
    ("Guibéroua", "Guibéroua"),
    ("Guiglo", "Guiglo"),
    ("Issia", "Issia"),
    ("Jacqueville", "Jacqueville"),
    ("Kaniasso", "Kaniasso"),
    ("Katiola", "Katiola"),
    ("Kokumbo", "Kokumbo"),
    ("Korhogo", "Korhogo"),
    ("Koumassi", "Koumassi"),
    ("Koumbala", "Koumbala"),
    ("Kouassi-Datékro", "Kouassi-Datékro"),
    ("Kouassi-Kouassikro", "Kouassi-Kouassikro"),
    ("Kouibly", "Kouibly"),
    ("Kouto", "Kouto"),
    ("Lakota", "Lakota"),
    ("Logoualé", "Logoualé"),
    ("Madina-N'Gana", "Madina-N'Gana"),
    ("Man", "Man"),
    ("Mankono", "Mankono"),
    ("Massala", "Massala"),
    ("Mayo", "Mayo"),
    ("M'Bahiakro", "M'Bahiakro"),
    ("M'Batto", "M'Batto"),
    ("Méagui", "Méagui"),
    ("Minignan", "Minignan"),
    ("Morondo", "Morondo"),
    ("Napiéolédougou", "Napiéolédougou"),
    ("Nassian", "Nassian"),
    ("N'Djébonouan", "N'Djébonouan"),
    ("Niablé", "Niablé"),
    ("Niakaramandougou", "Niakaramandougou"),
    ("Niellé", "Niellé"),
    ("Niofoin", "Niofoin"),
    ("Odienné", "Odienné"),
    ("Ouaninou", "Ouaninou"),
    ("Ouellé", "Ouellé"),
    ("Oumé", "Oumé"),
    ("Ouragahio", "Ouragahio"),
    ("Plateau", "Plateau"),
    ("Port-Bouët", "Port-Bouët"),
    ("Prikro", "Prikro"),
    ("Rubino", "Rubino"),
    ("Saïoua", "Saïoua"),
    ("Sakassou", "Sakassou"),
    ("San-Pédro", "San-Pédro"),
    ("Sassandra", "Sassandra"),
    ("Séguéla", "Séguéla"),
    ("Sikensi", "Sikensi"),
    ("Sinématiali", "Sinématiali"),
    ("Sinfra", "Sinfra"),
    ("Sipilou", "Sipilou"),
    ("Sirasso", "Sirasso"),
    ("Songon", "Songon"),
    ("Soubré", "Soubré"),
    ("Taabo", "Taabo"),
    ("Tabou", "Tabou"),
    ("Tafiré", "Tafiré"),
    ("Tanda", "Tanda"),
    ("Téhini", "Téhini"),
    ("Tiapoum", "Tiapoum"),
    ("Tiassalé", "Tiassalé"),
    ("Tiébissou", "Tiébissou"),
    ("Tiémélékro", "Tiémélékro"),
    ("Tié-N'Diékro", "Tié-N'Diékro"),
    ("Tienko", "Tienko"),
    ("Tioroniaradougou", "Tioroniaradougou"),
    ("Touba", "Touba"),
    ("Toulépleu", "Toulépleu"),
    ("Toumodi", "Toumodi"),
    ("Transua", "Transua"),
    ("Treichville", "Treichville"),
]


    commune = models.CharField(
        max_length=100, choices=COMMUNE_CHOICES, verbose_name="Commune"
    )

    presentation_video = models.FileField(
        upload_to="videos/", null=True, blank=True, verbose_name="Vidéo de présentation"
    )

    # Caractéristiques professionnelles
    SPECIALIZATIONS = [
        ("Gros Oeuvre", "Gros Oeuvre"),
        ("Second Oeuvre", "Second Oeuvre"),
        ("Finitions", "Finitions"),
        ("Plomberie", "Plomberie"),
        ("Électricité", "Électricité"),
        (
            "Chauffage, Ventilation et Climatisation (CVC)",
            "Chauffage, Ventilation et Climatisation (CVC)",
        ),
        ("Toiture", "Toiture"),
        ("Menuiserie", "Menuiserie"),
        ("Serrurerie", "Serrurerie"),
        ("Peinture et Décoration", "Peinture et Décoration"),
        ("Plâtrerie", "Plâtrerie"),
        ("Revêtements de Sol et Murs", "Revêtements de Sol et Murs"),
        ("Aménagements Extérieurs", "Aménagements Extérieurs"),
        ("Rénovation et Réhabilitation", "Rénovation et Réhabilitation"),
        ("Isolation Thermique et Acoustique", "Isolation Thermique et Acoustique"),
        ("Éclairage", "Éclairage"),
        ("Sécurité Incendie", "Sécurité Incendie"),
    ]

    specialization = models.CharField(
        max_length=255, choices=SPECIALIZATIONS, verbose_name="Spécialisation"
    )

    class SkillLevel(models.TextChoices):
        DEBUTANT = "Débutant", "Débutant"
        INTERMEDIAIRE = "Intermédiaire", "Intermédiaire"
        EXPERT = "Expert", "Expert"

    skill_level = models.CharField(
        max_length=50,
        choices=SkillLevel.choices,
        verbose_name="Niveau de compétence",
    )

    certifications = models.TextField(verbose_name="Certifications", blank=True)
    years_of_experience = models.PositiveIntegerField(
        help_text="Nombre d'années d'expérience", verbose_name="Années d'expérience"
    )
    daily_rate = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Tarif journalier"
    )
    availability = models.CharField(
        max_length=255,
        help_text="Exemple : Lundi - Vendredi, 9h - 18h",
        verbose_name="Disponibilité",
    )
    identity_verified = models.BooleanField(
        default=False, verbose_name="Identité vérifiée"
    )

    @property
    def display_certifications(self):
        return self.certifications if self.certifications else "Aucune"

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        return (
            reviews.aggregate(models.Avg("rating"))["rating__avg"]
            if reviews.exists()
            else 0
        )

    def is_available(self):
        current_date = timezone.now().date()
        return not self.contracts.filter(
            start_date__lte=current_date, end_date__gte=current_date, status="confirmed"
        ).exists()

    def __str__(self):
        return self.full_name

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["email"], name="unique_email"),
        ]


class Portfolio(models.Model):
    professional = models.ForeignKey(
        Professional, related_name="portfolios", on_delete=models.CASCADE
    )
    project_title = models.CharField(max_length=255)
    project_description = models.TextField()
    project_image = models.ImageField(upload_to='portfolio_images/', blank=True, null=True)

    def __str__(self):
        return self.project_title




class Contract(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contracts")
    professional = models.ForeignKey(
        "Professional", on_delete=models.CASCADE, related_name="contracts"
    )
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)
    STATUS_CHOICES = [
        ("requested", "Demandé"),
        ("confirmed", "Confirmé"),
        ("completed", "Terminé"),
        ("cancelled", "Annulé"),
    ]
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="requested"
    )

    payment_status = models.CharField(
        max_length=20,
        choices=[("pending", "En attente"), ("paid", "Payé")],
        default="pending",
    )

    def is_paid(self):
        return self.payment_status == "paid"

    def __str__(self):
        return (
            f"{self.user} - {self.professional} ({self.start_date} to {self.end_date})"
        )
        
    def mark_as_completed(self):
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save()

    @property
    def can_be_reviewed(self):
        if self.completed_at:
            return timezone.now() < self.completed_at + timezone.timedelta(days=60)
        return False

    @property
    def is_current(self):
        """Returns True if the contract is currently active."""
        # Vérifiez si les dates sont valides
        if self.start_date and self.end_date:
            return self.start_date <= timezone.now().date() <= self.end_date
        return False

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["professional", "status"],
                condition=Q(status="confirmed"),
                name="unique_active_contract",
            ),
        ]


class Review(models.Model):
    professional = models.ForeignKey(Professional, related_name="reviews", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="reviews", on_delete=models.CASCADE)
    contract = models.ForeignKey(Contract, related_name="reviews", on_delete=models.CASCADE, default=None)
    rating = models.IntegerField(null=False, blank=False)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    edit_count = models.PositiveIntegerField(default=0)

    def can_edit(self):
        return self.edit_count < 2

    def __str__(self):
        return f"Review by {self.user.username} on {self.professional}"

    def clean(self):
        if self.rating is None:
            raise ValidationError("Rating cannot be None.")
        if not (1 <= self.rating <= 5):
            raise ValidationError("Rating must be between 1 and 5.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        # Vous pouvez ajouter des contraintes supplémentaires ici si nécessaire
        unique_together = ('user', 'contract')  # Assure qu'un utilisateur ne peut laisser qu'un avis par contrat
        
