# 🛡️ InventoryIntel-Agro | Full-Stack Monitoring System

[![Security: Inmutable](https://img.shields.io/badge/Data-Immutable-green.svg)]()
[![Environment: Mobile-Dev](https://img.shields.io/badge/Dev_Environment-Termux-orange.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)]()

### "En un sistema de inventario, la integridad de los datos no es una opción, es un requisito de seguridad."

**InventoryIntel-Agro** es una solución de gestión de suministros diseñada para entornos agrícolas de alta precisión. Este sistema no solo rastrea existencias; audita movimientos, genera inteligencia visual y garantiza que los registros críticos permanezcan inalterables mediante políticas de inmutabilidad a nivel de kernel de aplicación.

---

## 🛠️ Stack Tecnológico (The Tech Arsenal)

Este proyecto fue desarrollado íntegramente desde una terminal **Termux (Android)**, demostrando que la potencia reside en la lógica, no en el hardware.

* **Core:** Python 3.12 / Django 6.0 (Robustez y Escalabilidad).
* **Database:** PostgreSQL (Neon.tech) con persistencia segura.
* **Analytics:** Matplotlib (Generación de telemetría visual en memoria).
* **Export Engine:** ReportLab (Auditoría PDF) & CSV streaming.
* **QA/Security:** Pytest-Django + Faker + DDF (Testing automatizado de grado industrial).
* **Frontend:** Bootstrap 5 con arquitectura de filtros dinámicos.

---

## 🛡️ Características de Seguridad y Lógica (Security Features)

* **Inmutabilidad de Registros:** Los nombres de los productos y reportes críticos están protegidos mediante el override del método `.save()`, impidiendo la manipulación accidental o malintencionada de la identidad del inventario.
* **Auditoría Automatizada:** Generación de reportes PDF dinámicos con flujos de `io.BytesIO` para evitar fugas de datos en el sistema de archivos del servidor.
* **Filtros de Búsqueda Crítica:** Implementación de parámetros `GET` para análisis instantáneo de niveles de stock (Critical vs Warning).



---

## 🧪 Control de Calidad (Testing Suite)

El sistema ha sido sometido a pruebas de estrés y validación mediante **Pytest**:
- **Población con Faker:** Simulación de entornos reales con +20 registros aleatorios.
- **Validación de Inmutabilidad:** Pruebas de intercepción de errores con `pytest.raises`.
- **Integration Tests:** Simulación de peticiones de usuario para exportación de documentos.

```bash
# Ejecución del arsenal de pruebas
test-python
```

## 🔐 Acceso de Auditoría (Testing Credentials)

Para pruebas manuales y validación de la integridad del sistema, se ha configurado un perfil de superusuario con datos de telemetría pre-cargados.

| Atributo | Credencial de Acceso |
| :--- | :--- |
| **Identificador (User)** | `tester_shadow` |
| **Código de Acceso (Pass)** | `ShadowPassword2026` |
| **Nivel de Privilegio** | `Superuser / Root Access` |

> **Nota de Seguridad:** Estas credenciales están destinadas exclusivamente a entornos de desarrollo local y staging. En el despliegue final de producción, este acceso será revocado para cumplir con las políticas de endurecimiento (hardening) del sistema.


## 🚀 Despliegue (Deployment)
El sistema está configurado para operar en entornos Serverless (Vercel) utilizando:
+ WhiteNoise: Para una entrega eficiente de activos estáticos con compresión Gzip.
+ MPLCONFIGDIR: Configuración dinámica de directorios temporales para evitar errores en sistemas de archivos de solo lectura.

### 👤 Autor
**ShadowRoot07 Full-Stack Developer | Mobile Development Enthusiast | Ethical Mindset**
*"Compilado en la oscuridad de la terminal."*

