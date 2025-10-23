# FlyMCP Server

Un server MCP (Model Context Protocol) deployato su Fly.io.

## Strumenti Disponibili

- `get_server_info` - Informazioni sul server
- `calculate_operation` - Operazioni matematiche
- `format_text` - Formattazione testo
- `get_system_status` - Statistiche sistema

## Deploy

```bash
fly launch
fly deploy

# JSON/RPC
# Schema Standard MCP per Tools

Non è un JSON semplice, ma segue lo schema standard del protocollo MCP.

## 🏗️ Struttura Standard Obbligatoria
```python
tools = [
    {
        # ✅ CAMPI OBBLIGATORI
        "name": "string",                    # ← Nome univoco del tool
        "description": "string",             # ← Descrizione per Claude
        "inputSchema": {                     # ← Schema JSON Schema
            "type": "object",
            "properties": {
                "param1": {"type": "string"},
                "param2": {"type": "number"}
            },
            "required": ["param1"]  # ← Parametri obbligatori
        }
    }
]
```

## 📖 Schema Completo Standard
```python
tools = [
    {
        # 🔹 IDENTIFICAZIONE (obbligatori)
        "name": "get_server_info",                    # ← Nome unico
        "description": "Get server information",      # ← Cosa fa
        
        # 🔹 INPUT SCHEMA (obbligatorio)
        "inputSchema": {
            "type": "object",                         # ← SEMPRE "object"
            
            # Parametri disponibili
            "properties": {
                "timeout": {
                    "type": "number",                 # ← Tipo dato
                    "description": "Timeout in seconds",  # ← Descrizione param
                    "default": 30                    # ← Valore default
                },
                "format": {
                    "type": "string",
                    "enum": ["json", "yaml", "text"] # ← Valori permessi
                }
            },
            
            # Parametri obbligatori
            "required": ["format"]                    # ← Solo "format" obbligatorio
        }
    }
]
```

## 🎯 Confronto: TUO CODICE vs STANDARD

### Tool 1: Senza parametri
```python
{
    "name": "get_server_info",
    "description": "Get server information and status",
    "inputSchema": {
        "type": "object",           # ✅ STANDARD
        "properties": {}            # ✅ Nessun parametro
        # "required": []            # ⚠️ Mancante ma ok se vuoto
    }
}
```

### Tool 2: Con parametro obbligatorio
```python
{
    "name": "calculate_operation", 
    "description": "Perform mathematical calculations",
    "inputSchema": {
        "type": "object",           # ✅ STANDARD
        "properties": {
            "operation": {
                "type": "string",   # ✅ Tipo corretto
                "description": "Math operation like '2+2'"  # ✅ Descrizione
            }
        },
        "required": ["operation"]   # ✅ Parametro obbligatorio
    }
}
```

### Tool 3: Con enum e parametri multipli
```python
{
    "name": "format_text",
    "description": "Format text in different styles", 
    "inputSchema": {
        "type": "object",           # ✅ STANDARD
        "properties": {
            "text": {"type": "string"},  # ✅ Parametro 1
            "style": {
                "type": "string",
                "enum": ["uppercase", "lowercase", "title"]  # ✅ Valori permessi
            }
        },
        "required": ["text", "style"]  # ✅ Entrambi obbligatori
    }
}
```

## 📚 TIPI DATI SUPPORTATI (JSON Schema)
```python
# ✅ TIPI VALIDI
"properties": {
    "string_param": {"type": "string"},
    "number_param": {"type": "number"}, 
    "integer_param": {"type": "integer"},
    "boolean_param": {"type": "boolean"},
    "array_param": {"type": "array"},
    "object_param": {"type": "object"}
}

# ✅ VALIDAZIONI AVANZATE
"properties": {
    "age": {
        "type": "integer",
        "minimum": 0,                      # ← Valore minimo
        "maximum": 150
    },
    "email": {
        "type": "string", 
        "format": "email"                  # ← Formato specifico
    },
    "category": {
        "type": "string",
        "enum": ["tech", "science", "art"] # ← Valori permessi
    }
}
```

## 🔄 COME CLAUDE USA LO SCHEMA

Quando Claude vuole chiamare `calculate_operation`:

1. **Legge lo schema**: parametro `operation` obbligatorio, tipo stringa

2. **Costruisce la chiamata**:
```json
{
  "method": "tools/call",
  "params": {
    "name": "calculate_operation",
    "arguments": {
      "operation": "2+2"  # ← Basato sullo schema
    }
  }
}
```

## ⚠️ ERRORI COMUNI SCHEMA
```python
# ❌ SBAGLIATO
"inputSchema": {
    "type": "string"  # ← DEVE ESSERE "object"
}

# ❌ SBAGLIATO  
"inputSchema": {
    "properties": {
        "param": {"type": "invalid_type"}  # ← Tipo non valido
    }
}

# ❌ SBAGLIATO
"inputSchema": {
    "properties": {...},
    "required": ["param_non_esistente"]  # ← Parametro inesistente
}
```

