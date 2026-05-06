"""
============================================================
PROYECTO MONGODB - SISTEMA DE VENTAS E-COMMERCE
Archivo: aplicacion_principal.py
Finalidad: Integración Python + MongoDB, Menú Interactivo y Validación Lógica
============================================================
"""

from pymongo import MongoClient
from datetime import datetime
import sys
import re

# ============================================================
# CONFIGURACIÓN Y CONEXIÓN
# ============================================================

def conectar():
    """Conecta a MongoDB y retorna la base de datos."""
    try:
        cliente = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=3000)
        cliente.server_info()
        db = cliente["tienda_ecommerce"]
        print("✅ Conexión exitosa a MongoDB\n")
        return db
    except Exception as e:
        print(f"❌ Error al conectar a MongoDB: {e}")
        sys.exit(1)

# ============================================================
# UTILIDADES DE FORMATO
# ============================================================

def separador(titulo=""):
    """Imprime una línea separadora con título para mejorar la lectura en consola."""
    largo = 65
    if titulo:
        padding = (largo - len(titulo) - 2) // 2
        print("\n" + "=" * padding + f" {titulo} " + "=" * padding)
    else:
        print("\n" + "=" * largo)

def formatear_precio(precio):
    """Formatea un número como precio en pesos chilenos."""
    return f"${precio:,.0f}".replace(",", ".")

def mostrar_cliente(cliente):
    """Muestra los datos de un cliente de forma estructurada."""
    fecha = cliente.get('fecha_registro', '')
    if isinstance(fecha, datetime):
        fecha = fecha.strftime("%d/%m/%Y")
    print(f"  👤 {cliente.get('nombre', 'N/A')}")
    print(f"     ID             : {cliente.get('id_cliente', 'N/A')}")
    print(f"     Email          : {cliente.get('email', 'N/A')}")
    print(f"     Teléfono       : {cliente.get('telefono', 'N/A')}")
    dir_ = cliente.get('direccion', {})
    print(f"     Dirección      : {dir_.get('calle', '')}, {dir_.get('ciudad', '')}, {dir_.get('region', '')}")
    print(f"     Fecha registro : {fecha}")

def mostrar_producto(prod):
    """Muestra los datos de un producto, incluyendo sus atributos dinámicos."""
    print(f"  📦 {prod.get('nombre', 'N/A')}")
    print(f"     ID        : {prod.get('id_producto', 'N/A')}")
    print(f"     Categoría : {prod.get('categoria', 'N/A')}")
    print(f"     Precio    : {formatear_precio(prod.get('precio', 0))}")
    print(f"     Stock     : {prod.get('stock', 0)} unidades")
    
    # Mostrar atributos si existen
    atributos = prod.get('atributos', {})
    if atributos:
        print("     Atributos :")
        for clave, valor in atributos.items():
            print(f"               - {clave.capitalize()}: {valor}")

def mostrar_pedido(pedido):
    """
    Muestra los datos de un pedido.
    Se agregó la funcionalidad para iterar y mostrar el detalle de los productos comprados.
    """
    fecha = pedido.get('fecha', '')
    if isinstance(fecha, datetime):
        fecha = fecha.strftime("%d/%m/%Y")
    print(f"  🛒 Pedido: {pedido.get('id_pedido', 'N/A')}")
    print(f"     Fecha   : {fecha}")
    print(f"     Estado  : {pedido.get('estado', 'N/A').upper()}")
    cli = pedido.get('cliente', {})
    print(f"     Cliente : {cli.get('nombre', 'N/A')}")
    
    # Iteración sobre el arreglo de subdocumentos para mostrar el detalle
    detalle = pedido.get('detalle_pedido', [])
    if detalle:
        print("     Detalle :")
        for item in detalle:
            nombre_prod = item.get('nombre', 'N/A')
            cantidad = item.get('cantidad', 0)
            precio_u = item.get('precio_unitario', 0)
            print(f"               - {cantidad}x {nombre_prod} ({formatear_precio(precio_u)} c/u)")
            
    print(f"     TOTAL   : {formatear_precio(pedido.get('total', 0))}")

# ============================================================
# VALIDACIONES DE ENTRADA
# ============================================================

def validar_email(email):
    """Valida formato de email con expresiones regulares."""
    patron = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
    return bool(re.match(patron, email))

def validar_precio(valor):
    """Valida que el precio ingresado sea un número positivo."""
    try:
        precio = float(valor)
        return precio > 0, precio
    except ValueError:
        return False, 0

def validar_entero_positivo(valor):
    """Valida que la cantidad o stock sea un entero positivo."""
    try:
        num = int(valor)
        return num > 0, num
    except ValueError:
        return False, 0

# ============================================================
# OPERACIONES CRUD
# ============================================================

class SistemaVentas:
    def __init__(self, db):
        self.db = db
        self.clientes = db.clientes
        self.productos = db.productos
        self.pedidos = db.pedidos

    # ---------- CREATE ----------

    def insertar_cliente(self):
        separador("INSERTAR CLIENTE")
        nombre = input("Nombre del cliente: ").strip()
        if not nombre: return print("❌ El nombre no puede estar vacío.")

        email = input("Email: ").strip()
        if not validar_email(email): return print("❌ Email inválido.")

        if self.clientes.find_one({"email": email}):
            return print(f"❌ Ya existe un cliente con el email {email}.")

        telefono = input("Teléfono: ").strip()
        calle = input("Calle y número: ").strip()
        ciudad = input("Ciudad: ").strip()
        region = input("Región: ").strip()

        ultimo = self.clientes.find_one(sort=[("id_cliente", -1)])
        nuevo_num = int(ultimo["id_cliente"][3:]) + 1 if ultimo else 1
        nuevo_id = f"CLI{nuevo_num:03d}"

        nuevo_cliente = {
            "id_cliente": nuevo_id,
            "nombre": nombre,
            "email": email,
            "telefono": telefono,
            "direccion": {"calle": calle, "ciudad": ciudad, "region": region},
            "fecha_registro": datetime.now(),
            "historial_compras": []
        }
        self.clientes.insert_one(nuevo_cliente)
        print(f"\n✅ Cliente insertado con ID: {nuevo_id}")

    def insertar_producto(self):
        separador("INSERTAR PRODUCTO")
        nombre = input("Nombre del producto: ").strip()
        if not nombre: return print("❌ El nombre no puede estar vacío.")

        categoria = input("Categoría: ").strip()
        
        precio_str = input("Precio: ").strip()
        valido, precio = validar_precio(precio_str)
        if not valido: return print("❌ Precio inválido. Debe ser número mayor a 0.")

        stock_str = input("Stock: ").strip()
        valido, stock = validar_entero_positivo(stock_str)
        if not valido: return print("❌ Stock inválido. Debe ser número entero mayor a 0.")

        print("\n--- Atributos Específicos del Producto ---")
        print("Puedes agregar características como talla, color, marca, etc.")
        atributos = {}
        while True:
            clave = input("Ingresa el nombre del atributo (o escribe 'listo' para terminar): ").strip().lower()
            if clave == 'listo':
                break
            if not clave:
                print("❌ El nombre del atributo no puede estar vacío.")
                continue
            
            valor = input(f"Ingresa el valor para '{clave}': ").strip()
            if not valor:
                print("❌ El valor no puede estar vacío.")
                continue
                
            atributos[clave] = valor
            print(f"✅ Atributo guardado -> {clave}: {valor}")

        ultimo = self.productos.find_one(sort=[("id_producto", -1)])
        nuevo_num = int(ultimo["id_producto"][4:]) + 1 if ultimo else 1
        nuevo_id = f"PROD{nuevo_num:03d}"

        nuevo_producto = {
            "id_producto": nuevo_id,
            "nombre": nombre,
            "categoria": categoria,
            "precio": int(precio),
            "stock": stock,
            "atributos": atributos
        }
        self.productos.insert_one(nuevo_producto)
        print(f"\n✅ Producto insertado con ID: {nuevo_id}")

    def insertar_pedido(self):
        separador("INSERTAR PEDIDO")
        id_cliente = input("Ingresa el ID del cliente: ").strip().upper()
        cli = self.clientes.find_one({"id_cliente": id_cliente})
        if not cli: return print("❌ No se encontró el cliente en la base de datos.")

        detalle = []
        total = 0
        while True:
            id_prod = input("\nID del producto (o escribe 'listo' para terminar): ").strip().upper()
            if id_prod == "LISTO":
                if not detalle: return print("❌ El pedido no puede estar vacío. Operación cancelada.")
                break

            prod = self.productos.find_one({"id_producto": id_prod})
            if not prod:
                print("❌ Producto no encontrado.")
                continue

            cant_str = input(f"Cantidad de '{prod['nombre']}': ").strip()
            valido, cantidad = validar_entero_positivo(cant_str)
            if not valido:
                print("❌ Cantidad inválida.")
                continue
                
            if cantidad > prod["stock"]:
                print(f"❌ Stock insuficiente. Solo quedan {prod['stock']} unidades.")
                continue

            subtotal = prod["precio"] * cantidad
            total += subtotal
            detalle.append({
                "producto": id_prod,
                "nombre": prod["nombre"],
                "cantidad": cantidad,
                "precio_unitario": prod["precio"]
            })
            print(f"✅ Agregado al carrito.")

        ultimo = self.pedidos.find_one(sort=[("id_pedido", -1)])
        nuevo_num = int(ultimo["id_pedido"][3:]) + 1 if ultimo else 1
        nuevo_id = f"PED{nuevo_num:03d}"

        nuevo_pedido = {
            "id_pedido": nuevo_id,
            "fecha": datetime.now(),
            "estado": "procesando",
            "cliente": {"id_cliente": cli["id_cliente"], "nombre": cli["nombre"], "email": cli["email"]},
            "detalle_pedido": detalle,
            "total": total
        }

        self.pedidos.insert_one(nuevo_pedido)
        self.clientes.update_one({"id_cliente": id_cliente}, {"$push": {"historial_compras": nuevo_id}})
        
        for item in detalle:
            self.productos.update_one(
                {"id_producto": item["producto"]},
                {"$inc": {"stock": -item["cantidad"]}}
            )

        print(f"\n✅ Pedido insertado exitosamente con ID: {nuevo_id}")
        print("✅ El stock de los productos ha sido actualizado automáticamente.")

    # ---------- READ ----------

    def listar_clientes(self):
        separador("TODOS LOS CLIENTES")
        clientes = list(self.clientes.find({}, {"_id": 0}))
        if not clientes: return print("No hay clientes registrados.")
        for c in clientes: mostrar_cliente(c); print()

    def listar_productos(self):
        separador("TODOS LOS PRODUCTOS")
        productos = list(self.productos.find({}, {"_id": 0}))
        if not productos: return print("No hay productos registrados.")
        for p in productos: mostrar_producto(p); print()

    def listar_pedidos(self):
        separador("TODOS LOS PEDIDOS")
        pedidos = list(self.pedidos.find({}, {"_id": 0}))
        if not pedidos: return print("No hay pedidos registrados.")
        for ped in pedidos: mostrar_pedido(ped); print()

    def buscar_cliente_por_nombre(self):
        separador("BUSCAR CLIENTE POR NOMBRE")
        termino = input("Ingresa parte del nombre: ").strip()
        resultados = list(self.clientes.find({"nombre": {"$regex": termino, "$options": "i"}}, {"_id": 0}))
        if not resultados: return print("No se encontraron coincidencias.")
        for c in resultados: mostrar_cliente(c); print()

    def buscar_productos_por_rango_precio(self):
        separador("PRODUCTOS POR RANGO DE PRECIO")
        min_p = input("Precio mínimo: ").strip()
        max_p = input("Precio máximo: ").strip()
        if min_p.isdigit() and max_p.isdigit():
            resultados = list(self.productos.find({"precio": {"$gte": int(min_p), "$lte": int(max_p)}}, {"_id": 0}))
            if not resultados: return print("No se encontraron productos en ese rango.")
            for p in resultados: mostrar_producto(p); print()
        else:
            print("❌ Valores inválidos. Deben ser números enteros.")

    def buscar_pedidos_por_fecha(self):
        separador("PEDIDOS POR RANGO DE FECHA")
        print("Formato requerido: DD-MM-YYYY")
        try:
            dt_ini = datetime.strptime(input("Fecha inicio: ").strip(), "%d-%m-%Y")
            dt_fin = datetime.strptime(input("Fecha fin: ").strip(), "%d-%m-%Y")
            resultados = list(self.pedidos.find({"fecha": {"$gte": dt_ini, "$lte": dt_fin}}, {"_id": 0}))
            if not resultados: return print("No se encontraron pedidos en esas fechas.")
            for ped in resultados: mostrar_pedido(ped); print()
        except ValueError:
            print("❌ Formato de fecha inválido. Asegúrate de usar guiones (ej: 01-12-2024).")

    def buscar_pedidos_con_producto(self):
        separador("PEDIDOS CON PRODUCTO ESPECÍFICO")
        id_prod = input("Ingresa el ID del producto: ").strip().upper()
        resultados = list(self.pedidos.find({"detalle_pedido.producto": id_prod}, {"_id": 0}))
        if not resultados: return print("El producto no está asociado a ningún pedido.")
        for ped in resultados: mostrar_pedido(ped); print()

    def filtros_de_busqueda_dinamicos(self):
        while True:
            separador("SUBMENÚ DE FILTROS AVANZADOS")
            print("  1. Filtrar por exclusión de valor          - Operador $ne")
            print("  2. Filtrar por valor estrictamente mayor   - Operador $gt")
            print("  3. Filtrar por valor mayor o igual         - Operador $gte")
            print("  4. Filtrar por valor estrictamente menor   - Operador $lt")
            print("  5. Filtrar por valor menor o igual         - Operador $lte")
            print("  6. Filtrar por coincidencia en lista       - Operador $in")
            print("  7. Requerir múltiples condiciones          - Operador $and")
            print("  8. Requerir al menos una condición         - Operador $or")
            print("  0. Volver al menú principal")
            
            opcion = input("\nSelecciona una lógica de filtrado: ").strip()

            if opcion == "0":
                break
            elif opcion == "1":
                valor = input("Ingresa el precio a excluir: ")
                if valor.isdigit():
                    resultados = list(self.productos.find({"precio": {"$ne": int(valor)}}, {"_id": 0}))
                    for r in resultados: mostrar_producto(r); print()
            elif opcion == "2":
                valor = input("Ingresa el umbral mínimo del total: ")
                if valor.isdigit():
                    resultados = list(self.pedidos.find({"total": {"$gt": int(valor)}}, {"_id": 0}))
                    for r in resultados: mostrar_pedido(r); print()
            elif opcion == "3":
                valor = input("Ingresa el umbral mínimo de stock: ")
                if valor.isdigit():
                    resultados = list(self.productos.find({"stock": {"$gte": int(valor)}}, {"_id": 0}))
                    for r in resultados: mostrar_producto(r); print()
            elif opcion == "4":
                valor = input("Ingresa el umbral máximo de precio: ")
                if valor.isdigit():
                    resultados = list(self.productos.find({"precio": {"$lt": int(valor)}}, {"_id": 0}))
                    for r in resultados: mostrar_producto(r); print()
            elif opcion == "5":
                valor = input("Ingresa el umbral máximo del total: ")
                if valor.isdigit():
                    resultados = list(self.pedidos.find({"total": {"$lte": int(valor)}}, {"_id": 0}))
                    for r in resultados: mostrar_pedido(r); print()
            elif opcion == "6":
                categorias_str = input("Ingresa categorías separadas por coma (ej: Ropa, Electrónica): ")
                lista_categorias = [c.strip() for c in categorias_str.split(",")]
                resultados = list(self.productos.find({"categoria": {"$in": lista_categorias}}, {"_id": 0}))
                for r in resultados: mostrar_producto(r); print()
            elif opcion == "7":
                cat = input("Ingresa la categoría requerida: ").strip()
                precio = input("Ingresa el límite máximo de precio: ").strip()
                if precio.isdigit():
                    consulta = {"$and": [{"categoria": cat}, {"precio": {"$lt": int(precio)}}]}
                    resultados = list(self.productos.find(consulta, {"_id": 0}))
                    for r in resultados: mostrar_producto(r); print()
            elif opcion == "8":
                ciudad1 = input("Ingresa la primera ciudad: ").strip()
                ciudad2 = input("Ingresa la segunda ciudad: ").strip()
                consulta = {"$or": [{"direccion.ciudad": ciudad1}, {"direccion.ciudad": ciudad2}]}
                resultados = list(self.clientes.find(consulta, {"_id": 0}))
                for c in resultados: mostrar_cliente(c); print()
            else:
                print("❌ Opción no válida.")

    # ---------- UPDATE ----------

    def actualizar_cliente(self):
        separador("ACTUALIZAR CLIENTE")
        id_cli = input("Ingresa el ID del cliente: ").strip().upper()
        if not self.clientes.find_one({"id_cliente": id_cli}): return print("❌ Cliente no encontrado.")
        
        print("\n¿Qué dato deseas modificar?")
        print("1. Nombre")
        print("2. Email")
        print("3. Teléfono")
        print("4. Dirección (Calle y Número)")
        print("5. Dirección (Ciudad)")
        print("6. Dirección (Región)")
        print("0. Cancelar")
        
        opcion = input("\nSelecciona una opción: ").strip()
        campo_db = ""
        nuevo_valor = ""
        
        if opcion == "1":
            campo_db = "nombre"
            nuevo_valor = input("Ingresa el nuevo nombre: ").strip()
        elif opcion == "2":
            campo_db = "email"
            nuevo_valor = input("Ingresa el nuevo email: ").strip()
            if not validar_email(nuevo_valor): return print("❌ Email inválido. Operación cancelada.")
        elif opcion == "3":
            campo_db = "telefono"
            nuevo_valor = input("Ingresa el nuevo teléfono: ").strip()
        elif opcion == "4":
            campo_db = "direccion.calle"
            nuevo_valor = input("Ingresa la nueva calle y número: ").strip()
        elif opcion == "5":
            campo_db = "direccion.ciudad"
            nuevo_valor = input("Ingresa la nueva ciudad: ").strip()
        elif opcion == "6":
            campo_db = "direccion.region"
            nuevo_valor = input("Ingresa la nueva región: ").strip()
        elif opcion == "0":
            return print("❌ Operación cancelada.")
        else:
            return print("❌ Opción no válida. Operación cancelada.")

        if not nuevo_valor: 
            return print("❌ El valor no puede estar vacío. Operación cancelada.")
        
        self.clientes.update_one({"id_cliente": id_cli}, {"$set": {campo_db: nuevo_valor}})
        print(f"✅ Información de cliente actualizada correctamente ({campo_db}).")

    def actualizar_producto(self):
        """Menú consolidado para modificar varios campos lógicos de un producto."""
        separador("ACTUALIZAR PRODUCTO")
        id_prod = input("ID del producto: ").strip().upper()
        prod = self.productos.find_one({"id_producto": id_prod})
        if not prod: return print("❌ Producto no encontrado.")
        
        print(f"\n¿Qué dato de '{prod['nombre']}' deseas modificar?")
        print("1. Nombre")
        print("2. Precio")
        print("3. Stock")
        print("4. Atributos (ej: talla, color, marca)")
        print("0. Cancelar")
        
        opcion = input("\nSelecciona una opción: ").strip()
        
        if opcion == "1":
            nuevo_nombre = input("Ingresa el nuevo nombre: ").strip()
            if not nuevo_nombre: return print("❌ El nombre no puede estar vacío. Operación cancelada.")
            self.productos.update_one({"id_producto": id_prod}, {"$set": {"nombre": nuevo_nombre}})
            print("✅ Nombre del producto actualizado.")
            
        elif opcion == "2":
            nuevo_precio = input("Ingresa el nuevo precio: ").strip()
            valido, precio = validar_precio(nuevo_precio)
            if not valido: return print("❌ Precio inválido. Operación cancelada.")
            self.productos.update_one({"id_producto": id_prod}, {"$set": {"precio": int(precio)}})
            print("✅ Precio del producto actualizado.")
            
        elif opcion == "3":
            print(f"Stock actual: {prod['stock']}")
            nuevo_stock = input("Ingresa el nuevo stock total: ").strip()
            if nuevo_stock.isdigit() and int(nuevo_stock) >= 0:
                self.productos.update_one({"id_producto": id_prod}, {"$set": {"stock": int(nuevo_stock)}})
                print("✅ Stock actualizado exitosamente.")
            else:
                print("❌ Stock inválido. Debe ser un número entero mayor o igual a cero. Operación cancelada.")
                
        elif opcion == "4":
            clave = input("Ingresa el nombre del atributo a modificar o agregar (ej: color): ").strip().lower()
            if not clave: return print("❌ El nombre del atributo no puede estar vacío.")
            valor = input(f"Ingresa el nuevo valor para '{clave}': ").strip()
            if not valor: return print("❌ El valor no puede estar vacío.")
            self.productos.update_one({"id_producto": id_prod}, {"$set": {f"atributos.{clave}": valor}})
            print(f"✅ Atributo '{clave}' actualizado a '{valor}'.")
            
        elif opcion == "0":
            return print("❌ Operación cancelada.")
        else:
            return print("❌ Opción no válida. Operación cancelada.")

    def actualizar_pedido(self):
        """Menú consolidado para modificar estado o cantidades, autocalculando el total."""
        separador("ACTUALIZAR PEDIDO")
        id_ped = input("ID del pedido: ").strip().upper()
        pedido = self.pedidos.find_one({"id_pedido": id_ped})
        if not pedido: return print("❌ Pedido no encontrado.")
        
        print("\n¿Qué dato del pedido deseas modificar?")
        print("1. Estado del pedido (ej. procesando, enviado, entregado)")
        print("2. Cantidad de un producto en el pedido")
        print("0. Cancelar")
        
        opcion = input("\nSelecciona una opción: ").strip()
        
        if opcion == "1":
            nuevo_est = input("Nuevo estado: ").strip().lower()
            if not nuevo_est: return print("❌ El estado no puede estar vacío. Operación cancelada.")
            self.pedidos.update_one({"id_pedido": id_ped}, {"$set": {"estado": nuevo_est}})
            print(f"✅ Estado del pedido actualizado a '{nuevo_est}'.")
            
        elif opcion == "2":
            id_prod = input("ID del producto a modificar: ").strip().upper()
            
            # Verificamos si el producto existe dentro del pedido
            item_actual = next((item for item in pedido.get("detalle_pedido", []) if item["producto"] == id_prod), None)
            if not item_actual:
                return print("❌ Ese producto no se encuentra dentro del pedido indicado.")
                
            print(f"Cantidad actual de '{item_actual.get('nombre', 'N/A')}': {item_actual['cantidad']}")
            nueva_cant = input("Nueva cantidad (0 para eliminar el producto): ").strip()
            
            if nueva_cant.isdigit() and int(nueva_cant) >= 0:
                cant_int = int(nueva_cant)
                if cant_int == 0:
                    # Elimina el producto del arreglo
                    self.pedidos.update_one(
                        {"id_pedido": id_ped},
                        {"$pull": {"detalle_pedido": {"producto": id_prod}}}
                    )
                    print("✅ Producto eliminado del pedido (cantidad 0).")
                else:
                    # Actualiza la cantidad
                    self.pedidos.update_one(
                        {"id_pedido": id_ped, "detalle_pedido.producto": id_prod},
                        {"$set": {"detalle_pedido.$.cantidad": cant_int}}
                    )
                    print("✅ Cantidad en el pedido actualizada.")
                
                # RECALCULAR EL TOTAL AUTOMÁTICAMENTE
                pedido_actualizado = self.pedidos.find_one({"id_pedido": id_ped})
                nuevo_total = sum(item["cantidad"] * item["precio_unitario"] for item in pedido_actualizado.get("detalle_pedido", []))
                self.pedidos.update_one({"id_pedido": id_ped}, {"$set": {"total": nuevo_total}})
                print(f"✅ El TOTAL del pedido ha sido recalculado automáticamente: {formatear_precio(nuevo_total)}")
                
            else:
                print("❌ Cantidad inválida. Operación cancelada.")
                
        elif opcion == "0":
            return print("❌ Operación cancelada.")
        else:
            return print("❌ Opción no válida. Operación cancelada.")

    def actualizar_historial_compras(self):
        separador("ACTUALIZAR HISTORIAL")
        id_cli = input("ID del cliente: ").strip().upper()
        if not self.clientes.find_one({"id_cliente": id_cli}): return print("❌ Cliente no encontrado.")
        
        id_ped = input("ID del pedido a vincular: ").strip().upper()
        if not self.pedidos.find_one({"id_pedido": id_ped}): return print("❌ Pedido no encontrado.")
        
        self.clientes.update_one({"id_cliente": id_cli}, {"$push": {"historial_compras": id_ped}})
        print("✅ Historial de compras del cliente actualizado.")

    # ---------- DELETE ----------

    def eliminar_cliente(self):
        separador("ELIMINAR CLIENTE")

        print("Clientes disponibles:")
        for c in self.clientes.find({}, {"_id": 0, "id_cliente": 1, "nombre": 1}):
            print(f"  {c['id_cliente']}  →  {c['nombre']}")

        id_cli = input("\nID del cliente a eliminar: ").strip().upper()
        cliente = self.clientes.find_one({"id_cliente": id_cli})
        if not cliente: return print("❌ Cliente no encontrado.")

        pedidos_activos = self.pedidos.count_documents({"cliente.id_cliente": id_cli})
        if pedidos_activos > 0:
            print(f"❌ ACCIÓN BLOQUEADA: No se puede eliminar a este cliente porque tiene {pedidos_activos} pedido(s) asociado(s) en el sistema.")
            return

        print(f"\nCliente a eliminar: {cliente['nombre']} ({cliente['email']})")
        confirmacion = input("¿Estás completamente seguro de eliminar este cliente? (si/no): ").strip().lower()
        if confirmacion == "si":
            self.clientes.delete_one({"id_cliente": id_cli})
            print("✅ Cliente eliminado permanentemente.")
        else:
            print("❌ Eliminación cancelada.")

    def eliminar_producto(self):
        separador("ELIMINAR PRODUCTO")

        print("Productos disponibles:")
        for p in self.productos.find({}, {"_id": 0, "id_producto": 1, "nombre": 1, "precio": 1}):
            print(f"  {p['id_producto']}  →  {p['nombre']:<40}  {formatear_precio(p['precio'])}")

        id_prod = input("\nID del producto a eliminar: ").strip().upper()
        prod = self.productos.find_one({"id_producto": id_prod})
        if not prod: return print("❌ Producto no encontrado.")

        en_pedidos = self.pedidos.count_documents({"detalle_pedido.producto": id_prod})
        if en_pedidos > 0:
            print(f"❌ ACCIÓN BLOQUEADA: No se puede eliminar este producto porque aparece en {en_pedidos} boleta(s) o pedido(s).")
            return

        print(f"\nProducto a eliminar: {prod['nombre']} | {formatear_precio(prod['precio'])}")
        confirmacion = input("¿Estás seguro de eliminar este producto del catálogo? (si/no): ").strip().lower()
        if confirmacion == "si":
            self.productos.delete_one({"id_producto": id_prod})
            print("✅ Producto eliminado permanentemente.")
        else:
            print("❌ Eliminación cancelada.")

    def eliminar_pedido(self):
        separador("ELIMINAR PEDIDO")

        print("Pedidos disponibles:")
        for ped in self.pedidos.find({}, {"_id": 0, "id_pedido": 1, "cliente": 1, "estado": 1, "total": 1}):
            fecha = ped.get("fecha", "")
            print(f"  {ped['id_pedido']}  →  {ped['cliente']['nombre']:<25}  {ped['estado']:<14}  {formatear_precio(ped['total'])}")

        id_ped = input("\nID del pedido a eliminar: ").strip().upper()
        pedido_existente = self.pedidos.find_one({"id_pedido": id_ped})
        if not pedido_existente: return print("❌ Pedido no encontrado.")

        print(f"\nPedido a eliminar:")
        print(f"  ID      : {pedido_existente['id_pedido']}")
        print(f"  Cliente : {pedido_existente['cliente']['nombre']}")
        print(f"  Estado  : {pedido_existente['estado']}")
        print(f"  Total   : {formatear_precio(pedido_existente['total'])}")

        confirmacion = input(f"\n¿Estás seguro de eliminar el pedido {id_ped}? (si/no): ").strip().lower()
        if confirmacion == "si":
            self.pedidos.delete_one({"id_pedido": id_ped})
            id_cliente = pedido_existente["cliente"]["id_cliente"]
            self.clientes.update_one({"id_cliente": id_cliente}, {"$pull": {"historial_compras": id_ped}})
            print("✅ Pedido eliminado permanentemente y removido del historial del cliente.")
        else:
            print("❌ Eliminación cancelada.")


# ============================================================
# MENÚ PRINCIPAL
# ============================================================

def mostrar_menu():
    print("\n" + "═" * 85)
    print(" SISTEMA DE VENTAS E-COMMERCE - MongoDB ".center(85))
    print("═" * 85)
    print("\n CREAR")
    print("    1. Insertar nuevo cliente")
    print("    2. Insertar nuevo producto")
    print("    3. Insertar nuevo pedido")
    print("\n LEER")
    print("    4. Listar todos los clientes")
    print("    5. Listar todos los productos")
    print("    6. Listar todos los pedidos")
    print("    7. Buscar cliente por nombre parcial")
    print("    8. Buscar productos por rango de precio")
    print("    9. Buscar pedidos por rango de fecha")
    print("   10. Buscar pedidos con producto específico")
    print("   11. Filtros de búsqueda avanzados")
    print("\n ACTUALIZAR")
    print("   12. Actualizar datos de cliente")
    print("   13. Actualizar datos de producto")
    print("   14. Actualizar datos de pedido")
    print("   15. Actualizar historial de compras de cliente")
    print("\n ELIMINAR")
    print("   16. Eliminar cliente")
    print("   17. Eliminar producto")
    print("   18. Eliminar pedido")
    print("\n" + "─" * 85)
    print("    0. Salir")
    print("═" * 85)

def main():
    db = conectar()
    sistema = SistemaVentas(db)

    opciones = {
        "1":  sistema.insertar_cliente,
        "2":  sistema.insertar_producto,
        "3":  sistema.insertar_pedido,
        "4":  sistema.listar_clientes,
        "5":  sistema.listar_productos,
        "6":  sistema.listar_pedidos,
        "7":  sistema.buscar_cliente_por_nombre,
        "8":  sistema.buscar_productos_por_rango_precio,
        "9":  sistema.buscar_pedidos_por_fecha,
        "10": sistema.buscar_pedidos_con_producto,
        "11": sistema.filtros_de_busqueda_dinamicos,
        "12": sistema.actualizar_cliente,
        "13": sistema.actualizar_producto,
        "14": sistema.actualizar_pedido,
        "15": sistema.actualizar_historial_compras,
        "16": sistema.eliminar_cliente,
        "17": sistema.eliminar_producto,
        "18": sistema.eliminar_pedido,
    }

    while True:
        mostrar_menu()
        opcion = input("\nSelecciona una opción de la lista: ").strip()

        if opcion == "0":
            print("\n👋 ¡Excelente trabajo programando hoy! ¡Hasta luego!\n")
            break
        elif opcion in opciones:
            try:
                opciones[opcion]()
            except Exception as e:
                print(f"\n❌ Se produjo un error interno inesperado: {e}")
        else:
            print("\n⚠️  Opción no válida. Por favor digite un número del 0 al 18.")

if __name__ == "__main__":
    main()
