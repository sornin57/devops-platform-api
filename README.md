# msornin - DevOps Platform API

API FastAPI minimale pour un projet portfolio DevOps.

Le but du projet est de créer une petite API backend propre, testée en local, puis de l'utiliser ensuite comme base pour apprendre Docker, CI/CD, registry, Kubernetes et monitoring.

Pour l'instant, le projet reste volontairement simple : les services sont stockés en mémoire dans une liste Python.

## Fonctionnalites

- Endpoint de sante
- Informations de l'application
- Catalogue de services
- Lecture d'un service par id
- Creation d'un service
- Modification d'un service
- Suppression d'un service
- Filtres par status et environment
- Validation des donnees avec Pydantic
- Tests avec pytest
- Verification du style avec flake8
- Verification des types avec mypy
- CI GitHub Actions

## Structure

```text
devops-platform-api/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   └── schemas.py
├── tests/
│   └── test_main.py
├── .dockerignore
├── .flake8
├── .github/
│   └── workflows/
│       └── ci.yml
├── .gitignore
├── Dockerfile
├── pytest.ini
├── README.md
├── requirements-dev.txt
└── requirements.txt
```

## Commandes utiles

Creer l'environnement Python :

```bash
python3 -m venv .venv
```

Activer l'environnement :

```bash
source .venv/bin/activate
```

Installer les dependances :

```bash
pip install -r requirements.txt
```

Installer les dependances de developpement :

```bash
pip install -r requirements-dev.txt
```

Lancer l'API en local :

```bash
uvicorn app.main:app --reload
```

Lancer les tests :

```bash
pytest
```

Lancer les tests avec Python :

```bash
python -m pytest
```

Verifier le style :

```bash
flake8 app tests
```

Verifier les types :

```bash
mypy app
```

Lancer tous les checks principaux :

```bash
flake8 app tests
mypy app
pytest
```

## CI GitHub Actions

Le workflow `.github/workflows/ci.yml` se lance automatiquement sur :

```text
push sur main
pull request
```

Il execute :

```text
flake8 app tests
mypy app
pytest
docker build -t devops-platform-api .
```

## Docker

Construire l'image Docker :

```bash
docker build -t devops-platform-api .
```

Lancer l'API dans un container :

```bash
docker run --rm -p 8000:8000 devops-platform-api
```

Tester le container :

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/api/info
curl http://127.0.0.1:8000/api/services
```

Lancer le container avec des variables d'environnement :

```bash
docker run --rm -p 8000:8000 \
  -e APP_ENV=production \
  -e APP_NAME="DevOps Platform API Docker" \
  devops-platform-api
```

Tester la configuration Docker :

```bash
curl http://127.0.0.1:8000/api/info
```

Reponse attendue :

```json
{
  "app_name": "DevOps Platform API Docker",
  "environment": "production"
}
```

Voir les containers en cours :

```bash
docker ps
```

Voir tous les containers, meme arretes :

```bash
docker ps -a
```

Note : `--rm` supprime automatiquement le container quand il s'arrete. Il ne supprime pas l'image Docker.

## Variables d'environnement

Valeurs par defaut :

```text
APP_NAME=DevOps Platform API
APP_ENV=development
```

Exemple pour lancer l'API avec un environnement different :

```bash
APP_ENV=production uvicorn app.main:app --reload
```

## Endpoints

```text
GET    /health
GET    /api/info
GET    /api/services
GET    /api/services/{service_id}
POST   /api/services
PUT    /api/services/{service_id}
DELETE /api/services/{service_id}
```

## Filtres

Lister uniquement les services en running :

```bash
curl "http://127.0.0.1:8000/api/services?status=running"
```

Lister uniquement les services en production :

```bash
curl "http://127.0.0.1:8000/api/services?environment=production"
```

Combiner les deux filtres :

```bash
curl "http://127.0.0.1:8000/api/services?status=running&environment=production"
```

## Exemples curl

Verifier que l'API fonctionne :

```bash
curl http://127.0.0.1:8000/health
```

Afficher les infos de l'application :

```bash
curl http://127.0.0.1:8000/api/info
```

Lister les services :

```bash
curl http://127.0.0.1:8000/api/services
```

Afficher un service precis :

```bash
curl http://127.0.0.1:8000/api/services/1
```

Creer un service :

```bash
curl -X POST http://127.0.0.1:8000/api/services \
  -H "Content-Type: application/json" \
  -d '{
    "name": "payment-api",
    "status": "running",
    "version": "1.0.0",
    "environment": "production"
  }'
```

Modifier un service :

```bash
curl -X PUT http://127.0.0.1:8000/api/services/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "auth-api",
    "status": "degraded",
    "version": "1.0.1",
    "environment": "production"
  }'
```

Supprimer un service :

```bash
curl -X DELETE http://127.0.0.1:8000/api/services/2
```

## Valeurs autorisees

Status possibles :

```text
running
stopped
degraded
deploying
```

Environments possibles :

```text
development
staging
production
```

## Notes

Les donnees sont stockees en memoire. Si l'API ou le container redemarre, les services ajoutes avec `POST` disparaissent.

Docker est valide : l'API peut maintenant tourner en local ou dans un container.

La prochaine grosse etape sera Git/GitHub puis CI/CD.
