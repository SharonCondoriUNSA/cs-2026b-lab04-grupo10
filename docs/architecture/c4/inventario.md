# E1: Inventario de Elementos del Sistema EcoRecicla AQP

Este inventario consolida los elementos identificados en la arquitectura y diseño detallado de los Laboratorios 04 y 05, clasificándolos según las abstracciones del Modelo C4.

## 1. Personas (Usuarios del Sistema)
| Elemento | Tipo C4 | Archivo de Origen en Repositorio (Lab 04 / Lab 05) | Justificación en el Dominio |
| :--- | :--- | :--- | :--- |
| **Vecino / Ciudadano** | Persona | `docs/design/historia.md` <br> `docs/design/secuencia-solicitar-recojo.puml` | Usuario que registra solicitudes de recojo de reciclables y acumula puntos. |
| **Reciclador / Operador** | Persona | `docs/design/actividades-ruta-diaria.puml` | Personal operativo que atiende las rutas diarias, registra pesajes e incidencias. |
| **Administrador Municipal** | Persona | `docs/architecture/drivers.md` | Consulta reportes e indicadores de reciclaje municipal. |

## 2. Sistema de Software Principal
| Elemento | Tipo C4 | Archivo de Origen en Repositorio (Lab 04 / Lab 05) | Justificación en el Dominio |
| :--- | :--- | :--- | :--- |
| **EcoRecicla AQP** | Sistema de Software | `docs/architecture/adr/001-estilo-arquitectonico.md` | Plataforma municipal central para la gestión de recojo, pesaje y puntos. |

## 3. Sistemas Externos
| Elemento | Tipo C4 | Archivo de Origen en Repositorio (Lab 04 / Lab 05) | Justificación en el Dominio |
| :--- | :--- | :--- | :--- |
| **Servicio de Mapas y Geolocalización** | Sistema Externo | `docs/design/clases.puml` | Servicio externo para validar coordenadas (`ServicioMapas`). La cobertura distrital se determina en el módulo Rutas y Cobertura. |
| **API de Notificaciones WhatsApp** | Sistema Externo | `docs/architecture/diagramas/despliegue.py` | Servicio externo para el despacho asíncrono de alertas de confirmación. |

## 4. Contenedores (Unidades de Ejecución / Despliegue)
| Elemento | Tipo C4 | Archivo de Origen en Repositorio (Lab 04 / Lab 05) | Justificación en el Dominio |
| :--- | :--- | :--- | :--- |
| **Aplicación Web Progresiva (PWA)** | Contenedor | `docs/architecture/adr/003-aplicacion-frontend.md` | Interfaz web para vecinos y recicladores con soporte offline parcial. |
| **API REST Monolito Modular** | Contenedor | `docs/architecture/adr/001-estilo-arquitectonico.md` <br> `src/solicitudes/dominio.py` | Backend central que ejecuta la lógica de negocio y reglas de dominio en Python. |
| **Base de Datos Relacional** | Contenedor | `docs/architecture/adr/002-base-de-datos.md` | Almacenamiento PostgreSQL con esquemas aislados por módulo para solicitudes, usuarios y cobertura. |

## 5. Componentes de la API REST (Nivel 3)
| Elemento | Tipo C4 | Archivo de Origen en Repositorio (Lab 04 / Lab 05) | Justificación en el Dominio |
| :--- | :--- | :--- | :--- |
| **Módulo Solicitudes** | Componente | `docs/design/paquetes.puml` (`solicitudes` / `SOL`) | Gestiona el registro, validación y ciclo de vida de solicitudes. |
| **Módulo Rutas y Cobertura** | Componente | `docs/design/paquetes.puml` (`rutas_cobertura` / `RUT`) | Gestiona distritos, operadores y asignación de recojos. |
| **Módulo Puntos y Beneficios** | Componente | `docs/design/paquetes.puml` (`puntos_beneficios` / `PUN`) | Procesa la acreditación y cálculo de puntos por reciclaje. |
| **Módulo Reportes** | Componente | `docs/design/paquetes.puml` (`reportes` / `REP`) | Consolida métricas de reciclaje para la administración municipal. |
| **Módulo Notificaciones** | Componente | `docs/design/paquetes.puml` (`notificaciones` / `NOT`) | Componente auxiliar para alertas de registro. |
| **Módulo Compartido** | Componente | `docs/design/paquetes.puml` (`compartido` / `COM`) | Value Objects e identificadores comunes UUID. |
