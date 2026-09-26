# Documentación Legal — FinTrack

**Última actualización:** 25/09/2026
**Responsable del tratamiento:** Mariana Vargas Ospina
**Contacto:** <marianavargasospina@gmail.com>

---

## Tabla de contenido

1. [Política de Privacidad](#1-política-de-privacidad)
2. [Política de Cookies](#2-política-de-cookies)
3. [Aviso de Protección de Datos](#3-aviso-de-protección-de-datos)
4. [Términos y Condiciones](#4-términos-y-condiciones)
5. [Política de Propiedad Intelectual](#5-política-de-propiedad-intelectual)
6. [Política de Seguridad](#6-política-de-seguridad)
7. [Descargo de Responsabilidad Financiera](#7-descargo-de-responsabilidad-financiera)
8. [Política de Eliminación de Datos](#8-política-de-eliminación-de-datos)
9. [Aviso de Copyright](#9-aviso-de-copyright)
10. [Legislación Aplicable](#10-legislación-aplicable)
11. [Procedimiento de Atención de Solicitudes de Usuarios](#11-procedimiento-de-atención-de-solicitudes-de-usuarios)
12. [Consentimiento Informado para el Tratamiento de Datos](#12-consentimiento-informado-para-el-tratamiento-de-datos)

---

## 1. Política de Privacidad

### 1.1 Responsable del tratamiento

Mariana Vargas Ospina, con domicilio en Sonsón, Colombia y correo de contacto <marianavargasospina@gmail.com>
, es la responsable del tratamiento de los datos personales recopilados a través de FinTrack (en adelante, "la Plataforma").

### 1.2 Datos que se recopilan

- **Datos de registro:** nombre, correo electrónico, contraseña (almacenada mediante hashing con bcrypt, nunca en texto plano).
- **Datos financieros ingresados por el usuario:** ingresos, gastos, transferencias, cuentas, categorías, presupuestos y metas de ahorro.
- **Datos técnicos:** dirección IP, tipo de dispositivo y navegador, registros de acceso (logs) con fines de seguridad.
- **Datos de uso:** interacción con el dashboard, filtros de búsqueda utilizados, preferencias de interfaz (por ejemplo, modo oscuro).

FinTrack no solicita ni almacena números de tarjetas de crédito, claves bancarias ni credenciales de acceso a entidades financieras; los movimientos se registran manualmente por el usuario.

### 1.3 Finalidad del tratamiento

Los datos se utilizan para: (i) crear y administrar la cuenta del usuario; (ii) prestar las funcionalidades de la Plataforma(registro de transacciones, presupuestos, dashboards); (iii) garantizar la seguridad de la cuenta; (iv) cumplir obligaciones legales aplicables; y (v) mejorar la Plataforma.

### 1.4 Base legal / consentimiento

El tratamiento se realiza con el consentimiento previo, expreso e informado del titular, otorgado al momento del registro (ver sección 12), conforme a la Ley 1581 de 2012 y el Decreto 1377 de 2013 de Colombia. Para usuarios ubicados en la Unión Europea, el tratamiento se ampara adicionalmente en las bases legales previstas por el Reglamento General de Protección de Datos (GDPR).

### 1.5 Medidas de protección de datos

FinTrack implementa: autenticación mediante JWT, hashing de contraseñas con Passlib/Bcrypt, cifrado en tránsito mediante HTTPS/TLS, y Row Level Security (RLS) a nivel de base de datos, que impide que un usuario acceda a los datos de otro incluso ante errores en la capa de aplicación.

### 1.6 Encargados del tratamiento y proveedores

Para operar la Plataforma se utilizan los siguientes proveedores de infraestructura, que actúan como encargados del tratamiento: Render (alojamiento del backend y frontend) y Neon (base de datos PostgreSQL en producción). Estos proveedores pueden alojar datos en servidores ubicados fuera del país del usuario; en tal caso, se adoptan las garantías contractuales y técnicas correspondientes.

### 1.7 Derechos del titular

El usuario puede ejercer en cualquier momento los derechos de acceso, actualización, rectificación, cancelación y oposición sobre sus datos personales (derechos ARCO), así como solicitar prueba de la autorización otorgada, conforme al procedimiento descrito en la sección 11.

### 1.8 Conservación de datos

Los datos se conservarán mientras la cuenta permanezca activa y durante el tiempo adicional que exijan obligaciones legales o contractuales. Ver la Política de Eliminación de Datos (sección 8) para los plazos de eliminación tras el cierre de cuenta.

### 1.9 Menores de edad

FinTrack no está dirigido a menores de edad. No se recopila conscientemente información de personas menores de 18 años.

### 1.10 Cambios a esta política

Esta política puede actualizarse periódicamente. Los cambios sustanciales se notificarán a los usuarios por correo electrónico o mediante aviso dentro de la Plataforma.

---

## 2. Política de Cookies

### 2.1 Qué son las cookies

Las cookies son pequeños archivos que un sitio web almacena en el navegador del usuario para recordar información entre sesiones.

### 2.2 Uso de cookies en FinTrack

FinTrack utiliza principalmente almacenamiento local del navegador para mantener la sesión autenticada (token JWT) en lugar de cookies de terceros. En caso de incorporarse cookies en el futuro, estas se clasificarán como:

- **Cookies esenciales:** necesarias para el funcionamiento básico de la sesión y la autenticación.
- **Cookies de preferencia:** para recordar configuraciones como el modo oscuro.
- **Cookies analíticas (si se incorporan):** para entender el uso agregado de la Plataforma, siempre con consentimiento previo cuando la normativa aplicable lo exija.

### 2.3 Gestión de cookies

El usuario puede eliminar o bloquear cookies desde la configuración de su navegador. Bloquear cookies esenciales puede afectar el funcionamiento de la Plataforma, incluida la posibilidad de mantener la sesión iniciada.

### 2.4 Cambios

Esta política se actualizará si se modifica el uso de cookies o tecnologías similares en la Plataforma.

---

## 3. Aviso de Protección de Datos

En cumplimiento del Decreto 1377 de 2013 (Colombia), se informa de manera resumida al titular de los datos:

- **Responsable:** Mariana Vargas Ospina.
- **Finalidad:** gestión de la cuenta de usuario y prestación de las funcionalidades de FinTrack (transacciones, presupuestos, metas de ahorro, dashboards).
- **Derechos:** acceso, actualización, rectificación, cancelación y oposición, ejercibles mediante el procedimiento de la sección 11.
- **Carácter facultativo o no de las respuestas:** el suministro de los datos solicitados en el registro es necesario para poder usar la Plataforma; los campos opcionales se identifican como tales en el formulario correspondiente.
- **Documento completo:** la Política de Privacidad (sección 1) contiene el detalle completo del tratamiento.

Este aviso debe presentarse al usuario en el punto de recolección de datos (por ejemplo, en el formulario de registro), con un enlace a la Política de Privacidad completa.

---

## 4. Términos y Condiciones

### 4.1 Aceptación

El acceso y uso de FinTrack implica la aceptación plena de estos Términos y Condiciones. Si el usuario no está de acuerdo, debe abstenerse de utilizar la Plataforma.

### 4.2 Descripción del servicio

FinTrack es una plataforma de gestión de finanzas personales que permite registrar ingresos, gastos y transferencias, administrar cuentas y categorías, definir presupuestos y metas de ahorro, y visualizar estadísticas mediante dashboards.

### 4.3 Registro de cuenta

El usuario debe proporcionar información veraz y actualizada al registrarse, ser mayor de edad según la legislación aplicable, y es responsable de mantener la confidencialidad de sus credenciales de acceso.

### 4.4 Uso aceptable

El usuario se compromete a no utilizar la Plataforma para fines ilícitos, no intentar vulnerar las medidas de seguridad, no realizar ingeniería inversa del software, y no utilizar la información de otros usuarios sin autorización.

### 4.5 Disponibilidad del servicio

FinTrack se ofrece "tal cual" y "según disponibilidad". No se garantiza disponibilidad ininterrumpida ni ausencia de errores; se realizarán esfuerzos razonables para mantener la Plataforma operativa y notificar interrupciones programadas.

### 4.6 Limitación de responsabilidad

En la máxima medida permitida por la ley aplicable, Mariana Vargas Ospina no será responsable por daños indirectos, pérdida de datos o decisiones financieras tomadas por el usuario con base en la información de la Plataforma (ver Descargo de Responsabilidad Financiera, sección 7).

### 4.7 Terminación

El usuario puede cerrar su cuenta en cualquier momento. Mariana Vargas Ospina podrá suspender o terminar cuentas que incumplan estos términos, previa notificación cuando sea razonablemente posible.

### 4.8 Modificaciones

Estos términos podrán actualizarse; los cambios sustanciales se notificarán con antelación razonable.

### 4.9 Ley aplicable

Ver sección 10 (Legislación Aplicable).

---

## 5. Política de Propiedad Intelectual

### 5.1 Titularidad de la Plataforma

El código fuente, diseño de interfaz, marca "FinTrack", logotipos y demás elementos de la Plataforma son propiedad de Mariana Vargas Ospina, salvo los componentes de terceros bajo licencia de código abierto utilizados en su construcción (FastAPI, PostgreSQL, Chart.js, entre otros), que se rigen por sus respectivas licencias.

### 5.2 Propiedad de los datos del usuario

El usuario conserva la titularidad de la información financiera que ingresa en la Plataforma. FinTrack no reclama propiedad sobre dichos datos y los utiliza únicamente para prestar el servicio, conforme a la Política de Privacidad.

### 5.3 Uso permitido

Se autoriza el uso personal y no comercial de la Plataforma conforme a estos términos. Queda prohibida la reproducción, distribución o modificación del software sin autorización expresa, salvo que el código se publique bajo una licencia de código abierto específica.

### 5.4 Reclamos por infracción

Cualquier reclamo relacionado con presunta infracción de derechos de propiedad intelectual puede dirigirse a <marianavargasospina@gmail.com>, indicando la obra presuntamente infringida y la ubicación del contenido cuestionado.

---

## 6. Política de Seguridad

### 6.1 Medidas técnicas

- Autenticación basada en JSON Web Tokens (JWT) con expiración configurable.
- Almacenamiento de contraseñas mediante hashing con Passlib/Bcrypt; nunca en texto plano.
- Row Level Security (RLS) en PostgreSQL, que restringe el acceso a los datos exclusivamente al usuario propietario, como capa adicional independiente de la lógica de aplicación.
- Comunicación cifrada mediante HTTPS/TLS entre el cliente y el servidor.
- Separación de credenciales sensibles (claves, cadenas de conexión) mediante variables de entorno, nunca incluidas en el código fuente.

### 6.2 Medidas organizativas

Acceso restringido a los sistemas de producción, revisión periódica de dependencias y prácticas de desarrollo seguro durante el ciclo de vida del proyecto.

### 6.3 Gestión de incidentes

Ante una eventual vulneración de seguridad que afecte datos personales, se notificará a los usuarios afectados y, cuando la normativa lo exija, a la autoridad de control competente (en Colombia, la Superintendencia de Industria y Comercio), dentro de los plazos legales aplicables.

### 6.4 Reporte responsable de vulnerabilidades

Si detectas una vulnerabilidad de seguridad en FinTrack, repórtala de forma responsable a <marianavargasospina@gmail.com> antes de divulgarla públicamente, para permitir su corrección oportuna.

---

## 7. Descargo de Responsabilidad Financiera

FinTrack es una herramienta de organización y visualización de finanzas personales. No constituye asesoría financiera, contable, tributaria ni de inversión de ningún tipo. La información, cálculos y proyecciones mostrados en la Plataforma se basan exclusivamente en los datos ingresados por el usuario y pueden contener errores u omisiones.

Toda decisión financiera tomada con base en la información de FinTrack es responsabilidad exclusiva del usuario. Se recomienda consultar a un profesional certificado (contador, asesor financiero) antes de tomar decisiones financieras relevantes.

---

## 8. Política de Eliminación de Datos

### 8.1 Derecho a la eliminación

El usuario puede solicitar en cualquier momento la eliminación de su cuenta y de los datos personales asociados, conforme a los derechos ARCO reconocidos en la Política de Privacidad.

### 8.2 Procedimiento

La solicitud puede realizarse desde la configuración de la cuenta dentro de la Plataforma o mediante correo electrónico a <marianavargasospina@gmail.com>, indicando el correo asociado a la cuenta.

### 8.3 Plazos

La solicitud se atenderá dentro de un plazo máximo de 15 días hábiles, conforme a los términos previstos por la normativa colombiana de protección de datos, salvo prórroga justificada que será comunicada al usuario.

### 8.4 Excepciones

Determinada información podrá conservarse por el tiempo adicional que exijan obligaciones legales, contables o de defensa ante reclamaciones, incluso después de eliminada la cuenta.

### 8.5 Eliminación en copias de respaldo

Los datos eliminados de los sistemas activos se removerán de las copias de respaldo dentro de un plazo razonable, conforme al ciclo de rotación de dichas copias.

---

## 9. Aviso de Copyright

© 2026 Mariana Vargas Ospina. Todos los derechos reservados.

El código fuente, la documentación, el diseño de interfaz y la marca "FinTrack" están protegidos por la legislación de derechos de autor aplicable, incluida la Ley 23 de 1982 de Colombia. Queda prohibida la reproducción total o parcial de estos elementos sin autorización previa y por escrito del titular, salvo lo dispuesto en la Política de Propiedad Intelectual (sección 5) respecto de componentes de código abierto.

Para reportar un presunto uso no autorizado, escribe a [correo de contacto].

---

## 10. Legislación Aplicable

### 10.1 Marco legal principal

Estos documentos y el uso de FinTrack se rigen, con carácter general, por la legislación de la República de Colombia, incluyendo de forma enunciativa:

- Ley 1581 de 2012 y Decreto 1377 de 2013 — protección de datos personales (Habeas Data).
- Ley 23 de 1982 — derechos de autor.
- Ley 527 de 1999 — comercio electrónico y mensajes de datos.
- Ley 1273 de 2009 — protección de la información y de los datos (delitos informáticos).

### 10.2 Usuarios en otras jurisdicciones

Si FinTrack es utilizado por personas ubicadas en la Unión Europea, resultará aplicable adicionalmente el Reglamento General de Protección de Datos (GDPR); si es utilizado por residentes de California (Estados Unidos), podrá aplicar la California Consumer Privacy Act (CCPA). En caso de conflicto entre normativas, se aplicará la disposición que otorgue mayor protección al titular de los datos, sin perjuicio de las obligaciones legales específicas de cada jurisdicción.

### 10.3 Jurisdicción

Para la resolución de cualquier controversia derivada del uso de la Plataforma, las partes se someten a los jueces y tribunales competentes de Sonsón, Colombia, salvo que la normativa de protección al consumidor aplicable disponga un fuero distinto de carácter irrenunciable.

---

## 11. Procedimiento de Atención de Solicitudes de Usuarios

### 11.1 Canal de atención

Las solicitudes relacionadas con el ejercicio de derechos ARCO (acceso, rectificación, actualización, supresión y oposición) deben dirigirse a <marianavargasospina@gmail.com>.

### 11.2 Información requerida

La solicitud debe incluir: nombre completo, correo electrónico asociado a la cuenta, descripción clara de la solicitud, y documento de identificación cuando sea necesario para verificar la identidad del solicitante.

### 11.3 Verificación de identidad

Antes de dar trámite a la solicitud, se podrá requerir información adicional razonable para confirmar que quien solicita es efectivamente el titular de los datos.

### 11.4 Plazos de respuesta

- Consultas: se atenderán dentro de un plazo máximo de 10 días hábiles.
- Reclamos (rectificación, actualización, supresión): se atenderán dentro de un plazo máximo de 15 días hábiles.

Si no es posible atender la solicitud dentro de dichos plazos, se informará al solicitante indicando los motivos y la nueva fecha estimada de respuesta.

### 11.5 Registro de solicitudes

Se llevará un registro interno de las solicitudes recibidas y su estado de trámite, con fines de trazabilidad y cumplimiento normativo.

---

## 12. Consentimiento Informado para el Tratamiento de Datos

### 12.1 Texto sugerido para el formulario de registro

> He leído y acepto la Política de Privacidad y los Términos y Condiciones de FinTrack. Autorizo el tratamiento de mis datos personales, incluida la información financiera que registre en la Plataforma, para las finalidades descritas en la Política de Privacidad, de conformidad con la Ley 1581 de 2012 y demás normas aplicables.

Este texto debe ir acompañado de una casilla de verificación (checkbox) que el usuario debe marcar activamente antes de completar el registro; no debe estar premarcada.

### 12.2 Alcance del consentimiento

El consentimiento cubre el tratamiento necesario para prestar las funcionalidades de FinTrack descritas en la Política de Privacidad. Cualquier finalidad adicional (por ejemplo, envío de comunicaciones de marketing) debe solicitarse mediante un consentimiento separado y específico.

### 12.3 Revocación

El usuario puede revocar su consentimiento en cualquier momento, sin efectos retroactivos, mediante el procedimiento descrito en la sección 11. La revocación podrá implicar la imposibilidad de continuar utilizando la Plataforma, en la medida en que el tratamiento de esos datos sea indispensable para su funcionamiento.

### 12.4 Consecuencias de no otorgar el consentimiento

Si el usuario no otorga el consentimiento requerido, no será posible crear ni mantener una cuenta activa en FinTrack, dado que el tratamiento de los datos es necesario para la prestación del servicio.
