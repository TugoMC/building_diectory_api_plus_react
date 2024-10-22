# Generated by Django 4.2 on 2024-10-18 15:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('requested', 'Demandé'), ('confirmed', 'Confirmé'), ('completed', 'Terminé'), ('cancelled', 'Annulé')], default='requested', max_length=20)),
                ('payment_status', models.CharField(choices=[('pending', 'En attente'), ('paid', 'Payé')], default='pending', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_title', models.CharField(max_length=255)),
                ('project_description', models.TextField()),
                ('project_image', models.ImageField(blank=True, null=True, upload_to='portfolio_images/')),
            ],
        ),
        migrations.CreateModel(
            name='Professional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255, verbose_name='Nom complet')),
                ('profile_photo', models.ImageField(blank=True, null=True, upload_to='photos/', verbose_name='Photo de profil')),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True, verbose_name='Email')),
                ('phone', models.CharField(db_index=True, max_length=20, verbose_name='Téléphone')),
                ('city', models.CharField(choices=[('Abidjan', 'Abidjan'), ('Yamoussoukro', 'Yamoussoukro'), ('Bouaké', 'Bouaké'), ('Daloa', 'Daloa'), ('San-Pédro', 'San-Pédro'), ('Korhogo', 'Korhogo'), ('Gagnoa', 'Gagnoa'), ('Soubré', 'Soubré'), ('Man', 'Man'), ('Anyama', 'Anyama'), ('Abengourou', 'Abengourou'), ('Grand-Bassam', 'Grand-Bassam'), ('Divo', 'Divo'), ('Agboville', 'Agboville'), ('Katiola', 'Katiola'), ('Bondoukou', 'Bondoukou'), ('Ferkessédougou', 'Ferkessédougou'), ('Adzopé', 'Adzopé'), ('Oumé', 'Oumé'), ('Dabou', 'Dabou'), ('Sinfra', 'Sinfra'), ('Bingerville', 'Bingerville'), ('Duekoué', 'Duekoué'), ('Dimbokro', 'Dimbokro'), ('Séguéla', 'Séguéla'), ('Aboisso', 'Aboisso'), ('Daoukro', 'Daoukro'), ('Odienné', 'Odienné'), ('Bangolo', 'Bangolo'), ('Biankouma', 'Biankouma'), ('Sassandra', 'Sassandra'), ('Bouna', 'Bouna'), ('Touba', 'Touba'), ('Zoukougbeu', 'Zoukougbeu'), ('Bouaflé', 'Bouaflé'), ('Mankono', 'Mankono'), ('Kounahiri', 'Kounahiri')], max_length=100, verbose_name='Ville')),
                ('commune', models.CharField(choices=[('Abengourou', 'Abengourou'), ('Abobo', 'Abobo'), ('Aboisso', 'Aboisso'), ('Adiaké', 'Adiaké'), ('Adjamé', 'Adjamé'), ('Agboville', 'Agboville'), ('Agnibilékrou', 'Agnibilékrou'), ('Akoupé', 'Akoupé'), ('Anyama', 'Anyama'), ('Arrah', 'Arrah'), ('Assuéfry', 'Assuéfry'), ('Attécoubé', 'Attécoubé'), ('Ayémé', 'Ayémé'), ('Azaguié', 'Azaguié'), ('Bako', 'Bako'), ('Bangolo', 'Bangolo'), ('Bassawa', 'Bassawa'), ('Bédiala', 'Bédiala'), ('Béoumi', 'Béoumi'), ('Bettié', 'Bettié'), ('Biankouma', 'Biankouma'), ('Bingerville', 'Bingerville'), ('Bin-Houyé', 'Bin-Houyé'), ('Bloléquin', 'Bloléquin'), ('Bocanda', 'Bocanda'), ('Bodokro', 'Bodokro'), ('Bondoukou', 'Bondoukou'), ('Bongouanou', 'Bongouanou'), ('Bonon', 'Bonon'), ('Bonoua', 'Bonoua'), ('Booko', 'Booko'), ('Bouaflé', 'Bouaflé'), ('Bouaké', 'Bouaké'), ('Bouna', 'Bouna'), ('Boundiali', 'Boundiali'), ('Brobo', 'Brobo'), ('Buyo', 'Buyo'), ('Cocody', 'Cocody'), ('Dabakala', 'Dabakala'), ('Dabou', 'Dabou'), ('Daloa', 'Daloa'), ('Daoukro', 'Daoukro'), ('Dianra', 'Dianra'), ('Didiévi', 'Didiévi'), ('Dimbokro', 'Dimbokro'), ('Divo', 'Divo'), ('Djékanou', 'Djékanou'), ('Djibrosso', 'Djibrosso'), ('Ferkessédougou', 'Ferkessédougou'), ('Fresco', 'Fresco'), ('Grand-Bassam', 'Grand-Bassam'), ('Guéyo', 'Guéyo'), ('Guibéroua', 'Guibéroua'), ('Guiglo', 'Guiglo'), ('Issia', 'Issia'), ('Jacqueville', 'Jacqueville'), ('Kaniasso', 'Kaniasso'), ('Katiola', 'Katiola'), ('Kokumbo', 'Kokumbo'), ('Korhogo', 'Korhogo'), ('Koumassi', 'Koumassi'), ('Koumbala', 'Koumbala'), ('Kouassi-Datékro', 'Kouassi-Datékro'), ('Kouassi-Kouassikro', 'Kouassi-Kouassikro'), ('Kouibly', 'Kouibly'), ('Kouto', 'Kouto'), ('Lakota', 'Lakota'), ('Logoualé', 'Logoualé'), ("Madina-N'Gana", "Madina-N'Gana"), ('Man', 'Man'), ('Mankono', 'Mankono'), ('Massala', 'Massala'), ('Mayo', 'Mayo'), ("M'Bahiakro", "M'Bahiakro"), ("M'Batto", "M'Batto"), ('Méagui', 'Méagui'), ('Minignan', 'Minignan'), ('Morondo', 'Morondo'), ('Napiéolédougou', 'Napiéolédougou'), ('Nassian', 'Nassian'), ("N'Djébonouan", "N'Djébonouan"), ('Niablé', 'Niablé'), ('Niakaramandougou', 'Niakaramandougou'), ('Niellé', 'Niellé'), ('Niofoin', 'Niofoin'), ('Odienné', 'Odienné'), ('Ouaninou', 'Ouaninou'), ('Ouellé', 'Ouellé'), ('Oumé', 'Oumé'), ('Ouragahio', 'Ouragahio'), ('Plateau', 'Plateau'), ('Port-Bouët', 'Port-Bouët'), ('Prikro', 'Prikro'), ('Rubino', 'Rubino'), ('Saïoua', 'Saïoua'), ('Sakassou', 'Sakassou'), ('San-Pédro', 'San-Pédro'), ('Sassandra', 'Sassandra'), ('Séguéla', 'Séguéla'), ('Sikensi', 'Sikensi'), ('Sinématiali', 'Sinématiali'), ('Sinfra', 'Sinfra'), ('Sipilou', 'Sipilou'), ('Sirasso', 'Sirasso'), ('Songon', 'Songon'), ('Soubré', 'Soubré'), ('Taabo', 'Taabo'), ('Tabou', 'Tabou'), ('Tafiré', 'Tafiré'), ('Tanda', 'Tanda'), ('Téhini', 'Téhini'), ('Tiapoum', 'Tiapoum'), ('Tiassalé', 'Tiassalé'), ('Tiébissou', 'Tiébissou'), ('Tiémélékro', 'Tiémélékro'), ("Tié-N'Diékro", "Tié-N'Diékro"), ('Tienko', 'Tienko'), ('Tioroniaradougou', 'Tioroniaradougou'), ('Touba', 'Touba'), ('Toulépleu', 'Toulépleu'), ('Toumodi', 'Toumodi'), ('Transua', 'Transua'), ('Treichville', 'Treichville')], max_length=100, verbose_name='Commune')),
                ('presentation_video', models.FileField(blank=True, null=True, upload_to='videos/', verbose_name='Vidéo de présentation')),
                ('specialization', models.CharField(choices=[('Gros Oeuvre', 'Gros Oeuvre'), ('Second Oeuvre', 'Second Oeuvre'), ('Finitions', 'Finitions'), ('Plomberie', 'Plomberie'), ('Électricité', 'Électricité'), ('Chauffage, Ventilation et Climatisation (CVC)', 'Chauffage, Ventilation et Climatisation (CVC)'), ('Toiture', 'Toiture'), ('Menuiserie', 'Menuiserie'), ('Serrurerie', 'Serrurerie'), ('Peinture et Décoration', 'Peinture et Décoration'), ('Plâtrerie', 'Plâtrerie'), ('Revêtements de Sol et Murs', 'Revêtements de Sol et Murs'), ('Aménagements Extérieurs', 'Aménagements Extérieurs'), ('Rénovation et Réhabilitation', 'Rénovation et Réhabilitation'), ('Isolation Thermique et Acoustique', 'Isolation Thermique et Acoustique'), ('Éclairage', 'Éclairage'), ('Sécurité Incendie', 'Sécurité Incendie')], max_length=255, verbose_name='Spécialisation')),
                ('skill_level', models.CharField(choices=[('Débutant', 'Débutant'), ('Intermédiaire', 'Intermédiaire'), ('Expert', 'Expert')], max_length=50, verbose_name='Niveau de compétence')),
                ('certifications', models.TextField(blank=True, verbose_name='Certifications')),
                ('years_of_experience', models.PositiveIntegerField(help_text="Nombre d'années d'expérience", verbose_name="Années d'expérience")),
                ('daily_rate', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Tarif journalier')),
                ('availability', models.CharField(help_text='Exemple : Lundi - Vendredi, 9h - 18h', max_length=255, verbose_name='Disponibilité')),
                ('identity_verified', models.BooleanField(default=False, verbose_name='Identité vérifiée')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=30)),
                ('last_name', models.CharField(blank=True, max_length=30)),
                ('profession', models.CharField(blank=True, choices=[('entrepreneur', 'Entrepreneur'), ('proprietaire', 'Propriétaire'), ('investisseur', 'Investisseur'), ('locataire', 'Locataire'), ('agent_immobilier', 'Agent Immobilier'), ('architecte', 'Architecte'), ('decorateur', "Décorateur d'Intérieur"), ('autre', 'Autre')], max_length=20)),
                ('profile_photo', models.ImageField(blank=True, null=True, upload_to='profile_photos/')),
                ('phone_number', models.CharField(blank=True, max_length=20)),
                ('city', models.CharField(blank=True, choices=[('Abidjan', 'Abidjan'), ('Yamoussoukro', 'Yamoussoukro'), ('Bouaké', 'Bouaké'), ('Daloa', 'Daloa'), ('San-Pédro', 'San-Pédro'), ('Korhogo', 'Korhogo'), ('Gagnoa', 'Gagnoa'), ('Soubré', 'Soubré'), ('Man', 'Man'), ('Anyama', 'Anyama'), ('Abengourou', 'Abengourou'), ('Grand-Bassam', 'Grand-Bassam'), ('Divo', 'Divo'), ('Agboville', 'Agboville'), ('Katiola', 'Katiola'), ('Bondoukou', 'Bondoukou'), ('Ferkessédougou', 'Ferkessédougou'), ('Adzopé', 'Adzopé'), ('Oumé', 'Oumé'), ('Dabou', 'Dabou'), ('Sinfra', 'Sinfra'), ('Bingerville', 'Bingerville'), ('Duekoué', 'Duekoué'), ('Dimbokro', 'Dimbokro'), ('Séguéla', 'Séguéla'), ('Aboisso', 'Aboisso'), ('Daoukro', 'Daoukro'), ('Odienné', 'Odienné'), ('Bangolo', 'Bangolo'), ('Biankouma', 'Biankouma'), ('Sassandra', 'Sassandra'), ('Bouna', 'Bouna'), ('Touba', 'Touba'), ('Zoukougbeu', 'Zoukougbeu'), ('Bouaflé', 'Bouaflé'), ('Mankono', 'Mankono'), ('Kounahiri', 'Kounahiri')], max_length=100)),
                ('commune', models.CharField(blank=True, choices=[('Abengourou', 'Abengourou'), ('Abobo', 'Abobo'), ('Aboisso', 'Aboisso'), ('Adiaké', 'Adiaké'), ('Adjamé', 'Adjamé'), ('Agboville', 'Agboville'), ('Agnibilékrou', 'Agnibilékrou'), ('Akoupé', 'Akoupé'), ('Anyama', 'Anyama'), ('Arrah', 'Arrah'), ('Assuéfry', 'Assuéfry'), ('Attécoubé', 'Attécoubé'), ('Ayémé', 'Ayémé'), ('Azaguié', 'Azaguié'), ('Bako', 'Bako'), ('Bangolo', 'Bangolo'), ('Bassawa', 'Bassawa'), ('Bédiala', 'Bédiala'), ('Béoumi', 'Béoumi'), ('Bettié', 'Bettié'), ('Biankouma', 'Biankouma'), ('Bingerville', 'Bingerville'), ('Bin-Houyé', 'Bin-Houyé'), ('Bloléquin', 'Bloléquin'), ('Bocanda', 'Bocanda'), ('Bodokro', 'Bodokro'), ('Bondoukou', 'Bondoukou'), ('Bongouanou', 'Bongouanou'), ('Bonon', 'Bonon'), ('Bonoua', 'Bonoua'), ('Booko', 'Booko'), ('Bouaflé', 'Bouaflé'), ('Bouaké', 'Bouaké'), ('Bouna', 'Bouna'), ('Boundiali', 'Boundiali'), ('Brobo', 'Brobo'), ('Buyo', 'Buyo'), ('Cocody', 'Cocody'), ('Dabakala', 'Dabakala'), ('Dabou', 'Dabou'), ('Daloa', 'Daloa'), ('Daoukro', 'Daoukro'), ('Dianra', 'Dianra'), ('Didiévi', 'Didiévi'), ('Dimbokro', 'Dimbokro'), ('Divo', 'Divo'), ('Djékanou', 'Djékanou'), ('Djibrosso', 'Djibrosso'), ('Ferkessédougou', 'Ferkessédougou'), ('Fresco', 'Fresco'), ('Grand-Bassam', 'Grand-Bassam'), ('Guéyo', 'Guéyo'), ('Guibéroua', 'Guibéroua'), ('Guiglo', 'Guiglo'), ('Issia', 'Issia'), ('Jacqueville', 'Jacqueville'), ('Kaniasso', 'Kaniasso'), ('Katiola', 'Katiola'), ('Kokumbo', 'Kokumbo'), ('Korhogo', 'Korhogo'), ('Koumassi', 'Koumassi'), ('Koumbala', 'Koumbala'), ('Kouassi-Datékro', 'Kouassi-Datékro'), ('Kouassi-Kouassikro', 'Kouassi-Kouassikro'), ('Kouibly', 'Kouibly'), ('Kouto', 'Kouto'), ('Lakota', 'Lakota'), ('Logoualé', 'Logoualé'), ("Madina-N'Gana", "Madina-N'Gana"), ('Man', 'Man'), ('Mankono', 'Mankono'), ('Massala', 'Massala'), ('Mayo', 'Mayo'), ("M'Bahiakro", "M'Bahiakro"), ("M'Batto", "M'Batto"), ('Méagui', 'Méagui'), ('Minignan', 'Minignan'), ('Morondo', 'Morondo'), ('Napiéolédougou', 'Napiéolédougou'), ('Nassian', 'Nassian'), ("N'Djébonouan", "N'Djébonouan"), ('Niablé', 'Niablé'), ('Niakaramandougou', 'Niakaramandougou'), ('Niellé', 'Niellé'), ('Niofoin', 'Niofoin'), ('Odienné', 'Odienné'), ('Ouaninou', 'Ouaninou'), ('Ouellé', 'Ouellé'), ('Oumé', 'Oumé'), ('Ouragahio', 'Ouragahio'), ('Plateau', 'Plateau'), ('Port-Bouët', 'Port-Bouët'), ('Prikro', 'Prikro'), ('Rubino', 'Rubino'), ('Saïoua', 'Saïoua'), ('Sakassou', 'Sakassou'), ('San-Pédro', 'San-Pédro'), ('Sassandra', 'Sassandra'), ('Séguéla', 'Séguéla'), ('Sikensi', 'Sikensi'), ('Sinématiali', 'Sinématiali'), ('Sinfra', 'Sinfra'), ('Sipilou', 'Sipilou'), ('Sirasso', 'Sirasso'), ('Songon', 'Songon'), ('Soubré', 'Soubré'), ('Taabo', 'Taabo'), ('Tabou', 'Tabou'), ('Tafiré', 'Tafiré'), ('Tanda', 'Tanda'), ('Téhini', 'Téhini'), ('Tiapoum', 'Tiapoum'), ('Tiassalé', 'Tiassalé'), ('Tiébissou', 'Tiébissou'), ('Tiémélékro', 'Tiémélékro'), ("Tié-N'Diékro", "Tié-N'Diékro"), ('Tienko', 'Tienko'), ('Tioroniaradougou', 'Tioroniaradougou'), ('Touba', 'Touba'), ('Toulépleu', 'Toulépleu'), ('Toumodi', 'Toumodi'), ('Transua', 'Transua'), ('Treichville', 'Treichville')], max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('edit_count', models.PositiveIntegerField(default=0)),
                ('contract', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='professionals.contract')),
                ('professional', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='professionals.professional')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='professional',
            constraint=models.UniqueConstraint(fields=('email',), name='unique_email'),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='professional',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='portfolios', to='professionals.professional'),
        ),
        migrations.AddField(
            model_name='contract',
            name='professional',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contracts', to='professionals.professional'),
        ),
        migrations.AddField(
            model_name='contract',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contracts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('user', 'contract')},
        ),
        migrations.AddConstraint(
            model_name='contract',
            constraint=models.UniqueConstraint(condition=models.Q(('status', 'confirmed')), fields=('professional', 'status'), name='unique_active_contract'),
        ),
    ]
