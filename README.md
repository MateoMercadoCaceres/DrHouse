# DrHouse

Asistente médico con IA. Permite a un usuario registrado describir síntomas y obtener un posible diagnóstico, consultar información sobre medicamentos (usos, efectos secundarios, recomendaciones) y generar imágenes ilustrativas de medicamentos. Las consultas quedan guardadas en el historial del usuario.

> ⚠️ Proyecto académico. Las respuestas son generadas por modelos de lenguaje y **no sustituyen una consulta médica**.

## Arquitectura

```
┌──────────────┐     HTTP      ┌──────────────────┐     HTTP      ┌──────────────────┐
│   Frontend   │ ────────────▶ │     Backend      │ ────────────▶ │    Models API    │
│  React :3000 │               │  FastAPI :1712   │               │  FastAPI :2342   │
└──────┬───────┘               └────────┬─────────┘               └────────┬─────────┘
       │                                │                                  │
       │  generación de imágenes        ▼                                  ▼
       └───────────────────────▶   MongoDB :27017              OpenRouter (DeepSeek)
                                   (usuarios, historial)       Google Gemini (imágenes)
```

| Proyecto | Descripción | Tecnologías |
|---|---|---|
| [drhouse-backend](drhouse-backend/) | API principal: registro/login con JWT, persistencia de diagnósticos y consultas de medicamentos por usuario. Hace de intermediario con la Models API. | Python 3.12, FastAPI, PyMongo, python-jose, bcrypt |
| [drhouse-frontend](drhouse-frontend/) | Interfaz web con chats de diagnóstico, medicamentos y generación de imágenes. | React 19, React Router, lucide-react |
| [drhouse-deploy](drhouse-deploy/) | `docker-compose` que levanta backend, Models API y MongoDB juntos. | Docker Compose |
| [drhouse-models](drhouse-models/) | Servicio de IA: diagnóstico a partir de síntomas, información de medicamentos y generación de imágenes. Incluye los scripts de los modelos GPT-2 afinados. | FastAPI, OpenAI SDK (OpenRouter), google-genai, Transformers, PyTorch |

## Estructura

```
DrHouse/
├── drhouse-backend/
│   └── src/
│       ├── config/         # conexión a MongoDB
│       ├── controllers/    # auth, users, diagnostics, medicines, test
│       ├── middleware/     # validación de JWT
│       ├── models/         # esquemas Pydantic
│       ├── repositories/   # acceso a MongoDB
│       └── services/       # lógica de negocio y llamadas a la Models API
├── drhouse-frontend/
│   └── src/
│       ├── infrastructure/ # servicios HTTP, modelos, cookies
│       └── presentation/   # páginas (Home, Models, About, Contact, Auth) y chats
├── drhouse-deploy/
│   └── docker-compose.yml
└── drhouse-models/
    ├── database/           # datasets CSV (síntomas/enfermedades y medicamentos)
    └── src/
        ├── controllers/    # diagnóstico, medicina, imágenes
        ├── prompt/         # prompts para cada tarea
        ├── services/       # clientes de OpenRouter y Gemini
        ├── models/         # esquemas y scripts de los modelos GPT-2
        └── static/images/  # imágenes generadas
```

## Requisitos

- Docker y Docker Compose (recomendado), o bien
- Python 3.12, Node.js 18+ y una instancia de MongoDB
- Claves de API:
  - `OPENROUTER_API_KEY` — [OpenRouter](https://openrouter.ai/), usado para DeepSeek
  - `GENAI_API_KEY` — [Google AI Studio](https://aistudio.google.com/), usado para Gemini

## Puesta en marcha

### Con Docker (backend + Models API + MongoDB)

```bash
cd drhouse-deploy
export OPENROUTER_API_KEY=tu_clave
export GENAI_API_KEY=tu_clave
docker compose up --build
```

Luego levanta el frontend por separado:

```bash
cd drhouse-frontend
npm install
npm start
```

| Servicio | URL |
|---|---|
| Frontend | http://localhost:3000 |
| Backend (Swagger) | http://localhost:1712/docs |
| Models API (Swagger) | http://localhost:2342/docs |

### Manual (sin Docker)

Cada servicio Python lee su configuración de un archivo `.env` en su carpeta (no se versiona).

**Models API**

```bash
cd drhouse-models
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cd src && uvicorn main:app --host 0.0.0.0 --port 2342
```

`drhouse-models/.env`:

```env
OPENROUTER_API_KEY=...
GENAI_API_KEY=...
```

**Backend**

```bash
cd drhouse-backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cd src && uvicorn main:app --host 0.0.0.0 --port 1712
```

`drhouse-backend/.env`:

```env
MONGO_URL=mongodb://localhost:27017
DB_NAME=userapi
DIAGNOSTIC_API_BASE_URL=http://localhost:2342/api/v1
SECRET_KEY=una_clave_secreta        # firma y valida los JWT de /api/users y del middleware
JWT_SECRET_KEY=una_clave_secreta    # usada por /api/v1/auth/login
JWT_ALGORITHM=HS256
```

Puedes generar una clave con `python drhouse-backend/src/utils/generate_secret.py`.

**Frontend**

```bash
cd drhouse-frontend
npm install
npm start
```

Las URLs de las APIs están definidas en `drhouse-frontend/src/infrastructure/services/` (`http://localhost:1712` y `http://localhost:2342`).

## Endpoints principales

### Backend (`:1712`)

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/api/users/register` | Registro de usuario |
| POST | `/api/users/login` | Login, devuelve JWT |
| GET | `/api/users/me` | Datos del usuario autenticado |
| POST | `/api/diagnostics/` | Crear diagnóstico a partir de síntomas |
| POST | `/api/diagnostics/symptoms` | Extraer síntomas de un texto |
| POST | `/api/diagnostics/explain-disease` | Explicar una enfermedad |
| GET | `/api/diagnostics/` | Historial de diagnósticos del usuario |
| POST | `/api/medicines/` | Consulta sobre un medicamento |
| POST | `/api/medicines/info` · `/side-effects` · `/uses` | Información específica de un medicamento |
| GET | `/api/medicines/` | Historial de consultas de medicamentos |

Las rutas de diagnósticos y medicamentos requieren el header `Authorization: Bearer <token>`.

### Models API (`:2342`, prefijo `/api/v1`)

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/diagnose` | Diagnóstico a partir de síntomas (DeepSeek R1) |
| POST | `/symptoms` | Extracción de síntomas |
| POST | `/explain-disease` | Explicación de una enfermedad |
| GET | `/medicine/{nombre}/info` | Información del medicamento (DeepSeek Chat) |
| GET | `/medicine/{nombre}/side-effects` | Efectos secundarios |
| GET | `/medicine/{nombre}/uses` | Usos |
| POST | `/medicine/recommend` | Recomendación de medicamento |
| POST | `/medicine/generate-image` | Genera imagen del medicamento (Gemini) |

## Modelos GPT-2 propios

En `drhouse-models/src/models/` están los scripts de dos modelos GPT-2 afinados:

- `diagnostic-drhouse-model.py` → `gpt2-medical/`, entrenado con `database/Training.csv`
- `medicine-model.py` → `medicine-gpt2-drhouse/`, entrenado con `database/Medicine_Details-*.csv`

Los pesos y checkpoints entrenados (~11 GB) **no están en el repositorio** por su tamaño. Para usarlos hay que volver a entrenarlos o colocar las carpetas `gpt2-medical/` y `medicine-gpt2-drhouse/` dentro de `drhouse-models/src/models/`. La API actual usa DeepSeek y Gemini, no estos modelos locales.

## Autor

Mateo Mercado Caceres
