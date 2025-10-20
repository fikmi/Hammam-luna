# Hammam Luna

Plateforme de réservation et de commerce pour un hammam moderne. Projet Django 5 avec HTMX, Tailwind CSS et Django REST Framework.

## Fonctionnalités clés

- Frontoffice responsive permettant la consultation du catalogue, la réservation de services et la commande de produits.
- Backoffice sécurisé (RBAC via permissions Django) incluant la gestion des services, produits, prestataires, règles de prix, commandes et planning.
- API REST `/api/v1/` pour services, produits, rendez-vous, commandes, prestataires et règles tarifaires.
- Facturation PDF (WeasyPrint), notifications e-mail (console par défaut) et audit log.
- Authentification par sessions, inscription, réinitialisation de mot de passe et option 2FA (TOTP).
- Tests automatisés (pytest + pytest-django), lint (ruff), formatage (black) et typage (mypy sur les apps principales).

## Démarrage rapide

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

Accès :
- Front : http://127.0.0.1:8000/
- Backoffice : http://127.0.0.1:8000/backoffice/
- Dashboard : http://127.0.0.1:8000/dashboard/
- API : http://127.0.0.1:8000/api/v1/

Comptes démo créés par `seed_demo` (mot de passe `demo1234`).

## Docker

```bash
docker compose up --build
```

## Commandes utiles

```bash
make dev        # migrations + serveur dev
make test       # exécuter la suite de tests
make lint       # lint ruff
make format     # formatage black + ruff fix
make seed       # données de démo
```

## Tests & Qualité

- Tests intégration : réservation, règles de prix, flux commande→paiement.
- Couverture visée >85% (à ajuster selon évolutions).
- CI minimale via GitHub Actions (`.github/workflows/ci.yml`).

## Captures d'écran

Inclure des captures d'écran dans un dossier `docs/` si nécessaire.
