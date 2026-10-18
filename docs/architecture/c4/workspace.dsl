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
        # 3. SISTEMA PRINCIPAL (Nivel 1 - Contexto)
        # ==========================================
        ecorecicla = softwareSystem "EcoRecicla AQP" "Plataforma municipal para la gestion integral de recojo, pesaje y acreditacion de reciclaje."

        # ==========================================
        # 4. RELACIONES NIVEL 1 (Verbos de Intención)
        # ==========================================
        vecino -> ecorecicla "Registra solicitudes de recojo de reciclables y consulta sus puntos"
        reciclador -> ecorecicla "Consulta rutas asignadas, atiende recojos y registra pesajes in situ"
        admin -> ecorecicla "Consulta reportes de pesaje e indicadores de reciclaje municipal"
        
        ecorecicla -> mapas "Valida coordenadas geograficas de los puntos de recojo"
        ecorecicla -> whatsapp "Envia avisos y notificaciones de confirmacion de recojo"
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
            element "Externo" {
                background #999999
                color #ffffff
            }
        }
    }
}
