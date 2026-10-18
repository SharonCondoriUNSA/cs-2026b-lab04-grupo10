workspace "EcoRecicla AQP - Arquitectura C4" "Modelo de arquitectura C4 para la plataforma municipal de reciclaje EcoRecicla AQP." {

    model {
        # ==========================================
        # 1. PERSONAS (Nivel 1 - Contexto)
        # ==========================================
        vecino = person "Vecino / Ciudadano" "Residente de Arequipa que solicita el recojo de residuos reciclables y acumula puntos de beneficio." "User"
        reciclador = person "Reciclador / Operador" "Personal operativo que atiende las rutas de recojo, registra pesajes y gestiona atenciones." "Operator"
        admin = person "Administrador Municipal" "Personal encargado de supervisar indicadores de reciclaje y gestionar la cobertura distrital." "Admin"

        # ==========================================
        # 2. SISTEMAS EXTERNOS (Nivel 1 - Contexto)
        # ==========================================
        mapas = softwareSystem "Servicio de Mapas y Geolocalizacion" "API externa utilizada para geocodificacion, validacion de distritos y trazado de rutas." "Externo"
        whatsapp workspace "EcoRecicla AQP - Arquitectura C4" "Modelo de arquitectura C4 para la plataforma municipal de reciclaje EcoRecicla AQP." {
        
            model {
                # ==========================================
                # 1. PERSONAS (Nivel 1 - Contexto)
                # ==========================================
                vecino = person "Vecino / Ciudadano" "Residente de Arequipa que solicita el recojo de residuos reciclables y acumula puntos de beneficio." "User"
                reciclador = person "Reciclador / Operador" "Personal operativo que atiende las rutas de recojo, registra pesajes y gestiona atenciones." "Operator"
                admin = person "Administrador Municipal" "Personal encargado de supervisar indicadores de reciclaje y gestionar la cobertura distrital." "Admin"
        
                # ==========================================
                # 2. SISTEMAS EXTERNOS (Nivel 1 - Contexto)
                # ==========================================
                mapas = softwareSystem "Servicio de Mapas y Geolocalizacion" "API externa utilizada para geocodificacion, validacion de distritos y trazado de rutas." "Externo"
                whatsapp = softwareSystem "API de Notificaciones WhatsApp" "Servicio externo para el envio asincrono de mensajes y alertas de confirmacion." "Externo"
                pagos = softwareSystem "Proveedor de Pagos / Beneficios" "Plataforma externa para la redencion y acreditacion de puntos de beneficio." "Externo"
        
                # ==========================================
                # 3. SISTEMA PRINCIPAL Y CONTENEDORES (Nivel 2)
                # ==========================================
                ecorecicla = softwareSystem "EcoRecicla AQP" "Plataforma municipal para la gestion integral de recojo, pesaje y acreditacion de reciclaje." {
                    
                    pwa = container "Aplicacion Web Progresiva (PWA)" "Interfaz de usuario accesible desde navegadores moviles y de escritorio con soporte offline parcial." "React / TypeScript PWA" "Web Browser"
                    
                    api = container "API REST Monolito Modular" "Ejecuta la logica de negocio, validaciones de dominio y orquestacion de modulos." "Python 3.12 / FastAPI" "Backend"
                    
                    worker = container "Worker de Tareas Asincronas" "Procesa trabajos en segundo plano como el despacho diferido de notificaciones." "Python / Celery" "Worker"
                    
                    bd = container "Base de Datos Relacional" "Almacena la informacion persistente de usuarios, solicitudes, rutas y puntos." "PostgreSQL 16" "Database"
                    
                    redis = container "Cola de Mensajes y Cache" "Gestiona la cola de tareas asincronas para Celery y el almacenamiento en memoria." "Redis 7" "Queue"
                }
        
                # ==========================================
                # 4. RELACIONES (Nivel 1 y Nivel 2 con Protocolos)
                # ==========================================
                # Interaccion de Usuarios con Frontend
                vecino -> pwa "Registra solicitudes y consulta puntos" "HTTPS / TLS"
                reciclador -> pwa "Consulta rutas, registra atenciones y pesajes" "HTTPS / TLS"
                admin -> pwa "Consulta reportes e indicadores municipales" "HTTPS / TLS"
        
                # Comunicacion Frontend -> Backend
                pwa -> api "Consume endpoints REST para solicitudes, rutas y autenticacion" "HTTPS / JSON"
        
                # Comunicacion Backend -> Infraestructura Interna
                api -> bd "Lee y escribe datos del dominio con integridad transaccional" "SQL / TCP (port 5432)"
                api -> redis "Encola tareas asincronas y consulta cache" "RESP / TCP (port 6379)"
                worker -> redis "Obtiene tareas pendientes de la cola" "RESP / TCP (port 6379)"
                worker -> bd "Actualiza estados de envios de notificaciones" "SQL / TCP (port 5432)"
        
                # Comunicacion Backend -> Sistemas Externos
                api -> mapas "Valida coordenadas geograficas y limites distritales" "HTTPS / REST JSON"
                worker -> whatsapp "Despacha mensajes de texto y alertas de confirmacion" "HTTPS / REST API"
                api -> pagos "Acredita y sincroniza puntos de beneficio" "HTTPS / REST API"
        
                # Relaciones de alto nivel del Sistema
                ecorecicla -> mapas "Valida cobertura distrital"
                ecorecicla -> whatsapp "Envia notificaciones"
                ecorecicla -> pagos "Canaliza puntos"
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
                # ESTILOS VISUALES Y FORMAS
                # ------------------------------------------
                styles {
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
                    element "Worker" {
                        shape Robot
                        background #85bbf0
                        color #000000
                    }
                    element "Database" {
                        shape Cylinder
                        background #438dd5
                        color #ffffff
                    }
                    element "Queue" {
                        shape Pipe
                        background #85bbf0
                        color #000000
                    }
                }
            }
        }= softwareSystem "API de Notificaciones WhatsApp" "Servicio externo para el envio asincrono de mensajes y alertas de confirmacion." "Externo"
        pagos = softwareSystem "Proveedor de Pagos / Beneficios" "Plataforma externa para la redencion y acreditacion de puntos de beneficio." "Externo"

        # ==========================================
        # 3. SISTEMA PRINCIPAL (Nivel 1 - Contexto)
        # ==========================================
        ecorecicla = softwareSystem "EcoRecicla AQP" "Plataforma municipal para la gestion integral de recojo, pesaje y acreditacion de reciclaje."

        # ==========================================
        # 4. RELACIONES NIVEL 1 (Verbos de Intención)
        # ==========================================
        vecino -> ecorecicla "Registra solicitudes de recojo de reciclables y consulta sus puntos"
        reciclador -> ecorecicla "Consulta rutas asignadas, atiende recojos y registra pesajes in situ"
        admin -> ecorecicla "Consulta reportes de pesaje e indicadores de reciclaje municipal"
        
        ecorecicla -> mapas "Valida cobertura distrital y coordenadas geograficas"
        ecorecicla -> whatsapp "Envia avisos y notificaciones de confirmacion de recojo"
        ecorecicla -> pagos "Canaliza la acreditacion de puntos de beneficio"
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

        # ESTILOS VISUALES
        styles {
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
            element workspace "EcoRecicla AQP - Arquitectura C4" "Modelo de arquitectura C4 para la plataforma municipal de reciclaje EcoRecicla AQP." {
            
                model {
                    # ==========================================
                    # 1. PERSONAS (Nivel 1 - Contexto)
                    # ==========================================
                    vecino = person "Vecino / Ciudadano" "Residente de Arequipa que solicita el recojo de residuos reciclables y acumula puntos de beneficio." "User"
                    reciclador = person "Reciclador / Operador" "Personal operativo que atiende las rutas de recojo, registra pesajes y gestiona atenciones." "Operator"
                    admin = person "Administrador Municipal" "Personal encargado de supervisar indicadores de reciclaje y gestionar la cobertura distrital." "Admin"
            
                    # ==========================================
                    # 2. SISTEMAS EXTERNOS (Nivel 1 - Contexto)
                    # ==========================================
                    mapas = softwareSystem "Servicio de Mapas y Geolocalizacion" "API externa utilizada para geocodificacion, validacion de distritos y trazado de rutas." "Externo"
                    whatsapp = softwareSystem "API de Notificaciones WhatsApp" "Servicio externo para el envio asincrono de mensajes y alertas de confirmacion." "Externo"
                    pagos = softwareSystem "Proveedor de Pagos / Beneficios" "Plataforma externa para la redencion y acreditacion de puntos de beneficio." "Externo"
            
                    # ==========================================
                    # 3. SISTEMA PRINCIPAL, CONTENEDORES Y COMPONENTES (Nivel 2 y 3)
                    # ==========================================
                    ecorecicla = softwareSystem "EcoRecicla AQP" "Plataforma municipal para la gestion integral de recojo, pesaje y acreditacion de reciclaje." {
                        
                        pwa = container "Aplicacion Web Progresiva (PWA)" "Interfaz de usuario accesible desde navegadores moviles y de escritorio con soporte offline parcial." "React / TypeScript PWA" "Web Browser"
                        
                        # CONTENEDOR PRINCIPAL CON COMPONENTES (Nivel 3)
                        api = container "API REST Monolito Modular" "Ejecuta la logica de negocio, validaciones de dominio y orquestacion de modulos." "Python 3.12 / FastAPI" "Backend" {
                            
                            solicitudesMod = component "Modulo Solicitudes" "Gestiona el registro, validacion y ciclo de vida de las solicitudes de recojo." "FastAPI / Python" "Component"
                            rutasMod = component "Modulo Rutas y Cobertura" "Gestiona las zonas de cobertura distrital y las rutas asignadas a recicladores." "FastAPI / Python" "Component"
                            puntosMod = component "Modulo Puntos y Beneficios" "Administra la acreditacion y canje de puntos de reciclaje para los vecinos." "FastAPI / Python" "Component"
                            reportesMod = component "Modulo Reportes" "Genera indicadores municipales sobre toneladas recicladas y cobertura." "FastAPI / Python" "Component"
                            notifMod = component "Modulo Notificaciones" "Servicio auxiliar para la composicion y despacho asincrono de avisos." "FastAPI / Python" "Component"
                        }
                        
                        worker = container "Worker de Tareas Asincronas" "Procesa trabajos en segundo plano como el despacho diferido de notificaciones." "Python / Celery" "Worker"
                        bd = container "Base de Datos Relacional" "Almacena la informacion persistente de usuarios, solicitudes, rutas y puntos." "PostgreSQL 16" "Database"
                        redis = container "Cola de Mensajes y Cache" "Gestiona la cola de tareas asincronas para Celery y el almacenamiento en memoria." "Redis 7" "Queue"
                    }
            
                    # ==========================================
                    # 4. RELACIONES (Nivel 1, 2 y 3)
                    # ==========================================
                    # Interaccion de Usuarios con Frontend
                    vecino -> pwa "Registra solicitudes y consulta puntos" "HTTPS / TLS"
                    reciclador -> pwa "Consulta rutas, registra atenciones y pesajes" "HTTPS / TLS"
                    admin -> pwa "Consulta reportes e indicadores municipales" "HTTPS / TLS"
            
                    # Comunicacion Frontend -> Componentes de la API
                    pwa -> solicitudesMod "Envia solicitudes de recojo y atenciones" "HTTPS / REST JSON"
                    pwa -> reportesMod "Consulta indicadores y reportes" "HTTPS / REST JSON"
            
                    # Dependencias internas entre Componentes (Alineadas a paquetes.puml - Sin Ciclos)
                    solicitudesMod -> rutasMod "Consulta contrato publico de cobertura" "Llamada interna"
                    solicitudesMod -> puntosMod "Solicita acreditacion de puntos" "Llamada interna"
                    solicitudesMod -> notifMod "Pide notificar evento de confirmacion" "Llamada interna"
                    reportesMod -> solicitudesMod "Consulta datos de solicitudes para estadisticas" "Lectura directa"
            
                    # Conexiones de Componentes hacia Infraestructura y Servicios Externos
                    notifMod -> redis "Encola tareas de notificaciones" "RESP / TCP (port 6379)"
                    solicitudesMod -> bd "Persiste solicitudes de recojo" "SQL / TCP (port 5432)"
                    rutasMod -> bd "Persiste rutas y zonas" "SQL / TCP (port 5432)"
                    puntosMod -> bd "Persiste saldo y canjes de puntos" "SQL / TCP (port 5432)"
                    
                    worker -> redis "Obtiene tareas pendientes de la cola" "RESP / TCP (port 6379)"
                    worker -> bd "Actualiza estados de envios de notificaciones" "SQL / TCP (port 5432)"
            
                    rutasMod -> mapas "Valida coordenadas geograficas y limites distritales" "HTTPS / REST API"
                    worker -> whatsapp "Despacha mensajes de texto y alertas de confirmacion" "HTTPS / REST API"
                    puntosMod -> pagos "Acredita y sincroniza puntos de beneficio" "HTTPS / REST API"
            
                    # Relaciones de alto nivel
                    ecorecicla -> mapas "Valida cobertura distrital"
                    ecorecicla -> whatsapp "Envia notificaciones"
                    ecorecicla -> pagos "Canaliza puntos"
                }
            
                views {
                    # VISTA NIVEL 1: Contexto
                    systemContext ecorecicla "VistaContexto" "Diagrama de Contexto del Sistema EcoRecicla AQP (Nivel 1 C4)." {
                        title "Diagrama de Contexto del Sistema EcoRecicla AQP"
                        description "Muestra las personas que interactuan con la plataforma EcoRecicla AQP y sus conexiones con sistemas externos."
                        include *
                        autoLayout lr
                    }
            
                    # VISTA NIVEL 2: Contenedores
                    container ecorecicla "VistaContenedores" "Diagrama de Contenedores del Sistema EcoRecicla AQP (Nivel 2 C4)." {
                        title "Diagrama de Contenedores - EcoRecicla AQP"
                        description "Muestra las aplicaciones, servicios y almacenes de datos que integran la plataforma y sus protocolos de comunicacion."
                        include *
                        autoLayout lr
                    }
            
                    # VISTA NIVEL 3: Componentes (NUEVA EN E3)
                    component api "VistaComponentes" "Diagrama de Componentes del contenedor API REST Monolito Modular (Nivel 3 C4)." {
                        title "Diagrama de Componentes - API REST Monolito Modular"
                        description "Muestra los modulos internos de la API, sus dependencias libres de ciclos y sus conexiones externas."
                        include *
                        autoLayout lr
                    }
            
                    # ESTILOS VISUALES
                    styles {
                        element "User" { shape Person background #08427b color #ffffff }
                        element "Operator" { shape Person background #1168cb color #ffffff }
                        element "Admin" { shape Person background #228b22 color #ffffff }
                        element "Software System" { background #1168cb color #ffffff }
                        element "Externo" { background #999999 color #ffffff }
                        element "Web Browser" { shape WebBrowser background #438dd5 color #ffffff }
                        element "Backend" { shape Component background #85bbf0 color #000000 }
                        element "Component" { shape Component background #85bbf0 color #000000 }
                        element "Worker" { shape Robot background #85bbf0 color #000000 }
                        element "Database" { shape Cylinder background #438dd5 color #ffffff }
                        element "Queue" { shape Pipe background #85bbf0 color #000000 }
                    }
                }
            }"Externo" {
                background #999999
                color #ffffff
            }
        }
    }
}