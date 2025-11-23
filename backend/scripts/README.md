# Backend Scripts

Scripts útiles para desarrollo y mantenimiento de la aplicación.

## Seed Scripts

### ⚡ Quick Start - Seed All

Ejecuta todos los seeds de una vez:

```bash
# Desde la raíz del backend
python -m scripts.seed_all
```

Este script ejecutará:

- ✅ Templates seed
- ✅ Job offerings seed

---

### Job Offerings Seed

Inserta ofertas de trabajo de ejemplo en la base de datos.

**Ejecutar:**

```bash
# Desde la raíz del backend
python -m scripts.seed_job_offerings
```

**Contenido:**

- 10 ofertas de trabajo reales de empresas chilenas
- Incluye: frontend, backend, fullstack positions
- Empresas: Bruno Fritsch, BairesDev, AgendaPro, Uber, Coderhub, Grupo Falabella, NeuralWorks, BC Tecnología, Deloitte, Sezzle
- Datos: descripción, requisitos, responsabilidades, ubicación, salario (cuando aplica)

### Templates Seed

Inserta plantillas de CV en la base de datos.

**Ejecutar:**

```bash
# Desde la raíz del backend
python -m scripts.seed_templates
```

## Testing Scripts

### Test Extraction E2E

Prueba end-to-end del servicio de extracción de perfiles.

```bash
python -m scripts.test_extraction_e2e
```

### Test Extraction Simple

Prueba simple del servicio de extracción.

```bash
python -m scripts.test_extraction_simple
```

### Test Render

Prueba el renderizado de CVs con Typst.

```bash
python -m scripts.test_render
```

### Demo LLM

Demostración del servicio LLM.

```bash
python -m scripts.demo_llm
```

## Notas

- Todos los scripts deben ejecutarse desde la raíz del directorio `backend`
- Asegúrate de que la base de datos esté configurada y corriendo
- Verifica que las variables de entorno estén configuradas en el archivo `.env`
