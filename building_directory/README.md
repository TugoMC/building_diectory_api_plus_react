Application Web de Gestion des Contrats Professionnels
Cette application web permet de gérer efficacement les contrats avec des professionnels de divers domaines. Elle offre des fonctionnalités complètes allant de la création de contrats à la gestion des paiements.
Table des matières

Principales Fonctionnalités
Stack Technologique
Installation
Configuration
Utilisation
Contribution
Auteurs
Licence

Principales Fonctionnalités

Création et gestion de contrats
Affichage des profils et portfolios des professionnels
Système d'évaluation et d'avis
Paiement sécurisé via Stripe
Authentification des utilisateurs

Stack Technologique

Backend : Django, Django REST Framework
Frontend : HTML, CSS, Bootstrap
Base de données : SQLite (développement), PostgreSQL (production recommandée)
Paiement : Intégration Stripe

Installation

Clonez le dépôt :
git clone https://github.com/yourusername/yourproject.git
cd yourproject

Créez un environnement virtuel :
python -m venv venv
source venv/bin/activate  # Sur Windows, utilisez `venv\Scripts\activate`

Installez les dépendances :
pip install -r requirements.txt

Effectuez les migrations :
python manage.py migrate


Configuration

Créez un fichier .env à la racine du projet et ajoutez les variables d'environnement nécessaires :
SECRET_KEY=votre_clé_secrète_django
DEBUG=True
STRIPE_PUBLIC_KEY=votre_clé_publique_stripe
STRIPE_SECRET_KEY=votre_clé_secrète_stripe

Configurez la base de données dans settings.py si vous utilisez autre chose que SQLite.

Pour la production, assurez-vous de définir DEBUG=False et configurez correctement ALLOWED_HOSTS.


Utilisation

Lancez le serveur de développement :
python manage.py runserver

Accédez à l'application via http://localhost:8000 dans votre navigateur.

Créez un compte administrateur :
python manage.py createsuperuser

Accédez au panel d'administration via http://localhost:8000/admin/ pour gérer les données.
