# ProDig Architect Engine

Este es el cerebro de consultoría en IA de ProDig. Una solución integral para la captura de conocimientos, consulta arquitectónica y exploración tecnológica.

## Estructura del Proyecto

- `index.html`: Interfaz principal.
- `index.css`: Sistema de diseño premium.
- `app.js`: Lógica de la aplicación y conectividad con APIs.
- `api/`:
  - `chat.py`: Motor de consultoría con Groq y RAG local.
  - `harvest.py`: Cosechador de noticias con Brave Search.
  - `tech.py`: API para el repositorio de tecnologías.

## Tecnologías

- **Frontend**: HTML5, Vanilla CSS3, JavaScript (ES6+).
- **IA**: Groq API (Llama 3.3 70B), RAG con contexto local.
- **Búsqueda**: Brave Search API.
- **Despliegue**: Vercel (Python Serverless Functions).

## Configuración en Vercel

Para que el proyecto funcione, debes añadir las siguientes variables de entorno en tu panel de Vercel:

1. `GROQ_API_KEY`: Tu clave de Groq (console.groq.com).
2. `BRAVE_API_KEY`: Tu clave de Brave Search (api.search.brave.com).

## Roadmap

1. [x] Diseño de Interfaz Premium.
2. [x] Implementación del Harvester (API Brave).
3. [x] Integración de Groq para Consultoría (RAG).
4. [x] Visual Explorer dinámico desde CSV.
5. [ ] Tech Mixer para MVPs.
