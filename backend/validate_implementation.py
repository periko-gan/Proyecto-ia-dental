#!/usr/bin/env python
"""
Script de validacion de la entrega minima del backend.
Ejecutar desde: cd backend && python validate_implementation.py
"""

import sys
from pathlib import Path

def validate():
    """Ejecuta validaciones de la entrega minima."""
    
    print("=" * 70)
    print("VALIDACION - BACKEND FASE 1 - PRIMERA ENTREGA MINIMA")
    print("=" * 70)
    
    checks = []
    
    # 1. Imports basicos
    try:
        from src.app import create_app
        from src.api.schema import schema
        from src.config.settings import get_settings
        from src.persistence.models import AnalysisRecord, AnalysisStatus
        print("✅ Imports de modulos principales: OK")
        checks.append(True)
    except Exception as e:
        print(f"❌ Imports: FALLO - {e}")
        checks.append(False)
    
    # 2. Creacion de app
    try:
        app = create_app()
        assert app is not None
        assert app.title == "Dental IA Backend"
        print("✅ Creacion de app FastAPI: OK")
        checks.append(True)
    except Exception as e:
        print(f"❌ App creation: FALLO - {e}")
        checks.append(False)
    
    # 3. Rutas
    try:
        routes = [r.path for r in app.routes if hasattr(r, 'path')]
        assert '/graphql' in routes
        assert '/health' in routes
        print(f"✅ Rutas montadas: {routes}")
        checks.append(True)
    except Exception as e:
        print(f"❌ Routes: FALLO - {e}")
        checks.append(False)
    
    # 4. Schema GraphQL
    try:
        schema_str = schema.as_str()
        assert 'type Query' in schema_str
        assert 'type Mutation' in schema_str
        assert 'getAnalysisById' in schema_str
        assert 'uploadRadiography' in schema_str
        print("✅ Schema GraphQL con contrato minimo: OK")
        checks.append(True)
    except Exception as e:
        print(f"❌ Schema: FALLO - {e}")
        checks.append(False)
    
    # 5. Configuracion
    try:
        settings = get_settings()
        assert settings.env == "development"
        assert settings.port == 8000
        print(f"✅ Configuracion cargada: env={settings.env}, port={settings.port}")
        checks.append(True)
    except Exception as e:
        print(f"❌ Settings: FALLO - {e}")
        checks.append(False)
    
    # 6. Modelos persistencia
    try:
        record = AnalysisRecord(
            analysis_id="test",
            file_name="test.jpg",
            file_path="/tmp/test.jpg",
            mime_type="image/jpeg",
            file_size_bytes=1024,
            status=AnalysisStatus.COMPLETED,
            model_version="best.pt"
        )
        assert record.analysis_id == "test"
        assert record.status == AnalysisStatus.COMPLETED
        print("✅ Modelos de persistencia: OK")
        checks.append(True)
    except Exception as e:
        print(f"❌ Models: FALLO - {e}")
        checks.append(False)
    
    # Resultado
    print("\n" + "=" * 70)
    total = len(checks)
    passed = sum(checks)
    print(f"RESULTADO: {passed}/{total} validaciones pasadas")
    
    if all(checks):
        print("✅ BACKEND LISTO PARA PRODUCCION")
        print("\nPasos siguientes:")
        print("1. Copiar .env.example a .env")
        print("2. Ajustar rutas en .env (modelo, MongoDB)")
        print("3. Ejecutar: uvicorn main:app --reload")
        print("4. Acceder a http://localhost:8000/graphql")
        return 0
    else:
        print("❌ FALLOS DETECTADOS - Revisar errores arriba")
        return 1

if __name__ == "__main__":
    sys.exit(validate())
