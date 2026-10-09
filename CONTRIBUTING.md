# Contribuir a FinTrack

Gracias por contribuir a FinTrack. El proyecto es software libre bajo la licencia MIT.

## Flujo de trabajo

1. Crea una rama descriptiva desde la rama principal.
2. Mantén los cambios enfocados y respeta la arquitectura `api -> services -> repositories`.
3. No incluyas secretos, archivos `.env`, datos financieros reales ni credenciales en commits.
4. Añade o actualiza pruebas para cada comportamiento nuevo.
5. Ejecuta las validaciones locales antes de abrir el pull request.

## Validaciones locales

Desde PowerShell:

```powershell
Set-Location backend
.\venv\Scripts\python.exe -m pytest -q
.\venv\Scripts\python.exe -m compileall -q app tests
Set-Location ..
Get-ChildItem frontend\js -Recurse -Filter *.js | ForEach-Object { node --check $_.FullName }
```

Los cambios que afectan PostgreSQL deben probarse además contra una instancia de PostgreSQL con los scripts de `backend/sql/` aplicados y `FINTRACK_RLS_TESTS=1`.

## Pull requests

Describe el problema, el comportamiento esperado, las decisiones relevantes y las pruebas ejecutadas. Las contribuciones deben mantener los mensajes de usuario en español y los identificadores y comentarios de código en inglés.
