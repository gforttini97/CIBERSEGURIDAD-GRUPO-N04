# Farma Help — Arquitectura

## Diagrama

```mermaid
flowchart LR
    subgraph L1["Límite 1: Entradas no confiables"]
        OP["Operador"]
        CON["Consultor solo lectura"]
        DOC["Documento externo"]
        CAT["Catálogo de pruebas"]
    end

    subgraph L2["Límite 2: Producto Farma Help"]
        UI["Interfaz"]
        ORQ["Orquestador y verificación de rol"]
        K1["K1 Detector de inyección"]
        K2["K2 Filtro de información restringida"]
        RAG["Componente 1: RAG con modelo de lenguaje"]
        CLF["Componente 2: Clasificador de reclamos"]
        AG["Componente 3: Agente propone ticket"]
        K3["K3 Autorización de herramienta"]
        CONF{"Confirmación del operador"}
        TK["Herramienta crear_ticket"]
    end

    subgraph L3["Límite 3: Datos internos sintéticos"]
        CORPUS[("Corpus de 3 políticas")]
        MOD[("Modelo y reclamos etiquetados")]
        USERS[("Usuarios y roles")]
        TICKETS[("tickets.json")]
        LOG[("registro.jsonl")]
    end

    subgraph L4["Límite 4: Evaluación"]
        RUN["correr_evaluacion.py"]
        MET["Métricas: éxito, Wilson y falsos positivos"]
    end

    OP --> UI
    CON --> UI
    UI --> ORQ
    ORQ --> USERS
    ORQ --> K1
    K1 --> RAG
    DOC -->|"ingesta"| CORPUS
    CORPUS --> K2
    K2 --> RAG
    ORQ --> CLF
    MOD --> CLF
    CLF --> RAG
    RAG -->|"respuesta"| ORQ
    ORQ -->|"respuesta final"| UI
    RAG -->|"acción propuesta"| AG
    AG --> K3
    K3 -->|"permitida"| CONF
    CONF -->|"confirma"| TK
    TK --> TICKETS

    ORQ -.-> LOG
    K1 -.-> LOG
    K2 -.-> LOG
    RAG -.-> LOG
    CLF -.-> LOG
    K3 -.-> LOG
    CONF -.-> LOG
    TK -.-> LOG

    CAT --> RUN
    RUN --> UI
    LOG --> MET
```

## Componentes

| Componente | Función |
|---|---|
| Interfaz | Recibe la consulta del usuario |
| Orquestador | Verifica el rol y coordina RAG, clasificador, agente y registro |
| RAG | Recupera fragmentos de las políticas y redacta la respuesta citando el documento |
| Clasificador | Asigna el reclamo a entrega, facturación o devolución |
| Agente | Propone un ticket y lo registra solo tras la confirmación del operador |
| K1, K2 y K3 | Controles que se activan o desactivan por parámetro |
| Registro | Guarda consulta, documentos recuperados, acciones y respuestas |

## Límites de confianza

| Límite | Contenido | Por qué importa |
|---|---|---|
| L1 | Usuarios, documentos externos y catálogo de pruebas | Todo lo que entra puede ser malicioso |
| L2 | Producto y controles | Aquí se decide qué llega al modelo y qué acciones se ejecutan |
| L3 | Corpus, modelo, usuarios, tickets y registro | Datos que un atacante querría leer o alterar |
| L4 | Scripts y resultados de evaluación | Mide el efecto de los controles |

Cruces de mayor riesgo:

1. Documento externo hacia el corpus (inyección indirecta).
2. Salida del modelo hacia el agente (se valida en K3).
3. Producto hacia información restringida (filtración).
4. Agente hacia `tickets.json` (ticket no autorizado).

## Estado de implementación

| Elemento | Estado |
|---|---|
| Interfaz, orquestador y RAG | En construcción |
| Clasificador de reclamos | Pendiente |
| Agente y crear_ticket | Pendiente |
| Controles K1, K2 y K3 | Pendiente |
| Registro de eventos | En construcción |
| Evaluación | Pendiente |
