# FinTrack: instrucciones para Copilot

## Proyecto
App full-stack de finanzas personales. Backend FastAPI (Python 3.13), PostgreSQL con Row Level Security, frontend en HTML/CSS/JavaScript ES6 puro con Chart.js. La documentación está en /docs: lee architecture.md, documentation.md y security.md antes de cambiar nada.

## Arquitectura (obligatoria)
- backend/app/ tiene: api (routers), schemas, services, repositories, models, core.
- Dependencias en una sola dirección: api -> services -> repositories -> base de datos.
- Router: solo valida entrada y delega. Service: reglas de negocio. Repository: único que toca la base de datos.
- Cada router define solo su prefijo (por ejemplo /accounts) y se registra en app/main.py con include_router(prefix="/api/v1").
- Endpoints síncronos (def). SQLAlchemy 2.0 (Mapped, mapped_column), Pydantic v2, psycopg 3, PyJWT, passlib con bcrypt (bcrypt<4.1 fijado en requirements.txt).
- Patrón de referencia: copia la estructura del recurso accounts (models/account.py, schemas/account.py, repositories/account_repository.py, services/account_service.py, api/accounts.py).

## Base de datos y RLS
- El esquema se crea con scripts SQL que ejecuto a mano en pgAdmin (sin Alembic). Guarda cada script numerado en backend/sql/.
- Toda tabla con datos de un usuario lleva: user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE, ENABLE ROW LEVEL SECURITY y una política con USING y WITH CHECK sobre user_id = current_setting('app.current_user_id')::uuid.
- La tabla users NO tiene RLS (el login busca por email antes de saber quién es el usuario).
- La app se conecta con el rol fintrack_app (NOSUPERUSER, NOBYPASSRLS), nunca con postgres, porque los superusuarios se saltan RLS. No cambies el usuario de DATABASE_URL.
- En cada operación del repository, lo primero: SELECT set_config('app.current_user_id', :uid, true). No uses SET LOCAL con parámetros (falla). Ese valor dura solo la transacción: haz flush y refresh ANTES del commit. La sesión usa expire_on_commit=False.
- Modelos: id con server_default=text("gen_random_uuid()") y created_at con server_default=func.now(). SQLAlchemy no lee los defaults de la base de datos por sí solo.
- Dinero: NUMERIC(14,2) y Decimal, nunca float.

## Convenciones
- Identificadores y comentarios de código en inglés. Mensajes de error al usuario en español.
- Nunca confíes en un user_id enviado por el cliente: sale siempre de get_current_user.
- Las operaciones sobre varias filas (transferencias) van en una sola transacción.
- Validación con Pydantic (Literal para tipos, Field(gt=0) para montos). EmailStr rechaza dominios .test.
- Secretos solo en .env (ignorado por git). Mantén backend/.env.example actualizado, sin valores reales.
- Entorno Windows con PowerShell: da los comandos en sintaxis PowerShell.
- Documentación sin emojis, en tono profesional. Si cambias el modelo de datos o los endpoints, actualiza docs/documentation.md. No inventes funcionalidades fuera del alcance.

## Pruebas
pytest. Services con repository simulado, endpoints con TestClient. Incluye siempre una prueba de aislamiento entre dos usuarios.