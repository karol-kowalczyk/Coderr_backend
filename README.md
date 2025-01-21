# **Backend für mein Freelancer-Projekt**

Dieses Projekt ist das Backend für meine Plattform, die speziell für Softwareentwickler und Freelancer entwickelt wurde. Es bietet eine robuste API, um das Frontend mit allen erforderlichen Funktionen zu versorgen und ein nahtloses Nutzererlebnis zu gewährleisten.

---

## **Überblick**

Das Backend basiert auf Django und bietet die Kernfunktionen für meine Freelancer-Plattform. Es ermöglicht Unternehmen (Business-Benutzer) und Kunden (Customer-Benutzer), miteinander zu interagieren, Angebote zu erstellen und zu verwalten sowie Bestellungen und Bewertungen durchzuführen.

### **Wichtige Funktionen:**
- **Registrierung und Login:** Unterschiedliche Benutzertypen (Business und Customer) können sich registrieren und anmelden.
- **Angebotsmanagement:** Business-Benutzer können Angebote erstellen, bearbeiten und verwalten.
- **Bestellungen:** Customer-Benutzer können Angebote bestellen und so Dienstleistungen in Anspruch nehmen.
- **Bewertungen:** Kunden können Reviews erstellen, bearbeiten und löschen, um Feedback zu geben.
- **Profilmanagement:** Jeder Benutzer kann sein eigenes Profil verwalten.

---

## **Voraussetzungen**

Damit dieses Projekt lokal ausgeführt werden kann, sind die folgenden Software-Komponenten erforderlich:

1. **Python:** Version 3.x (empfohlen: 3.8 oder höher).
2. **Django:** Siehe Version und spezifische Abhängigkeiten in der Datei `requirements.txt`.
3. **Virtuelle Umgebung:** Zur Verwaltung der Python-Abhängigkeiten.

> **Hinweis:** Alle erforderlichen Pakete und Versionen können bequem mit dem Befehl `pip install -r requirements.txt` installiert werden.

---

## **Installation**

### **1. Projekt klonen**
Zuerst muss das Projekt-Repository geklont und das Arbeitsverzeichnis gewechselt werden:

git clone <REPOSITORY-URL>
cd <PROJEKT-ORDNER>
2. Virtuelle Umgebung einrichten
Um Konflikte mit global installierten Python-Bibliotheken zu vermeiden, sollte eine virtuelle Umgebung erstellt und aktiviert werden:

Kopieren
Bearbeiten
python -m venv env
source env/bin/activate    # Für Linux/Mac
env\Scripts\activate       # Für Windows
3. Abhängigkeiten installieren
Installiere alle benötigten Pakete und Bibliotheken, die in der Datei requirements.txt definiert sind:

Kopieren
Bearbeiten
pip install -r requirements.txt
4. Datenbank einrichten und Server starten
Das Projekt verwendet Django für die Datenbankverwaltung. Führe folgende Befehle aus, um die Datenbank zu initialisieren und den Entwicklungsserver zu starten:

Kopieren
Bearbeiten
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
Das Projekt ist nun lokal unter der URL http://127.0.0.1:8000 erreichbar.

5. Superuser (Admin) erstellen
Ein Superuser ist erforderlich, um das Admin-Panel von Django zu verwalten. Folge diesen Schritten:

Öffne die Django-Shell:

Kopieren
Bearbeiten
python manage.py shell
Erstelle einen Superuser und das zugehörige Profil:
python
Kopieren
Bearbeiten
from django.contrib.auth.models import User
from <APP_NAME>.models import UserProfile

superuser = User.objects.create_superuser(
    username='admin',
    email='admin@admin.com',
    password='adminPassword'
)

user_profile = UserProfile.objects.create(
    user=superuser,
    location='Gladback',
    tel='1234567890',
    description='Admin-Profil',
    working_hours='9 AM - 5 PM',
    type='staff',
    email=superuser.email
)
Der Superuser kann nun das Backend über das Admin-Interface verwalten.

Konfiguration
Das Projekt enthält wichtige Einstellungen in der Datei settings.py, die für die lokale Ausführung optimiert wurden.

Wichtige Einstellungen in INSTALLED_APPS:
python
Kopieren
Bearbeiten
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    '<APP_NAME>',
    '<AUTH_APP_NAME>',
    'django_filters',
    'corsheaders',
]
REST-Framework Konfiguration:
Das Django-REST-Framework wird für die API verwendet und ist wie folgt konfiguriert:

python
Kopieren
Bearbeiten
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
}
Wichtige Features:
Permissions: Standardmäßig können nicht authentifizierte Benutzer nur Lesezugriff haben.
Token-Authentifizierung: Benutzer können sich mit einem Token anmelden.
Filter-Backends: Ermöglicht die einfache Filterung von Daten in API-Endpunkten.
Nutzung
Nützliche Befehle:
Datenbank migrieren:

Kopieren
Bearbeiten
python manage.py makemigrations
python manage.py migrate
Entwicklungsserver starten:

Kopieren
Bearbeiten
python manage.py runserver
Superuser erstellen: Verwende die Django-Shell, um einen Superuser zu erstellen (siehe Abschnitt oben).
API-Verwendung:
Die API-Endpunkte sind so konzipiert, dass sie nahtlos mit dem Frontend kommunizieren können. Weitere Dokumentationen zu den verfügbaren Endpunkten und deren Nutzung sollten in einer separaten API-Dokumentation bereitgestellt werden.







