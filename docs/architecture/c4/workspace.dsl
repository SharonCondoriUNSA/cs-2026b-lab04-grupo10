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

            pwa = container "Aplicacion Web Progresiva (PWA)" "Interfaz de usuario accesible desde navegadores moviles y de escritorio con soporte offline parcial." "JavaScript / Service Worker / IndexedDB" "Web Browser"

            api = container "API REST Monolito Modular" "Ejecuta la logica de negocio, validaciones de dominio y orquestacion de modulos." "Python / API REST" "Backend" {
            solicitudesMod = component "Modulo Solicitudes" "Gestiona el registro, validacion y ciclo de vida de las solicitudes de recojo." "Python" "Component"
            rutasMod = component "Modulo Rutas y Cobertura" "Gestiona las zonas de cobertura distrital y las rutas asignadas a recicladores." "Python" "Component"
            puntosMod = component "Modulo Puntos y Beneficios" "Administra la acreditacion y canje de puntos de reciclaje para los vecinos." "Python" "Component"
            reportesMod = component "Modulo Reportes" "Genera indicadores municipales sobre toneladas recicladas y cobertura." "Python" "Component"
            notifMod = component "Notificaciones (auxiliar de Solicitudes)" "Servicio auxiliar para la composicion y despacho asincrono de avisos." "Python" "Component"
            compartidoMod = component "Compartido" "Define IdentificadorSolicitud como alias de UUID, sin entidades de dominio ni acceso a datos." "Python / UUID" "Component"
        }


            bd = container "Base de Datos Relacional" "Almacena la informacion persistente de usuarios, solicitudes, rutas y puntos." "PostgreSQL" "Database"

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
    }

    views {
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
