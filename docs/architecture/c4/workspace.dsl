workspace "EcoRecicla AQP - Arquitectura C4" "Modelo de arquitectura C4 para la plataforma municipal de reciclaje EcoRecicla AQP." {

    model {
        # ==========================================
        # 1. PERSONAS (Nivel 1 - Contexto)
        # ==========================================
        vecino = person "Vecino / Ciudadano" "Residente de Arequipa que solicita el recojo de residuos reciclables y acumula puntos de beneficio." "User"
        reciclador = person "Reciclador / Operador" "Personal operativo que atiende las rutas de recojo, registra pesajes y gestiona atenciones." "Operator"
        admin = person "Administrador Municipal" "Personal encargado de consultar reportes e indicadores de reciclaje municipal." "Admin"

        # ==========================================
        # 2. SISTEMAS EXTERNOS (Nivel 1 - Contexto)
        # ==========================================
        mapas = softwareSystem "Servicio de Mapas y Geolocalizacion" "Servicio externo utilizado para validar coordenadas geograficas de los puntos de recojo." "Externo"
        whatsapp = softwareSystem "API de Notificaciones WhatsApp" "Servicio externo para el envio asincrono de mensajes y alertas de confirmacion." "Externo"

        # ==========================================
        # 3. SISTEMA PRINCIPAL Y CONTENEDORES (Nivel 2)
        # ==========================================
        ecorecicla = softwareSystem "EcoRecicla AQP" "Plataforma municipal para la gestion integral de recojo, pesaje y acreditacion de reciclaje." {

            pwa = container "Aplicacion Web Progresiva (PWA)" "Propone conservar pendientes con identificador estable en IndexedDB hasta ACK y reintentarlos al volver la red [QA-02, QA-07]. Falta integración real." "JavaScript / Service Worker / IndexedDB" "Web Browser" {
                bufferLocal = component "Cola local de sincronizacion" "Mantiene cada registro pendiente con un identificador estable y lo conserva hasta el ACK del servidor [QA-02, QA-07]. Diseño propuesto; pendiente de integración en la PWA." "IndexedDB / Service Worker" "Component"
            }

            api = container "API REST Monolito Modular" "Conserva los límites entre módulos. Propone configuración versionada [QA-01, QA-06], recepción idempotente [QA-02, QA-07] y autorización distrital [QA-04, QA-05]; la integración real está pendiente." "Python / API REST" "Backend" {
            solicitudesMod = component "Modulo Solicitudes" "Gestiona el registro y ciclo de vida; el diseño propone deduplicar sincronizaciones y validar el ámbito distrital antes del acceso [QA-02, QA-04, QA-05, QA-07]." "Python" "Component"
            syncReceiver = component "Receptor idempotente de sincronizacion" "Persiste efecto y clave (distrito, identificador) antes del ACK; reintentos idénticos no repiten el efecto [QA-02, QA-07]. Diseño propuesto, no implementado por el prototipo SQLite." "Python / transaccion PostgreSQL" "Component"
            authScope = component "Autorizacion de ambito distrital" "Deriva el distrito desde el contexto autenticado y rechaza ámbito ausente o incompatible antes de leer o escribir [QA-04, QA-05]. JWT y middleware reales siguen pendientes." "Python / contexto autenticado propuesto" "Component"
            rutasMod = component "Modulo Rutas y Cobertura" "Gestiona cobertura y horarios versionados por distrito mediante su contrato público, sin requerir cambios en los consumidores [QA-01, QA-06]." "Python" "Component"
            puntosMod = component "Modulo Puntos y Beneficios" "Administra acreditación y canje; mantiene tarifas versionadas por distrito en su propio esquema y usa estrategias para fórmulas variables [QA-01, QA-06]." "Python" "Component"
            reportesMod = component "Modulo Reportes" "Genera indicadores municipales y debe respetar el ámbito distrital autorizado en cada consulta [QA-04, QA-05]." "Python" "Component"
            notifMod = component "Notificaciones (auxiliar de Solicitudes)" "Servicio auxiliar para la composicion y despacho asincrono de avisos." "Python" "Component"
            compartidoMod = component "Compartido" "Define IdentificadorSolicitud como alias de UUID, sin entidades de dominio ni acceso a datos." "Python / UUID" "Component"
        }


            bd = container "Base de Datos Relacional" "PostgreSQL con esquemas por módulo, configuraciones versionadas, clave idempotente y distrito_id [QA-01, QA-02, QA-04, QA-05, QA-06, QA-07]. RLS es propuesta, no configurada ni verificada." "PostgreSQL / esquemas por módulo / claves únicas / RLS propuesta" "Database"

        }

        # ==========================================
        # 4. RELACIONES (Nivel 1 y Nivel 2 con Protocolos)
        # ==========================================
        # Relaciones de alto nivel del Sistema
        ecorecicla -> mapas "Valida coordenadas geograficas de los puntos de recojo"
        ecorecicla -> whatsapp "Envia avisos y notificaciones de confirmacion de recojo"
        vecino -> ecorecicla "Registra solicitudes de recojo de reciclables y consulta sus puntos"
        reciclador -> ecorecicla "Consulta rutas asignadas, atiende recojos y registra pesajes in situ"
        admin -> ecorecicla "Consulta reportes de pesaje e indicadores de reciclaje municipal"

        # Interaccion de Usuarios con Frontend
        vecino -> pwa "Registra solicitudes y consulta puntos" "HTTPS / TLS"
        reciclador -> pwa "Consulta rutas, registra atenciones y pesajes" "HTTPS / TLS"
        admin -> pwa "Consulta reportes e indicadores municipales" "HTTPS / TLS"

        # Comunicacion Frontend -> Backend
        pwa -> api "Consume endpoints REST para solicitudes, rutas y autenticacion" "HTTPS / JSON"

        # Comunicacion Backend -> Infraestructura Interna
        api -> bd "Lee y escribe datos del dominio con integridad transaccional" "SQL / TCP (port 5432)"

        # Comunicacion Backend -> Sistemas Externos
        api -> mapas "Valida coordenadas geograficas de los puntos de recojo" "HTTPS / REST JSON"

        api -> whatsapp "Despacha avisos de confirmacion de recojo" "HTTPS / REST API"

        # Colaboraciones de los componentes, alineadas con paquetes.puml
        pwa -> solicitudesMod "Envia solicitudes de recojo y atenciones" "HTTPS / REST JSON"
        pwa -> reportesMod "Consulta indicadores y reportes" "HTTPS / REST JSON"
        bufferLocal -> syncReceiver "Reintenta el mismo registro pendiente hasta recibir ACK" "HTTPS / JSON / identificador estable"
        syncReceiver -> bd "Persiste el efecto y la clave de idempotencia en una transaccion antes del ACK" "SQL / transaccion"
        solicitudesMod -> authScope "Valida el contexto distrital antes de acceder a datos" "Contrato interno"
        reportesMod -> authScope "Valida el contexto distrital antes de consultar datos" "Contrato interno"
        solicitudesMod -> rutasMod "Consulta CoberturaRecojo para determinar cobertura distrital" "Contrato publico / llamada interna"
        solicitudesMod -> puntosMod "Solicita acreditacion mediante AcreditadorPuntos" "Contrato publico / llamada interna"
        solicitudesMod -> notifMod "Solicita aviso asincrono mediante NotificadorSolicitud" "Puerto interno / llamada interna"
        reportesMod -> solicitudesMod "Consulta pesajes confirmados mediante FuentePesajes" "Contrato publico / llamada interna"
        solicitudesMod -> compartidoMod "Utiliza IdentificadorSolicitud" "Tipo compartido UUID"
        rutasMod -> compartidoMod "Utiliza IdentificadorSolicitud" "Tipo compartido UUID"
        puntosMod -> compartidoMod "Utiliza IdentificadorSolicitud" "Tipo compartido UUID"
        notifMod -> compartidoMod "Utiliza IdentificadorSolicitud" "Tipo compartido UUID"
        reportesMod -> compartidoMod "Utiliza IdentificadorSolicitud" "Tipo compartido UUID"
        solicitudesMod -> bd "Persiste solicitudes en su esquema" "SQL / TCP (port 5432)"
        rutasMod -> bd "Persiste rutas y zonas en su esquema" "SQL / TCP (port 5432)"
        puntosMod -> bd "Persiste puntos y canjes en su esquema" "SQL / TCP (port 5432)"
        solicitudesMod -> mapas "Valida opcionalmente coordenadas mediante ServicioMapas" "HTTPS / REST JSON"
        notifMod -> whatsapp "Despacha avisos de confirmacion de recojo" "HTTPS / REST API"

        # E5: dimensionamiento propuesto para el MVP, no infraestructura contratada.
        produccion = deploymentEnvironment "Producción" {
            deploymentNode "Dispositivo del usuario" "Equipo existente del vecino, reciclador o personal municipal, sin servidor adicional." "Android o Windows / navegador compatible con PWA" {
                deploymentNode "Navegador web" "Ejecuta la PWA y conserva registros temporales sin conexion." "JavaScript / Service Worker / IndexedDB" {
                    containerInstance pwa
                }
            }
            deploymentNode "VPS unico - MVP" "Propuesta inicial compartida para API y base de datos. Capacidad por confirmar mediante mediciones, sin proveedor contratado." "Ubuntu Server 24.04 LTS / 2 vCPU / 4 GB RAM / 40 GB SSD" {
                deploymentNode "Entorno de aplicacion" "Un proceso de la API del monolito modular, sin separar los modulos en servicios." "Python / entorno virtual" {
                    containerInstance api
                }
                deploymentNode "Servicio de base de datos" "Una instancia local, con esquemas aislados por modulo, accesible por la API." "PostgreSQL / servicio Linux" {
                    containerInstance bd
                }
            }
        }
    }

    views {
        properties {
            "c4plantuml.tags" "true"
        }
        # ------------------------------------------
        # VISTA NIVEL 1: Contexto del Sistema (E1)
        # ------------------------------------------
        systemContext ecorecicla "VistaContexto" "Diagrama de Contexto del Sistema EcoRecicla AQP (Nivel 1 C4)." {
            title "Diagrama de Contexto del Sistema EcoRecicla AQP"
            description "Muestra las personas que interactuan con la plataforma EcoRecicla AQP y sus conexiones con sistemas externos."
            include *
            autoLayout lr
        }

        # ------------------------------------------
        # VISTA NIVEL 2: Contenedores (E2)
        # ------------------------------------------
        container ecorecicla "VistaContenedores" "Diagrama de Contenedores del Sistema EcoRecicla AQP (Nivel 2 C4)." {
            title "Diagrama de Contenedores - EcoRecicla AQP"
            description "Muestra las aplicaciones, servicios y almacenes de datos que integran la plataforma y sus protocolos de comunicacion."
            include *
            autoLayout lr
        }

        # ------------------------------------------
        # VISTA NIVEL 3: Componentes (E3)
        component api "VistaComponentes" "Diagrama de Componentes del contenedor API REST Monolito Modular (Nivel 3 C4)." {
            title "Diagrama de Componentes - API REST Monolito Modular"
            description "Muestra los cuatro modulos de dominio, Notificaciones como auxiliar de Solicitudes y los tipos compartidos, con dependencias sin ciclos."
            include *
            autoLayout lr
        }

        # ESTILOS VISUALES Y FORMAS
        # ------------------------------------------
        # VISTA DINAMICA: escenario de registro con datos y cobertura validos (E4)
        dynamic api "VistaDinamica" "Flujo critico de solicitar el recojo de reciclables, con comprobacion opcional de mapas." {
            title "Vista Dinamica - Solicitar el recojo de reciclables"
            description "Tras validar datos, consulta cobertura, comprueba opcionalmente coordenadas, guarda PENDIENTE y solicita un aviso interno asincrono. Un fallo de mapas no impide guardar, el aviso no bloquea la confirmacion."
            pwa -> solicitudesMod "Envia los datos de la solicitud, que Solicitudes valida"
            solicitudesMod -> rutasMod "Consulta cobertura distrital mediante CoberturaRecojo"
            solicitudesMod -> mapas "Comprueba opcionalmente coordenadas, si falla continua con ubicacion pendiente de revision"
            solicitudesMod -> bd "Guarda la solicitud PENDIENTE y espera confirmacion de persistencia"
            solicitudesMod -> notifMod "Solicita confirmarRegistro como aviso interno asincrono, sin bloquear la respuesta"
            autoLayout lr
        }

        # E5: despliegue del MVP en un solo VPS
        deployment ecorecicla produccion "VistaDespliegue" "Despliegue propuesto en Producción para el MVP de EcoRecicla AQP." {
            title "Despliegue - EcoRecicla AQP (Produccion)"
            description "PWA en el dispositivo del usuario, API y PostgreSQL en un unico VPS. Dimensionamiento inicial sujeto a medicion y cotizacion, acorde con la prioridad de bajo costo de R-03."
            include *
            autoLayout lr
        }

        styles {
            element "Component" {
                shape Component
                background #85bbf0
                color #000000
            }
            element "User" {
                shape Person
                background #08427b
                color #ffffff
            }
            element "Operator" {
                shape Person
                background #1168cb
                color #ffffff
            }
            element "Admin" {
                shape Person
                background #228b22
                color #ffffff
            }
            element "Software System" {
                background #1168cb
                color #ffffff
            }
            element "Externo" {
                background #999999
                color #ffffff
            }
            element "Web Browser" {
                shape WebBrowser
                background #438dd5
                color #ffffff
            }
            element "Backend" {
                shape Component
                background #85bbf0
                color #000000
            }

            element "Database" {
                shape Cylinder
                background #438dd5
                color #ffffff
            }

        }
    }
}
