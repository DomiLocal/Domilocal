"""
Test Manual de la API de Comercios - HU-V01

Este archivo contiene ejemplos de cómo probar la API utilizando requests.
Se puede ejecutar con: python mi_api/Comercio/test_comercios.py
"""

import requests
import json
from typing import dict

# URL base de la API
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1/comercios"


class TestComerciosAPI:
    """Clase para pruebas de la API de Comercios"""
    
    def __init__(self):
        self.base_url = API_BASE
        self.comercio_id_creado = None
    
    def test_1_registro_exitoso(self):
        """
        Caso 1: Registro exitoso
        Precondición: No existe comercio con mismo nombre y dirección
        Resultado esperado: HTTP 201, estado pendiente_aprobacion
        """
        print("\n" + "="*70)
        print("TEST 1: Registro Exitoso")
        print("="*70)
        
        datos = {
            "nombre": "Tienda La Esquina",
            "direccion": "Calle Principal 123, Apartamento 4B",
            "categoria": "tienda_barrio",
            "telefono": "+57 300 123 4567",
            "correo": "contacto@laesquina.com"
        }
        
        print(f"\n📤 Request: POST {self.base_url}/registro")
        print(f"📋 Datos: {json.dumps(datos, indent=2, ensure_ascii=False)}")
        
        response = requests.post(
            f"{self.base_url}/registro",
            json=datos
        )
        
        print(f"\n✅ Response Status: {response.status_code}")
        print(f"📊 Response Body:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        
        # Guardar el ID para pruebas posteriores
        if response.status_code == 201:
            self.comercio_id_creado = response.json()["data"]["id_comercio"]
            print(f"\n✓ Comercio creado con ID: {self.comercio_id_creado}")
        
        assert response.status_code == 201, f"Esperado 201, obtenido {response.status_code}"
        assert response.json()["success"] == True
        assert response.json()["data"]["estado"] == "pendiente_aprobacion"
        print("\n✅ TEST PASADO")
    
    def test_2_comercio_duplicado(self):
        """
        Caso 2: Comercio duplicado
        Precondición: Ya existe comercio con mismo nombre y dirección
        Resultado esperado: HTTP 409 Conflict
        """
        print("\n" + "="*70)
        print("TEST 2: Comercio Duplicado")
        print("="*70)
        
        datos = {
            "nombre": "Tienda La Esquina",
            "direccion": "Calle Principal 123, Apartamento 4B",
            "categoria": "restaurante",
            "telefono": "+57 301 987 6543",
            "correo": "otro@email.com"
        }
        
        print(f"\n📤 Request: POST {self.base_url}/registro")
        print(f"📋 Datos: {json.dumps(datos, indent=2, ensure_ascii=False)}")
        print("(Mismo nombre y dirección que el comercio anterior)")
        
        response = requests.post(
            f"{self.base_url}/registro",
            json=datos
        )
        
        print(f"\n✅ Response Status: {response.status_code}")
        print(f"📊 Response Body:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        
        assert response.status_code == 409, f"Esperado 409, obtenido {response.status_code}"
        assert response.json()["success"] == False
        print("\n✅ TEST PASADO")
    
    def test_3_categoria_invalida(self):
        """
        Caso 3: Categoría inválida
        Resultado esperado: HTTP 400 Bad Request
        """
        print("\n" + "="*70)
        print("TEST 3: Categoría Inválida")
        print("="*70)
        
        datos = {
            "nombre": "Negocio Raro",
            "direccion": "Calle Extraña 999",
            "categoria": "categoria_inexistente",
            "telefono": "+57 310 111 2222",
            "correo": "raro@email.com"
        }
        
        print(f"\n📤 Request: POST {self.base_url}/registro")
        print(f"📋 Datos: {json.dumps(datos, indent=2, ensure_ascii=False)}")
        
        response = requests.post(
            f"{self.base_url}/registro",
            json=datos
        )
        
        print(f"\n✅ Response Status: {response.status_code}")
        print(f"📊 Response Body:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        
        assert response.status_code == 400, f"Esperado 400, obtenido {response.status_code}"
        assert response.json()["success"] == False
        print("\n✅ TEST PASADO")
    
    def test_4_campos_faltantes(self):
        """
        Caso 4: Campos obligatorios faltantes
        Resultado esperado: HTTP 400 Bad Request
        """
        print("\n" + "="*70)
        print("TEST 4: Campos Obligatorios Faltantes")
        print("="*70)
        
        # Faltan varios campos
        datos = {
            "nombre": "Otro Comercio",
            "categoria": "farmacia"
            # Falta: dirección, teléfono, correo
        }
        
        print(f"\n📤 Request: POST {self.base_url}/registro")
        print(f"📋 Datos: {json.dumps(datos, indent=2, ensure_ascii=False)}")
        print("(Faltan campos obligatorios)")
        
        response = requests.post(
            f"{self.base_url}/registro",
            json=datos
        )
        
        print(f"\n✅ Response Status: {response.status_code}")
        print(f"📊 Response Body:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        
        assert response.status_code == 400, f"Esperado 400, obtenido {response.status_code}"
        assert response.json()["success"] == False
        print("\n✅ TEST PASADO")
    
    def test_5_obtener_comercio(self):
        """
        Caso 5: Obtener comercio por ID
        Resultado esperado: HTTP 200 OK
        """
        print("\n" + "="*70)
        print("TEST 5: Obtener Comercio por ID")
        print("="*70)
        
        if not self.comercio_id_creado:
            print("⚠️  Saltando: No hay comercio creado (ejecutar test 1 primero)")
            return
        
        print(f"\n📤 Request: GET {self.base_url}/{self.comercio_id_creado}")
        
        response = requests.get(
            f"{self.base_url}/{self.comercio_id_creado}"
        )
        
        print(f"\n✅ Response Status: {response.status_code}")
        print(f"📊 Response Body:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        
        assert response.status_code == 200, f"Esperado 200, obtenido {response.status_code}"
        assert response.json()["success"] == True
        print("\n✅ TEST PASADO")
    
    def test_6_listar_comercios_activos(self):
        """
        Caso 6: Listar comercios activos
        Resultado esperado: HTTP 200 OK, lista de comercios
        """
        print("\n" + "="*70)
        print("TEST 6: Listar Comercios Activos")
        print("="*70)
        
        print(f"\n📤 Request: GET {self.base_url}")
        
        response = requests.get(self.base_url)
        
        print(f"\n✅ Response Status: {response.status_code}")
        print(f"📊 Response Body:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        
        assert response.status_code == 200, f"Esperado 200, obtenido {response.status_code}"
        print("\n✅ TEST PASADO")
    
    def test_7_listar_comercios_pendientes(self):
        """
        Caso 7: Listar comercios pendientes (Admin)
        Resultado esperado: HTTP 200 OK, lista de comercios pendientes
        """
        print("\n" + "="*70)
        print("TEST 7: Listar Comercios Pendientes de Aprobación (Admin)")
        print("="*70)
        
        print(f"\n📤 Request: GET {self.base_url}/admin/pendientes")
        
        response = requests.get(
            f"{self.base_url}/admin/pendientes"
        )
        
        print(f"\n✅ Response Status: {response.status_code}")
        print(f"📊 Response Body:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        
        assert response.status_code == 200, f"Esperado 200, obtenido {response.status_code}"
        print("\n✅ TEST PASADO")
    
    def test_8_aprobar_comercio(self):
        """
        Caso 8: Aprobar comercio (Admin)
        Resultado esperado: HTTP 200 OK, estado cambia a activo
        """
        print("\n" + "="*70)
        print("TEST 8: Aprobar Comercio (Admin)")
        print("="*70)
        
        if not self.comercio_id_creado:
            print("⚠️  Saltando: No hay comercio creado (ejecutar test 1 primero)")
            return
        
        print(f"\n📤 Request: PUT {self.base_url}/{self.comercio_id_creado}/aprobar")
        
        response = requests.put(
            f"{self.base_url}/{self.comercio_id_creado}/aprobar"
        )
        
        print(f"\n✅ Response Status: {response.status_code}")
        print(f"📊 Response Body:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        
        assert response.status_code == 200, f"Esperado 200, obtenido {response.status_code}"
        assert response.json()["data"]["estado"] == "activo"
        print("\n✅ TEST PASADO - Comercio ahora es visible para clientes")
    
    def test_9_rechazar_comercio(self):
        """
        Caso 9: Rechazar comercio (Admin)
        Primero crea un comercio, luego lo rechaza
        Resultado esperado: HTTP 200 OK, estado cambia a rechazado
        """
        print("\n" + "="*70)
        print("TEST 9: Rechazar Comercio (Admin)")
        print("="*70)
        
        # Crear un comercio para rechazar
        datos = {
            "nombre": "Comercio Para Rechazar",
            "direccion": "Calle Temporal 555",
            "categoria": "panaderia",
            "telefono": "+57 311 222 3333",
            "correo": "temporal@email.com"
        }
        
        print(f"\n1️⃣  Creando comercio...")
        response_crear = requests.post(
            f"{self.base_url}/registro",
            json=datos
        )
        
        comercio_id = response_crear.json()["data"]["id_comercio"]
        print(f"   ✓ Comercio creado: {comercio_id}")
        
        # Rechazarlo
        print(f"\n2️⃣  Rechazando comercio...")
        print(f"   📤 Request: PUT {self.base_url}/{comercio_id}/rechazar")
        
        response_rechazar = requests.put(
            f"{self.base_url}/{comercio_id}/rechazar"
        )
        
        print(f"\n✅ Response Status: {response_rechazar.status_code}")
        print(f"📊 Response Body:")
        print(json.dumps(response_rechazar.json(), indent=2, ensure_ascii=False))
        
        assert response_rechazar.status_code == 200
        assert response_rechazar.json()["data"]["estado"] == "rechazado"
        print("\n✅ TEST PASADO")
    
    def test_10_comercio_no_encontrado(self):
        """
        Caso 10: Comercio no encontrado
        Resultado esperado: HTTP 404 Not Found
        """
        print("\n" + "="*70)
        print("TEST 10: Comercio No Encontrado")
        print("="*70)
        
        id_inexistente = "COM-NOEXISTE"
        
        print(f"\n📤 Request: GET {self.base_url}/{id_inexistente}")
        
        response = requests.get(
            f"{self.base_url}/{id_inexistente}"
        )
        
        print(f"\n✅ Response Status: {response.status_code}")
        print(f"📊 Response Body:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        
        assert response.status_code == 404, f"Esperado 404, obtenido {response.status_code}"
        print("\n✅ TEST PASADO")
    
    def run_all_tests(self):
        """Ejecuta todos los tests"""
        print("\n" + "🚀 "*35)
        print("SUITE DE PRUEBAS - API DE COMERCIOS (HU-V01)")
        print("🚀 "*35)
        
        try:
            self.test_1_registro_exitoso()
            self.test_2_comercio_duplicado()
            self.test_3_categoria_invalida()
            self.test_4_campos_faltantes()
            self.test_5_obtener_comercio()
            self.test_6_listar_comercios_activos()
            self.test_7_listar_comercios_pendientes()
            self.test_8_aprobar_comercio()
            self.test_9_rechazar_comercio()
            self.test_10_comercio_no_encontrado()
            
            print("\n" + "="*70)
            print("✅ TODOS LOS TESTS PASARON EXITOSAMENTE")
            print("="*70)
            
        except AssertionError as e:
            print(f"\n❌ TEST FALLÓ: {e}")
        except requests.exceptions.ConnectionError:
            print("\n❌ ERROR: No se puede conectar a la API")
            print("   Asegúrate de que el servidor está ejecutándose:")
            print("   python mi_api/Comercio/main.py")
        except Exception as e:
            print(f"\n❌ ERROR INESPERADO: {e}")


if __name__ == "__main__":
    # Ejecutar las pruebas
    tester = TestComerciosAPI()
    tester.run_all_tests()
    
    # Instrucciones
    print("\n" + "="*70)
    print("📖 INSTRUCCIONES DE USO:")
    print("="*70)
    print("""
1. Instalar dependencias:
   pip install -r requirements.txt

2. Ejecutar la API en otra terminal:
   python mi_api/Comercio/main.py

3. Ejecutar las pruebas (en esta terminal):
   python mi_api/Comercio/test_comercios.py

4. Acceder a Swagger UI:
   http://localhost:8000/docs

5. Acceder a ReDoc:
   http://localhost:8000/redoc
    """)
