"""
Script de verificación del entorno
"""
print("=" * 60)
print("Verificando Mechanic Diagnostic Assistant")
print("=" * 60)

# Test 1: Imports básicos
print("\n[1/5] Verificando imports...")
try:
    from src.agent.tools import get_all_tools
    from src.utils.config import get_config_summary
    print("✅ Imports correctos")
except ImportError as e:
    print(f"❌ Error en imports: {e}")
    exit(1)

# Test 2: Herramientas
print("\n[2/5] Cargando herramientas...")
try:
    tools = get_all_tools()
    print(f"✅ {len(tools)} herramientas cargadas:")
    for tool in tools:
        print(f"   - {tool.name}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 3: Configuración
print("\n[3/5] Verificando configuración...")
try:
    config = get_config_summary()
    print("✅ Configuración:")
    for key, value in config.items():
        print(f"   - {key}: {value}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 4: Datos
print("\n[4/5] Verificando archivos de datos...")
try:
    from src.utils.config import OBD_CODES_PATH, SYMPTOMS_PATH, REPAIR_GUIDES_PATH
    import os
    
    files = {
        "OBD Codes": OBD_CODES_PATH,
        "Symptoms": SYMPTOMS_PATH,
        "Repair Guides": REPAIR_GUIDES_PATH
    }
    
    for name, path in files.items():
        if os.path.exists(path):
            print(f"   ✅ {name}")
        else:
            print(f"   ❌ {name} NO ENCONTRADO")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 5: Document loading
print("\n[5/5] Probando carga de documentos...")
try:
    from src.rag.document_loader import load_all_knowledge_base
    from src.utils.config import OBD_CODES_PATH, SYMPTOMS_PATH, REPAIR_GUIDES_PATH
    
    docs = load_all_knowledge_base(OBD_CODES_PATH, SYMPTOMS_PATH, REPAIR_GUIDES_PATH)
    print(f"✅ {len(docs)} documentos cargados correctamente")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 60)
print("✅ VERIFICACIÓN COMPLETADA")
print("=" * 60)
print("\nPróximos pasos:")
print("1. Configurar API keys en .env")
print("2. Ejecutar: python app.py")
print("3. Abrir: http://localhost:7860")
print("=" * 60)
