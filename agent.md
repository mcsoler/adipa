## El desafío

Construye una aplicación web que permita subir un documento (PDF, Word o Excel) y retorne automáticamente las preguntas y alternativas detectadas, estructuradas en un JSON estandarizado.

### Ejemplo de salida esperada

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

---

## Requerimientos

1. **Subida de archivos** — soportar PDF, `.docx` y `.xlsx`.
2. **Procesamiento** — extraer texto e identificar preguntas, tipo (selección múltiple, V/F, desarrollo, emparejamiento) y alternativas.
3. **Respuesta estructurada** — retornar el JSON según el esquema de arriba. Si la respuesta correcta está indicada en el documento, incluirla.
4. **Interfaz** — UI donde el usuario adjunta el archivo, inicia el procesamiento y visualiza o descarga el resultado.
5. **Manejo de errores** — informar si no se detectan preguntas, el formato es inválido o ocurre un error.

---

## Stack

| Capa | Requerido | Decisión libre |
|---|---|---|
| Frontend | React o Next.js | Estilos, librerías UI, tailwind, buen manejo en la gestion de estado | metodologia TDD | Utilizar puerto 6000 
| Backend | Python · FastAPI | Estructura, validación, logging | Docs | metodologia TDD | Utilizar puerto 5000 
| Base de datos | PostGreSql | ORM | Utilizar puerto 5435
| LLM / Extracción | landGraph | Ollama esta funcionando en el puerto 11434 y ya tiene modelos utiliza ese|
| Deploy | Docker compose  | 





