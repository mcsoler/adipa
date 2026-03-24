# ADIPA — Extractor Automático de Preguntas

Aplicación web full-stack que recibe un documento (PDF, DOCX o XLSX), extrae automáticamente las preguntas detectadas usando un modelo de lenguaje local (Ollama), y retorna un JSON estructurado con enunciados, alternativas, tipo de pregunta y respuesta correcta.

---

## Índice

1. [¿Qué hace la aplicación?](#qué-hace-la-aplicación)
2. [Arquitectura](#arquitectura)
3. [Stack tecnológico](#stack-tecnológico)
4. [Estructura de carpetas](#estructura-de-carpetas)
5. [Despliegue en Producción](#despliegue-en-producción)
6. [Despliegue con Docker Compose (local)](#despliegue-con-docker-compose)
7. [Variables de entorno](#variables-de-entorno)
8. [API Reference](#api-reference)
9. [Base de datos](#base-de-datos)
10. [Flujo LangGraph](#flujo-langgraph)
11. [Principios SOLID aplicados](#principios-solid-aplicados)
12. [Tests (TDD)](#tests-tdd)
13. [Desarrollo local sin Docker](#desarrollo-local-sin-docker)

---

## ¿Qué hace la aplicación?

1. El usuario sube un archivo **PDF**, **DOCX** o **XLSX** desde la interfaz web.
2. El backend extrae el texto crudo del documento.
3. Un pipeline **LangGraph** orquesta la extracción: envía el texto a **Ollama** (LLM local) con un prompt especializado.
4. El LLM identifica preguntas, clasifica su tipo y detecta alternativas y respuestas correctas.
5. El resultado se valida contra un schema Pydantic y se almacena en **PostgreSQL**.
6. La UI muestra las preguntas estructuradas con resaltado de respuestas correctas y permite descargar el resultado como JSON.

### Ejemplo de salida

```json
{
  "total_preguntas": 2,
  "preguntas": [
    {
      "numero": 1,
      "enunciado": "¿Cuál es el principal criterio diagnóstico del TAG?",
      "tipo": "seleccion_multiple",
      "alternativas": [
        { "letra": "A", "texto": "Alucinaciones visuales recurrentes" },
        { "letra": "B", "texto": "Preocupación excesiva difícil de controlar" },
        { "letra": "C", "texto": "Estado de ánimo persistentemente elevado" }
      ],
      "respuesta_correcta": "B"
    },
    {
      "numero": 2,
      "enunciado": "La terapia cognitivo-conductual es efectiva para el TAG.",
      "tipo": "verdadero_falso",
      "alternativas": [],
      "respuesta_correcta": "Verdadero"
    }
  ]
}
```

### Tipos de preguntas detectados

| Tipo | Descripción |
|------|-------------|
| `seleccion_multiple` | Pregunta con alternativas A, B, C, D… |
| `verdadero_falso` | Se responde con Verdadero o Falso |
| `desarrollo` | Respuesta abierta, sin alternativas |
| `emparejamiento` | Dos columnas para relacionar conceptos |

---

## Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                        Usuario (Browser)                    │
│                     React + Vite  :6000                     │
└─────────────────────────┬───────────────────────────────────┘
                          │ HTTP /api/v1
┌─────────────────────────▼───────────────────────────────────┐
│                    FastAPI Backend  :5000                    │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────┐  │
│  │  API Layer  │  │ Use Cases    │  │  Domain + SOLID    │  │
│  │  (Routes)   │→ │  (App Logic) │→ │  (Entities +       │  │
│  │             │  │              │  │   Interfaces)      │  │
│  └─────────────┘  └──────┬───────┘  └────────────────────┘  │
│                          │                                  │
│  ┌───────────────────────▼─────────────────────────────┐    │
│  │               LangGraph Pipeline                    │    │
│  │  extract_text → process_with_llm → validate_output  │    │
│  └───────────────────────┬─────────────────────────────┘    │
└──────────────────────────┼──────────────────────────────────┘
                           │
          ┌────────────────┼─────────────────┐
          │                │                 │
┌─────────▼──────┐  ┌──────▼──────┐  ┌──────▼──────┐
│   PostgreSQL   │  │   Ollama    │  │  Extractors │
│    :5435       │  │   :11434    │  │  PDF/DOCX/  │
│  (resultados) │  │  (LLM local)│  │  XLSX       │
└────────────────┘  └─────────────┘  └─────────────┘
```

---

## Stack tecnológico

| Capa | Tecnología | Versión | Puerto |
|------|-----------|---------|--------|
| Frontend | React + Vite + TypeScript | React 18 | 6000 |
| Estilos | Tailwind CSS | 3.x | — |
| Backend | FastAPI + Python | 3.12 | 5000 |
| ORM | SQLAlchemy (async) | 2.x | — |
| LLM Pipeline | LangGraph | 0.2.x | — |
| LLM Local | Ollama | (host) | 11434 |
| Base de datos | PostgreSQL | 16 | 5435 |
| Deploy | Docker Compose | — | — |
| Tests Backend | pytest + pytest-asyncio | — | — |
| Tests Frontend | Vitest + Testing Library | — | — |

---

## Estructura de carpetas

```
adipa/
├── docker-compose.yml
├── .env.example
├── .gitignore
├── README.md
│
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── pytest.ini
│   └── app/
│       ├── main.py                        # App factory FastAPI
│       ├── config.py                      # Settings con Pydantic
│       │
│       ├── domain/                        # Reglas de negocio puras
│       │   ├── value_objects/
│       │   │   ├── question_type.py       # Enum tipos de pregunta
│       │   │   └── file_type.py           # Enum tipos de archivo
│       │   └── exceptions/
│       │       ├── document_exceptions.py
│       │       └── extraction_exceptions.py
│       │
│       ├── interfaces/                    # Abstracciones (DIP)
│       │   ├── extractors/
│       │   │   └── text_extractor.py      # ITextExtractor (ABC)
│       │   ├── services/
│       │   │   └── llm_service.py         # ILLMService (ABC)
│       │   └── repositories/
│       │       ├── document_repository.py
│       │       └── extraction_repository.py
│       │
│       ├── infrastructure/                # Implementaciones concretas
│       │   ├── extractors/
│       │   │   ├── pdf_extractor.py       # PyMuPDF
│       │   │   ├── docx_extractor.py      # python-docx
│       │   │   ├── xlsx_extractor.py      # openpyxl
│       │   │   └── extractor_factory.py   # Factory (OCP)
│       │   ├── llm/
│       │   │   ├── ollama_llm_service.py
│       │   │   └── prompts/
│       │   │       └── question_extraction_prompt.py
│       │   ├── repositories/
│       │   │   ├── postgres_document_repository.py
│       │   │   └── postgres_extraction_repository.py
│       │   └── database/
│       │       ├── connection.py
│       │       └── models/
│       │           ├── document_model.py
│       │           └── extraction_model.py
│       │
│       ├── application/                   # Casos de uso (SRP)
│       │   ├── use_cases/
│       │   │   ├── upload_document.py
│       │   │   ├── extract_questions.py
│       │   │   └── get_extraction_result.py
│       │   ├── schemas/
│       │   │   ├── document_schema.py
│       │   │   ├── question_schema.py
│       │   │   └── extraction_schema.py
│       │   └── dependencies/
│       │       └── container.py           # Inyección de dependencias
│       │
│       ├── langgraph_workflow/            # Pipeline LangGraph
│       │   ├── state.py                   # WorkflowState (TypedDict)
│       │   ├── graph.py                   # StateGraph compilado
│       │   └── nodes/
│       │       ├── extract_text_node.py
│       │       ├── process_with_llm_node.py
│       │       └── validate_output_node.py
│       │
│       └── api/
│           ├── health.py
│           ├── middleware/
│           │   └── error_handler.py
│           └── v1/
│               ├── router.py
│               └── endpoints/
│                   ├── documents.py
│                   └── extractions.py
│
├── backend/tests/
│   ├── conftest.py
│   └── unit/
│       ├── test_extractors.py
│       ├── test_use_cases.py
│       ├── test_llm_service.py
│       ├── langgraph/
│       │   ├── test_extract_text_node.py
│       │   ├── test_process_with_llm_node.py
│       │   └── test_validate_output_node.py
│       └── api/
│           ├── test_documents_endpoint.py
│           └── test_extractions_endpoint.py
│
└── frontend/
    ├── Dockerfile
    ├── nginx.conf                         # Sirve en :81, proxy → backend:5000
    ├── vite.config.ts
    ├── tailwind.config.ts
    ├── package.json
    └── src/
        ├── main.tsx
        ├── App.tsx
        ├── index.css
        ├── types/
        │   ├── question.ts
        │   └── extraction.ts
        ├── services/
        │   ├── apiClient.ts               # Axios instance
        │   ├── documentService.ts
        │   └── extractionService.ts
        ├── hooks/
        │   └── useDocumentUpload.ts       # Orquesta todo el flujo UI
        └── components/
            ├── common/    Badge, Card, LoadingSpinner
            ├── upload/    FileDropzone, FilePreview, UploadButton
            ├── results/   ExtractionResultView, QuestionCard,
            │              AlternativasList, DownloadButton
            └── status/    ProcessingIndicator, ErrorMessage
```

---

## Despliegue en Producción

Guía completa desde un servidor limpio Ubuntu 22.04 LTS.

### Requisitos mínimos de servidor

| Recurso | Mínimo | Recomendado |
|---------|--------|-------------|
| RAM | 8 GB | 16 GB |
| CPU | 4 cores | 8 cores |
| Disco | 20 GB libres | 40 GB |
| SO | Ubuntu 22.04 | Ubuntu 22.04 LTS |
| Puertos abiertos | 6000, 5000 | 6000, 5000 |

> Con menos de 8 GB de RAM usar el modelo `phi3` (2.3 GB) en lugar de `llama3` (4.7 GB).

---

### Paso 1 — Instalar Docker

```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
newgrp docker
docker --version
```

---

### Paso 2 — Instalar Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Verificar que el servicio quedó activo y habilitarlo para inicio automático:

```bash
systemctl status ollama

# Si no está corriendo:
systemctl start ollama
systemctl enable ollama
```

---

### Paso 3 — Descargar el modelo LLM

```bash
# Ver modelos disponibles
ollama list

# Descargar según RAM disponible:
ollama pull llama3        # ~4.7 GB  — recomendado (≥8 GB RAM)
ollama pull mistral       # ~4.1 GB  — buena alternativa
ollama pull phi3          # ~2.3 GB  — opción ligera (4 GB RAM)
ollama pull llama3:70b    # ~40 GB   — solo con GPU dedicada
```

Verificar que el modelo responde antes de continuar:

```bash
ollama run llama3 "responde solo: hola"
# Ctrl+D para salir
```

---

### Paso 4 — Clonar el repositorio

```bash
git clone git@github.com:mcsoler/adipa.git
cd adipa
```

---

### Paso 5 — Configurar variables de entorno

```bash
cp .env.example .env
nano .env
```

Obtener la IP del bridge de Docker (necesaria para que el backend alcance Ollama):

```bash
ip route | grep docker0 | awk '{print $9}'
# Normalmente: 172.17.0.1
```

Editar `.env` con los valores de producción:

```env
# PostgreSQL
POSTGRES_USER=adipa
POSTGRES_PASSWORD=pon_aqui_una_password_segura
POSTGRES_DB=adipa_db

# Backend
DATABASE_URL=postgresql+asyncpg://adipa:pon_aqui_una_password_segura@postgres:5432/adipa_db

# Ollama — usar la IP del bridge Docker (172.17.0.1), NO host.docker.internal
OLLAMA_HOST=http://172.17.0.1:11434
OLLAMA_MODEL=llama3

# CORS — reemplazar con tu IP o dominio real
CORS_ORIGINS=http://TU_IP_O_DOMINIO:6000

# Frontend
VITE_API_URL=http://TU_IP_O_DOMINIO:5000
```

> **Importante:** En Linux, `host.docker.internal` no funciona por defecto. Siempre usar la IP del bridge (`172.17.0.1`) o la IP pública del servidor.

---

### Paso 6 — Levantar la aplicación

```bash
docker compose up --build -d
```

Verificar que los 3 contenedores están en estado `healthy` o `running`:

```bash
docker compose ps
```

Ver logs en tiempo real si hay problemas:

```bash
docker compose logs backend -f
docker compose logs frontend -f
docker compose logs postgres -f
```

---

### Paso 7 — Verificar que todo funciona

```bash
# Backend health check
curl http://localhost:5000/health
# Esperado: {"status":"ok","service":"adipa-backend"}

# Frontend responde
curl -I http://localhost:6000
# Esperado: HTTP/1.1 200 OK

# Prueba completa de extracción
curl -X POST http://localhost:5000/api/v1/documents/upload \
  -F "file=@/ruta/a/tu/documento.pdf"
# Esperado: {"document_id":"...","status":"pending",...}
```

Acceder desde el navegador: `http://TU_IP_O_DOMINIO:6000`

---

### Comandos útiles en producción

```bash
# Ver estado de todos los servicios
docker compose ps

# Reiniciar un servicio específico
docker compose restart backend

# Ver logs de las últimas 100 líneas
docker compose logs --tail=100 backend

# Actualizar a nueva versión
git pull
docker compose up --build -d

# Detener todo (conserva datos)
docker compose down

# Detener y eliminar volúmenes (BORRA LA BASE DE DATOS)
docker compose down -v

# Ver uso de recursos
docker stats
```

---

### Solución de problemas frecuentes

| Problema | Causa probable | Solución |
|----------|---------------|----------|
| Backend no conecta a Ollama | `host.docker.internal` no resuelve en Linux | Cambiar `OLLAMA_HOST` a `http://172.17.0.1:11434` |
| Error 503 en `/process` | Ollama no está corriendo | `systemctl start ollama` |
| Frontend muestra pantalla en blanco | `VITE_API_URL` incorrecto | Verificar IP en `.env` y reconstruir |
| PostgreSQL no inicia | Puerto 5435 ocupado | `lsof -i :5435` para ver qué lo usa |
| Modelo responde muy lento | RAM insuficiente | Cambiar a `phi3` en `OLLAMA_MODEL` |

---

## Despliegue con Docker Compose

### Prerequisitos

- Docker Desktop o Docker Engine + Compose v2
- Ollama corriendo en el host con al menos un modelo instalado
- Git

### 1. Clonar y configurar entorno

```bash
git clone git@github.com:mcsoler/adipa.git
cd adipa
cp .env.example .env
```

Editar `.env` con tus valores (mínimo revisar `OLLAMA_MODEL`).

### 2. Verificar que Ollama tiene un modelo

```bash
ollama list
# Si no hay modelos:
ollama pull llama3
```

### 3. Levantar todos los servicios

```bash
docker compose up --build
```

| Servicio | URL |
|----------|-----|
| Frontend | http://localhost:6000 |
| Backend API | http://localhost:5000 |
| API Docs (Swagger) | http://localhost:5000/docs |
| API Docs (ReDoc) | http://localhost:5000/redoc |
| PostgreSQL | localhost:5435 |

### 4. Detener

```bash
docker compose down
# Para eliminar también los datos de la base de datos:
docker compose down -v
```

### Servicios Docker

```yaml
# Resumen de puertos y dependencias
postgres  → :5435  (healthcheck: pg_isready)
backend   → :5000  (depends_on: postgres healthy)
frontend  → :6000  (nginx :81, depends_on: backend healthy)
ollama    → host:11434 (externo, via host.docker.internal)
```

---

## Variables de entorno

Copiar `.env.example` a `.env` y ajustar:

| Variable | Descripción | Default |
|----------|-------------|---------|
| `POSTGRES_USER` | Usuario de PostgreSQL | `adipa` |
| `POSTGRES_PASSWORD` | Contraseña de PostgreSQL | `adipa_secret` |
| `POSTGRES_DB` | Nombre de la base de datos | `adipa_db` |
| `DATABASE_URL` | URL completa de conexión async | `postgresql+asyncpg://...` |
| `OLLAMA_HOST` | URL de Ollama | `http://host.docker.internal:11434` |
| `OLLAMA_MODEL` | Modelo a usar | `llama3` |
| `CORS_ORIGINS` | Orígenes permitidos para CORS | `http://localhost:6000` |
| `MAX_FILE_SIZE_MB` | Tamaño máximo de archivo en MB | `50` |
| `VITE_API_URL` | URL del backend para el frontend | `http://localhost:5000` |

---

## API Reference

Base URL: `http://localhost:5000`

### Health

#### `GET /health`

Verifica que el servicio está activo.

**Response `200`**
```json
{ "status": "ok", "service": "adipa-backend" }
```

---

### Documents

#### `POST /api/v1/documents/upload`

Sube un documento para procesamiento. Retorna un `document_id` para usar en el siguiente paso.

**Request**
- Content-Type: `multipart/form-data`
- Body: `file` — archivo PDF, DOCX o XLSX (máx. 50 MB)

**Response `201`**
```json
{
  "document_id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "examen_psicologia.pdf",
  "status": "pending",
  "message": "Documento recibido. Llama a /process para extraer preguntas."
}
```

**Errores**

| Código | Causa |
|--------|-------|
| `413` | Archivo supera el límite de 50 MB |
| `415` | Formato no soportado (solo PDF, DOCX, XLSX) |
| `422` | No se envió ningún archivo |

---

### Extractions

#### `POST /api/v1/extractions/{document_id}/process`

Ejecuta el pipeline LangGraph sobre el documento y extrae las preguntas.

**Path params**
- `document_id` — UUID del documento obtenido en el paso anterior

**Request**
- Content-Type: `multipart/form-data`
- Body: `file` — el mismo archivo (necesario para el procesamiento)

**Response `200`**
```json
{
  "document_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "result": {
    "total_preguntas": 3,
    "preguntas": [
      {
        "numero": 1,
        "enunciado": "¿Cuál es el principal criterio diagnóstico del TAG?",
        "tipo": "seleccion_multiple",
        "alternativas": [
          { "letra": "A", "texto": "Alucinaciones visuales recurrentes" },
          { "letra": "B", "texto": "Preocupación excesiva difícil de controlar" }
        ],
        "respuesta_correcta": "B"
      }
    ]
  },
  "error": null
}
```

**Estados posibles en `status`**

| Estado | Descripción |
|--------|-------------|
| `completed` | Procesamiento exitoso |
| `failed` | Error durante la extracción |

**Errores**

| Código | Causa |
|--------|-------|
| `200` con `total_preguntas: 0` | No se detectaron preguntas |
| `503` | Ollama no disponible |

---

#### `GET /api/v1/extractions/{document_id}`

Recupera el resultado de una extracción ya procesada.

**Path params**
- `document_id` — UUID del documento

**Response `200`**
```json
{
  "document_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "result": { ... },
  "error": null
}
```

**Estados posibles**

| Estado | Descripción |
|--------|-------------|
| `completed` | Resultado disponible en `result` |
| `processing` | Aún en proceso |
| `failed` | Falló, ver campo `error` |
| `not_found` | `document_id` no existe |

---

### Flujo completo de uso

```bash
# 1. Subir documento
curl -X POST http://localhost:5000/api/v1/documents/upload \
  -F "file=@examen.pdf"
# → { "document_id": "abc-123", ... }

# 2. Procesar y extraer preguntas
curl -X POST http://localhost:5000/api/v1/extractions/abc-123/process \
  -F "file=@examen.pdf"
# → { "status": "completed", "result": { "total_preguntas": 5, ... } }

# 3. (Opcional) Consultar resultado guardado
curl http://localhost:5000/api/v1/extractions/abc-123
```

---

## Base de datos

### Diagrama de tablas

```
┌─────────────────────────────┐     ┌───────────────────────────────────┐
│         documents           │     │        extraction_results          │
├─────────────────────────────┤     ├───────────────────────────────────┤
│ id          UUID  PK        │──┐  │ id            UUID  PK            │
│ filename    VARCHAR(255)    │  └─►│ document_id   UUID  FK → documents│
│ file_type   VARCHAR(10)     │     │ result        JSONB               │
│ status      VARCHAR(20)     │     │ error_message TEXT  nullable      │
│ uploaded_at TIMESTAMPTZ     │     │ created_at    TIMESTAMPTZ         │
└─────────────────────────────┘     └───────────────────────────────────┘
```

### Tabla `documents`

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `id` | UUID | Identificador único (PK) |
| `filename` | VARCHAR(255) | Nombre original del archivo |
| `file_type` | VARCHAR(10) | `pdf`, `docx` o `xlsx` |
| `status` | VARCHAR(20) | `pending`, `processing`, `completed`, `failed` |
| `uploaded_at` | TIMESTAMPTZ | Fecha/hora de subida (auto) |

### Tabla `extraction_results`

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `id` | UUID | Identificador único (PK) |
| `document_id` | UUID | FK a `documents.id` (CASCADE DELETE) |
| `result` | JSONB | JSON completo con todas las preguntas extraídas |
| `error_message` | TEXT | Mensaje de error si falló (nullable) |
| `created_at` | TIMESTAMPTZ | Fecha/hora de creación (auto) |

### Estructura JSONB del campo `result`

```json
{
  "total_preguntas": 2,
  "preguntas": [
    {
      "numero": 1,
      "enunciado": "string",
      "tipo": "seleccion_multiple | verdadero_falso | desarrollo | emparejamiento",
      "alternativas": [
        { "letra": "A", "texto": "string" }
      ],
      "respuesta_correcta": "string | null"
    }
  ]
}
```

### Conexión directa a PostgreSQL

```bash
# Desde el host
psql -h localhost -p 5435 -U adipa -d adipa_db

# Consultas útiles
SELECT id, filename, status FROM documents ORDER BY uploaded_at DESC;
SELECT document_id, result->'total_preguntas' AS total FROM extraction_results;
```

---

## Flujo LangGraph

El pipeline es un `StateGraph` con 3 nodos y enrutamiento condicional:

```
START
  │
  ▼
extract_text_node
  │  Lee file_bytes + file_type del estado
  │  Usa ExtractorFactory para obtener el extractor correcto
  │  Escribe raw_text en el estado
  │
  ▼
process_with_llm_node
  │  Toma raw_text y lo envía a OllamaLLMService
  │  Construye prompt con SYSTEM + USER template
  │  Parsea la respuesta JSON del LLM
  │  En caso de LLMUnavailableError: reintenta hasta 2 veces
  │
  ├── [retry_count < 2 y error] ──► process_with_llm_node (reintento)
  │
  ▼
validate_output_node
  │  Valida el JSON contra ExtractionResultSchema (Pydantic)
  │  Si falla: modo rescate → filtra pregunta por pregunta
  │  Escribe validated_result en el estado
  │
  ▼
END
```

**WorkflowState (TypedDict)**

```python
{
  "file_bytes":       bytes,       # Contenido del archivo
  "file_type":        str,         # "pdf" | "docx" | "xlsx"
  "raw_text":         str,         # Texto extraído del documento
  "llm_result":       dict,        # JSON crudo del LLM
  "validated_result": dict,        # JSON validado con Pydantic
  "error":            str | None,  # Mensaje de error si hay fallo
  "retry_count":      int,         # Contador de reintentos LLM
}
```

---

## Principios SOLID aplicados

### S — Single Responsibility
Cada módulo tiene una única razón para cambiar:
- `PdfExtractor` solo extrae texto de PDFs
- `UploadDocumentUseCase` solo valida y persiste documentos
- `extract_text_node` solo extrae texto dentro del grafo

### O — Open/Closed
Agregar soporte para un nuevo formato (ej. PPTX) requiere:
1. Crear `PptxExtractor(ITextExtractor)` en `infrastructure/extractors/`
2. Registrarlo en `ExtractorFactory._registry`
3. Sin modificar ningún extractor existente

### L — Liskov Substitution
`PdfExtractor`, `DocxExtractor` y `XlsxExtractor` son intercambiables a través de `ITextExtractor`. El grafo LangGraph no sabe qué extractor usa.

### I — Interface Segregation
Interfaces pequeñas y enfocadas:
- `ITextExtractor`: solo `extract(bytes) → str`
- `ILLMService`: solo `process(str) → dict`
- `IDocumentRepository`: solo `save`, `find_by_id`, `update_status`

### D — Dependency Inversion
Los casos de uso dependen de interfaces, no de implementaciones concretas. El archivo `container.py` es el único lugar donde se cablea PostgreSQL/Ollama a las interfaces.

---

## Tests (TDD)

Metodología aplicada: **Red → Green → Refactor**

### Ejecutar tests del backend

```bash
cd backend
pip install -r requirements.txt
pytest -v
pytest --cov=app --cov-report=html  # con cobertura
```

### Ejecutar tests del frontend

```bash
cd frontend
npm install
npm test
npm run test:coverage
```

### Cobertura de tests

| Módulo | Tests | Ciclo TDD |
|--------|-------|-----------|
| Extractors (PDF/DOCX/XLSX) | 8 | Red→Green |
| Use Cases | 3 | Red→Green |
| LLM Service | 3 | Red→Green |
| LangGraph: extract_text_node | 4 | Red→Green |
| LangGraph: process_with_llm_node | 4 | Red→Green |
| LangGraph: validate_output_node | 4 | Red→Green |
| API: documents endpoint | 4 | Red→Green |
| API: extractions endpoint | 4 | Red→Green |
| Frontend: useDocumentUpload hook | 5 | Red→Green |
| Frontend: QuestionCard | 4 | Red→Green |
| Frontend: ErrorMessage | 3 | Red→Green |
| Frontend: FileDropzone | 4 | Red→Green |
| Frontend: DownloadButton | 3 | Red→Green |
| Frontend: ExtractionResultView | 4 | Red→Green |
| **Total** | **57** | |

---

## Desarrollo local sin Docker

### Backend

```bash
# Crear y activar entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

cd backend
pip install -r requirements.txt

# Copiar y editar variables de entorno
cp ../.env.example .env
# Ajustar DATABASE_URL para apuntar a PostgreSQL local

# Crear tablas (se hace automático al iniciar)
uvicorn app.main:app --reload --port 5000
```

### Frontend

```bash
cd frontend
npm install
npm run dev  # Inicia en http://localhost:6000
```

### PostgreSQL local

```bash
# Con Docker solo para la DB
docker run -d \
  --name adipa_postgres \
  -e POSTGRES_USER=adipa \
  -e POSTGRES_PASSWORD=adipa_secret \
  -e POSTGRES_DB=adipa_db \
  -p 5435:5432 \
  postgres:16-alpine
```

---

## Licencia

MIT
