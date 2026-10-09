# FinTrack

> Plataforma full-stack de finanzas personales, moderna y de código abierto.

FinTrack permite a estudiantes, profesionales y freelancers tomar el control real de sus finanzas: registrar ingresos, gastos y transferencias, administrar múltiples cuentas y categorías, definir presupuestos y metas de ahorro, y visualizar sus hábitos de consumo mediante dashboards interactivos.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6-F7DF1E?logo=javascript&logoColor=black)
![Pytest](https://img.shields.io/badge/Tested%20with-Pytest-0A9EDC?logo=pytest&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## Tabla de contenido

1. [Descripción general](#descripción-general)
2. [Características principales](#características-principales)
3. [Tecnologías utilizadas](#tecnologías-utilizadas)
4. [Arquitectura del proyecto](#arquitectura-del-proyecto)
5. [Instalación local](#instalación-local)
6. [Variables de entorno](#variables-de-entorno)
7. [Ejecución del backend](#ejecución-del-backend)
8. [Ejecución del frontend](#ejecución-del-frontend)
9. [Pruebas](#pruebas)
10. [Despliegue](#despliegue)
11. [Roadmap futuro](#roadmap-futuro)
12. [Capturas sugeridas](#capturas-sugeridas)
13. [Documentación adicional](#documentación-adicional)
14. [Licencia](#licencia)

---

## Descripción general

**FinTrack** es una aplicación web full-stack orientada a la gestión de finanzas personales. Su objetivo es ofrecer una herramienta simple, rápida y segura para que cualquier persona pueda entender en qué gasta su dinero, planificar presupuestos realistas y avanzar hacia sus metas de ahorro, sin depender de hojas de cálculo dispersas.

El proyecto está construido siguiendo buenas prácticas de ingeniería de software: separación de responsabilidades en capas (routers, services, repositories), autenticación propia con JWT, aislamiento de datos a nivel de base de datos mediante Row Level Security, y un frontend ligero sin frameworks pesados, priorizando el dominio real de las tecnologías utilizadas por encima de servicios gestionados que oculten su funcionamiento interno.

## Características principales

- **Autenticación segura** con JWT y hashing de contraseñas (Passlib/Bcrypt).
- **Gestión de transacciones**: registro de ingresos, gastos y transferencias entre cuentas.
- **Múltiples cuentas y categorías**, totalmente personalizables.
- **Presupuestos mensuales** con seguimiento de cumplimiento.
- **Metas de ahorro** con control de avance.
- **Dashboards financieros** con gráficas interactivas (Chart.js) sobre hábitos de consumo.
- **Búsqueda y filtrado avanzado** de movimientos (por fecha, cuenta, categoría, tipo, monto).
- **Exportación de información financiera**.
- **Modo oscuro** y enfoque en accesibilidad.
- **Aislamiento de datos por usuario** garantizado a nivel de base de datos (Row Level Security), no solo a nivel de aplicación.

## Tecnologías utilizadas

| Capa | Tecnología |
|---|---|
| Backend | Python + [FastAPI](https://fastapi.tiangolo.com/) |
| Autenticación | JWT + [Passlib](https://passlib.readthedocs.io/)/Bcrypt |
| Base de datos | PostgreSQL con Row Level Security (RLS) |
| Base de datos en producción | [Neon](https://neon.tech/) (Postgres serverless) |
| Frontend | HTML5, CSS3, JavaScript (ES6, módulos nativos) |
| Comunicación API | Fetch API |
| Visualización de datos | [Chart.js](https://www.chartjs.org/) |
| Testing | [Pytest](https://docs.pytest.org/) |
| Despliegue | [Render](https://render.com/) (backend + frontend estático) |

## Arquitectura del proyecto

El backend sigue una arquitectura por capas, que separa claramente responsabilidades y facilita el mantenimiento y las pruebas:

```
Cliente (Frontend)
        |
        v
   +---------+
   | Routers |   Define endpoints, valida entrada (Pydantic), maneja HTTP
   +----+----+
        |
        v
   +----------+
   | Services |   Lógica de negocio: reglas, validaciones, orquestación
   +----+-----+
        |
        v
   +--------------+
   | Repositories |   Acceso a datos: consultas SQL/ORM, sin lógica de negocio
   +------+-------+
          |
          v
   PostgreSQL (con Row Level Security)
```

Principios clave:
- Los routers no contienen lógica de negocio; solo reciben la petición, validan el esquema y delegan al service correspondiente.
- Los services concentran las reglas del dominio (por ejemplo: una transferencia debe afectar el saldo de dos cuentas de forma atómica).
- Los repositories son los únicos responsables de hablar con la base de datos.
- RLS actúa como una segunda barrera de seguridad: incluso si hubiera un error de lógica en el backend, la base de datos rechaza cualquier acceso a filas que no pertenezcan al usuario autenticado.

### Estructura de carpetas sugerida

```
fintrack/
├── backend/
│   ├── app/
│   │   ├── api/                # Routers (endpoints por versión/módulo)
│   │   ├── core/                # Configuración, seguridad, dependencias
│   │   ├── schemas/             # Esquemas Pydantic (entrada/salida)
│   │   ├── services/            # Lógica de negocio
│   │   ├── repositories/        # Acceso a datos
│   │   ├── models/               # Modelos de base de datos
│   │   └── main.py               # Punto de entrada de FastAPI
│   ├── tests/                    # Pruebas con Pytest
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── css/
│   ├── js/
│   │   ├── modules/               # Módulos ES6 (auth, dashboard, transactions...)
│   │   └── main.js
│   └── index.html
├── docs/
│   ├── architecture.md
│   ├── case-study.md
│   ├── documentation.md
│   ├── legal.md
│   ├── security.md
│   ├── user-guide.md
│   └── screenshots/
├── .gitignore
├── LICENSE
└── README.md
```

Nota: ajusta esta estructura a la organización real de tu repositorio.

## Instalación local

### Requisitos previos
- Python 3.13
- PostgreSQL instalado localmente (o una instancia en la nube, como Neon)
- Git

### Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/fintrack.git
cd fintrack
```

### Configurar el backend

```bash
cd backend
python -m venv venv

# Activar entorno virtual en PowerShell
.\venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

## Variables de entorno

Crea un archivo `.env` dentro de `backend/` basado en `.env.example`:

```env
# Base de datos
DATABASE_URL=postgresql://usuario:password@localhost:5432/fintrack

# Seguridad / JWT
JWT_SECRET_KEY=tu_clave_secreta_super_segura
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Entorno
ENVIRONMENT=development

# CORS
CORS_ORIGINS=http://localhost:5500,http://127.0.0.1:5500
```

Nota importante: nunca subas tu archivo `.env` real al repositorio. Asegúrate de incluirlo en `.gitignore`.

## Inicializar PostgreSQL

Aplica los scripts numerados desde `backend/sql/` en orden, conectado a la base de datos `fintrack`:

1. `000_create_users_and_accounts.sql` crea las tablas base y RLS de cuentas.
2. `001_create_categories.sql` a `004_create_savings_goals.sql` crean el resto del modelo y sus políticas RLS.
3. `005_grant_app_permissions.sql` concede permisos al rol `fintrack_app`.

El rol de aplicación debe ser `NOSUPERUSER` y `NOBYPASSRLS`. Nunca uses el usuario administrador de PostgreSQL en `DATABASE_URL`.

## Ejecución del backend

```bash
cd backend
uvicorn app.main:app --reload
```

- La API quedará disponible en: `http://127.0.0.1:8000`
- Documentación interactiva automática (Swagger UI): `http://127.0.0.1:8000/docs`
- Documentación alternativa (ReDoc): `http://127.0.0.1:8000/redoc`

## Ejecución del frontend

Al ser HTML, CSS y JavaScript puro (sin build step), puedes servirlo de cualquiera de estas formas:

**Opción 1 — Extensión Live Server (VS Code):**
Clic derecho sobre `frontend/index.html` y seleccionar "Open with Live Server".

**Opción 2 — Servidor HTTP simple con Python:**
```bash
cd frontend
python -m http.server 5500
```
Luego abre `http://127.0.0.1:5500` en tu navegador.

La URL base se configura en un solo lugar, `frontend/js/modules/api.js`, mediante `API_BASE_URL`. Por defecto apunta a `http://127.0.0.1:8000/api/v1`.

## Pruebas

El proyecto usa Pytest para pruebas automatizadas del backend.

```bash
cd backend
pytest
```

Para ver el detalle de cada prueba:
```bash
pytest -v
```

Para medir cobertura de código (requiere `pytest-cov`):
```bash
pytest --cov=app --cov-report=term-missing
```

La prueba de aislamiento RLS se omite si no se define `FINTRACK_RLS_TESTS=1`; para considerarla válida hay que ejecutarla contra PostgreSQL con los scripts aplicados.

## Código abierto

FinTrack se distribuye bajo la licencia MIT. Las contribuciones están descritas en [CONTRIBUTING.md](CONTRIBUTING.md). No incluyas secretos, datos reales ni archivos `.env` en pull requests.

Cada push y pull request ejecuta automáticamente las pruebas Python y la comprobación de sintaxis JavaScript mediante [CI](.github/workflows/ci.yml).

## Despliegue

FinTrack está pensado para desplegarse de forma gratuita usando:

| Componente | Servicio |
|---|---|
| Backend (API FastAPI) | [Render](https://render.com/) — Web Service |
| Frontend (estático) | [Render](https://render.com/) — Static Site |
| Base de datos | [Neon](https://neon.tech/) — PostgreSQL serverless |

Pasos generales:

1. Crea una base de datos en Neon y copia la cadena de conexión (`DATABASE_URL`).
2. En Render, crea un nuevo Web Service apuntando a la carpeta `backend/`, define el comando de inicio (`uvicorn app.main:app --host 0.0.0.0 --port $PORT`) y agrega las variables de entorno (`DATABASE_URL`, `JWT_SECRET_KEY`, etc.).
3. En Render, crea un Static Site apuntando a la carpeta `frontend/`.
4. Actualiza la URL base del backend en el frontend para que apunte al dominio del Web Service desplegado.
5. Configura `CORS_ORIGINS` en el backend para permitir el dominio del frontend en producción.

## Roadmap futuro

- [ ] Notificaciones y alertas de presupuesto (por correo o push).
- [ ] Exportación de reportes en PDF.
- [ ] Soporte multi-moneda.
- [ ] Categorización automática de gastos.
- [ ] Aplicación móvil (PWA).
- [ ] Panel de reportes comparativos mes a mes.
- [ ] Internacionalización (i18n).

Nota: estas son ideas sugeridas; ajústalas según la prioridad real de tu proyecto.

## Capturas sugeridas

Para enriquecer este README, considera agregar capturas de pantalla en `docs/screenshots/` y enlazarlas así:

```markdown
### Dashboard financiero
![Dashboard](docs/screenshots/dashboard.png)

### Registro de transacciones
![Transacciones](docs/screenshots/transacciones.png)

### Modo oscuro
![Modo oscuro](docs/screenshots/modo-oscuro.png)
```

Capturas recomendadas: pantalla de login, dashboard principal con gráficas, formulario de nueva transacción, vista de presupuestos y metas de ahorro, e interfaz en modo oscuro.

## Documentación adicional

- [Arquitectura del proyecto](docs/architecture.md)
- [Documentación técnica y de producto](docs/documentation.md)
- [Seguridad](docs/security.md)
- [Legal](docs/legal.md)
- [Caso de estudio](docs/case-study.md)
- [Manual de usuario](docs/user-guide.md)

## Licencia

Este proyecto está bajo la licencia MIT. Puedes usar, modificar y distribuir el código libremente, dando el crédito correspondiente.

```
MIT License

Copyright (c) 2026 Mariana Vargas Ospina

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

Desarrollado por Mariana Vargas Ospina.
