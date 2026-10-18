# E1: Inventario de Elementos del Sistema EcoRecicla AQP

Este inventario consolida los elementos identificados en la arquitectura y diseño detallado de los Laboratorios 04 y 05, clasificándolos según las abstracciones del Modelo C4.

## 1. Personas (Usuarios del Sistema)
| Elemento | Tipo C4 | Archivo de Origen en Repositorio (Lab 04 / Lab 05) | Justificación en el Dominio |
| :--- | :--- | :--- | :--- |
| **Vecino / Ciudadano** | Persona | `docs/design/historia.md` <br> `docs/design/secuencia-solicitar-recojo.puml` | Usuario que registra solicitudes de recojo de reciclables y acumula puntos. |
| **Reciclador / Operador** | Persona | `docs/design/actividades-ruta-diaria.puml` | Personal operativo que atiende las rutas diarias, registra pesajes e incidencias. |
| **Administrador Municipal** | Persona | `docs/architecture/drivers.md` | Supervisa métricas de reciclaje, gestiona la cobertura distrital y reportes. |

## 2. Sistema de Software Principal
| Elemento | Tipo C4 | Archivo de Origen en Repositorio (Lab 04 / Lab 05) | Justificación en el Dominio |
| :--- | :--- | :--- | :--- |
| **EcoRecicla AQP** | Sistema de Software | `docs/architecture/adr/001-estilo-arquitectonico.md` | Plataforma municipal central para la gestión de recojo, pesaje y puntos. |

## 3. Sistemas Externos
| Elemento | Tipo C4 | Archivo de Origen en Repositorio (Lab 04 / Lab 05) | Justificación en el Dominio |
| :--- | :--- | :--- | :--- |
| **Servicio de Mapas y Geolocalización** | Sistema Externo | `docs/design/clases.puml` | API externa para la validación de cobertura distrital y coordenadas (`ServicioMapas`). |
| **API de Notificaciones WhatsApp** | Sistema Externo | `docs/design/paquetes.puml` <br> `docs/architecture/adr/001-estilo-arquitectonico.md` | Servicio externo para el despacho asíncrono de alertas de confirmación. |
| **Proveedor de Pagos / Beneficios** | Sistema Externo | `docs/design/paquetes.puml` | Plataforma externa para la redención y acreditación de puntos de beneficio. |

## 4. Contenedores (Unidades de Ejecución / Despliegue)
| Elemento | Tipo C4 | Archivo de Origen en Repositorio (Lab 04 / Lab 05) | Justificación en el Dominio |
| :--- | :--- | :--- | :--- |
| **Aplicación Web Progresiva (PWA)** | Contenedor | `docs/architecture/adr/001-estilo-arquitectonico.md` <br> `docs/architecture/diagramas/despliegue.py` | Interfaz web para vecinos y recicladores con soporte offline parcial. |
| **API REST Monolito Modular** | Contenedor | `docs/architecture/adr/001-estilo-arquitectonico.md` | Backend central que ejecuta la lógica de negocio y reglas de dominio en Python. |
| **Worker de Tareas Asíncronas** | Contenedor | `docs/architecture/adr/001-estilo-arquitectonico.md` <br> `docs/architecture/diagramas/despliegue.py` | Procesador Celery en segundo plano para notificaciones y reintentos. |
| **Base de Datos Relacional** | Contenedor | `docs/architecture/adr/001-estilo-arquitectonico.md` <br> `docs/architecture/diagramas/despliegue.py` | Almacenamiento PostgreSQL 16 para solicitudes, usuarios y cobertura. |
| **Cola de Tareas y Caché** | Contenedor | `docs/architecture/adr/001-estilo-arquitectonico.md` <br> `docs/architecture/diagramas/despliegue.py` | Servicio Redis 7 para cola de tareas asíncronas y caché. |

## 5. Componentes de la API REST (Nivel 3)
| Elemento | Tipo C4 | Archivo de Origen en Repositorio (Lab 04 / Lab 05) | Justificación en el Dominio |
| :--- | :--- | :--- | :--- |
| **Módulo Solicitudes** | Componente | `docs/design/paquetes.puml` (`solicitudes` / `SOL`) | Gestiona el registro, validación y ciclo de vida de solicitudes. |
| **Módulo Rutas y Cobertura** | Componente | `docs/design/paquetes.puml` (`rutas_cobertura` / `RUT`) | Gestiona distritos, operadores y asignación de recojos. |
| **Módulo Puntos y Beneficios** | Componente | `docs/design/paquetes.puml` (`puntos_beneficios` / `PUN`) | Procesa la acreditación y cálculo de puntos por reciclaje. |
| **Módulo Reportes** | Componente | `docs/design/paquetes.puml` (`reportes` / `REP`) | Consolida métricas de reciclaje para la administración municipal. |
| **Módulo Notificaciones** | Componente | `docs/design/paquetes.puml` (`notificaciones` / `NOT`) | Componente auxiliar para alertas de registro. |
| **Módulo Compartido** | Componente | `docs/design/paquetes.puml` (`compartido` / `COM`) | Value Objects e identificadores comunes UUID. |