# Referencia de la API

La especificación completa se genera en `/openapi.json`. Todos los endpoints siguientes usan el prefijo `/api/v1`; salvo autenticación, requieren `Authorization: Bearer <JWT>`.

## Autenticación

- `POST /auth/register`: crea un usuario (`name`, `email`, `password`).
- `POST /auth/login`: devuelve `access_token` y `token_type`.
- `GET /auth/me`: devuelve el usuario autenticado.

## Recursos

- `GET/POST /accounts`: lista o crea cuentas.
- `GET/PUT/DELETE /accounts/{account_id}`: consulta, modifica o elimina una cuenta.
- `GET/POST /categories`: lista o crea categorías.
- `GET/POST /budgets`: lista o crea presupuestos.
- `GET /budgets/{budget_id}/progress`: consulta el progreso de un presupuesto.
- `GET/POST /transactions`: lista o crea movimientos. El listado acepta `page`, `page_size`, `date_from`, `date_to`, `account_id`, `category_id`, `type`, `min_amount`, `max_amount` y `description`.
- `GET/PUT/DELETE /transactions/{transaction_id}`: consulta, modifica o elimina un movimiento.
- `GET /goals`: lista metas con `percentage` calculado.
- `POST /goals`: crea una meta (`name`, `target_amount`, `current_amount`, `target_date`).
- `POST /goals/{goal_id}/progress`: registra el nuevo `current_amount` y devuelve el porcentaje.
- `GET /dashboard/summary`: devuelve ingresos y gastos del mes, gastos por categoría, serie de los últimos seis meses y saldo total. Acepta `month` como fecha de referencia.
- `GET /export/transactions?format=csv`: descarga movimientos en CSV usando los mismos filtros del listado.

Las respuestas de validación son `422`; un recurso inexistente devuelve `404`; un token ausente, inválido o expirado devuelve `401`.
