// ============================================================
// PROYECTO MONGODB - SISTEMA DE VENTAS E-COMMERCE
// CRUD Completo + Consultas Avanzadas
// ============================================================
// Cómo ejecutar: mongosh < 02_consultas_mongodb.js
// ============================================================

use("tienda_ecommerce");

print("\n========================================");
print("  CRUD Y CONSULTAS - SISTEMA E-COMMERCE");
print("========================================\n");

// ============================================================
// SECCIÓN 1: CREATE (Insertar)
// ============================================================

// ── 3 clientes ───────────────────────────────────────────────
print("--- [CREATE] Insertar 3 clientes ---");
db.clientes.insertOne({
  id_cliente: "CLI011",
  nombre: "Sofía Vargas",
  email: "sofia.vargas@email.com",
  telefono: "+56944112233",
  direccion: {
    calle: "Av. Libertad 500",
    ciudad: "Iquique",
    region: "Tarapacá"
  },
  fecha_registro: new Date(),
  historial_compras: []
});

db.clientes.insertOne({
  id_cliente: "CLI012",
  nombre: "Tomás Fuentes",
  email: "tomas.fuentes@email.com",
  telefono: "+56955667788",
  direccion: {
    calle: "Los Pinos 321",
    ciudad: "Arica",
    region: "Arica y Parinacota"
  },
  fecha_registro: new Date(),
  historial_compras: []
});

db.clientes.insertOne({
  id_cliente: "CLI013",
  nombre: "Camila Reyes",
  email: "camila.reyes@email.com",
  telefono: "+56966778899",
  direccion: {
    calle: "Calle Nueva 789",
    ciudad: "Valdivia",
    region: "Los Ríos"
  },
  fecha_registro: new Date(),
  historial_compras: []
});
print("✅ 3 clientes insertados. Total: " + db.clientes.countDocuments() + "\n");


// ── 3 productos ───────────────────────────────────────────────
print("--- [CREATE] Insertar 3 productos ---");
db.productos.insertOne({
  id_producto: "PROD011",
  nombre: "Teclado Mecánico Logitech G Pro",
  categoria: "Electrónica",
  precio: 149990,
  stock: 22,
  atributos: { marca: "Logitech", tipo: "Mecánico", switches: "Red", retroiluminacion: "RGB" }
});

db.productos.insertOne({
  id_producto: "PROD012",
  nombre: "Mouse Inalámbrico Razer DeathAdder",
  categoria: "Electrónica",
  precio: 79990,
  stock: 30,
  atributos: { marca: "Razer", tipo: "Inalámbrico", dpi: "20000", bateria: "70h" }
});

db.productos.insertOne({
  id_producto: "PROD013",
  nombre: "Polera Oversize Negra",
  categoria: "Ropa",
  precio: 19990,
  stock: 60,
  atributos: { talla: "L", color: "Negro", material: "Algodón" }
});
print("✅ 3 productos insertados. Total: " + db.productos.countDocuments() + "\n");


// ── 3 pedidos ─────────────────────────────────────────────────
print("--- [CREATE] Insertar 3 pedidos ---");
db.pedidos.insertMany([
  {
    id_pedido: "PED021",
    fecha: new Date("2024-11-05"),
    estado: "procesando",
    cliente: {
      id_cliente: "CLI011",
      nombre: "Sofía Vargas",
      email: "sofia.vargas@email.com"
    },
    detalle_pedido: [
      { producto: "PROD011", nombre: "Teclado Mecánico Logitech G Pro", cantidad: 1, precio_unitario: 149990 },
      { producto: "PROD012", nombre: "Mouse Inalámbrico Razer DeathAdder", cantidad: 1, precio_unitario: 79990 }
    ],
    total: 229980
  },
  {
    id_pedido: "PED022",
    fecha: new Date("2024-11-10"),
    estado: "entregado",
    cliente: {
      id_cliente: "CLI012",
      nombre: "Tomás Fuentes",
      email: "tomas.fuentes@email.com"
    },
    detalle_pedido: [
      { producto: "PROD013", nombre: "Polera Oversize Negra", cantidad: 2, precio_unitario: 19990 }
    ],
    total: 39980
  },
  {
    id_pedido: "PED023",
    fecha: new Date("2024-11-15"),
    estado: "en recorrido",
    cliente: {
      id_cliente: "CLI013",
      nombre: "Camila Reyes",
      email: "camila.reyes@email.com"
    },
    detalle_pedido: [
      { producto: "PROD011", nombre: "Teclado Mecánico Logitech G Pro", cantidad: 1, precio_unitario: 149990 },
      { producto: "PROD013", nombre: "Polera Oversize Negra", cantidad: 3, precio_unitario: 19990 }
    ],
    total: 209960
  }
]);
print("✅ 3 pedidos insertados. Total: " + db.pedidos.countDocuments() + "\n");

// ============================================================
// SECCIÓN 2: READ (Consultar)
// ============================================================

// --- Búsqueda por filtros de rango de fecha ---
print("--- [READ] Pedidos entre Feb y Jun 2024 ---");
let pedidosFecha = db.pedidos.find({
  fecha: {
    $gte: new Date("2024-02-01"),
    $lte: new Date("2024-06-30")
  }
}, { id_pedido: 1, fecha: 1, "cliente.nombre": 1, total: 1, _id: 0 });
pedidosFecha.forEach(p => print(JSON.stringify(p)));
print("");

// --- Búsqueda por rango de precio ---
print("--- [READ] Productos entre $50.000 y $300.000 ---");
let productosPrecio = db.productos.find(
  { precio: { $gte: 50000, $lte: 300000 } },
  { nombre: 1, precio: 1, categoria: 1, _id: 0 }
);
productosPrecio.forEach(p => print(JSON.stringify(p)));
print("");

// --- Búsqueda en arreglos: pedidos que contienen PROD001 ---
print("--- [READ] Pedidos que contienen PROD001 (Polera Nike) ---");
let pedidosConProd = db.pedidos.find(
  { "detalle_pedido.producto": "PROD001" },
  { id_pedido: 1, "cliente.nombre": 1, fecha: 1, _id: 0 }
);
pedidosConProd.forEach(p => print(JSON.stringify(p)));
print("");

// --- Uso de $ne (not equal) ---
print("--- [READ] Pedidos que NO están en estado 'cancelado' ($ne) ---");
let pedidosNoCancel = db.pedidos.find(
  { estado: { $ne: "cancelado" } },
  { id_pedido: 1, estado: 1, _id: 0 }
);
pedidosNoCancel.forEach(p => print(JSON.stringify(p)));
print("");

// --- Uso de $gt y $lt ---
print("--- [READ] Pedidos con total mayor a $400.000 ($gt) ---");
let pedidosCaros = db.pedidos.find(
  { total: { $gt: 400000 } },
  { id_pedido: 1, total: 1, "cliente.nombre": 1, _id: 0 }
);
pedidosCaros.forEach(p => print(JSON.stringify(p)));
print("");

// --- Uso de $in ---
print("--- [READ] Productos de categoría Electrónica o Ropa ($in) ---");
let productosCat = db.productos.find(
  { categoria: { $in: ["Electrónica", "Ropa"] } },
  { nombre: 1, categoria: 1, precio: 1, _id: 0 }
);
productosCat.forEach(p => print(JSON.stringify(p)));
print("");

// --- Uso de $and ---
print("--- [READ] Productos Electrónica con precio < $400.000 ($and) ---");
let productosAnd = db.productos.find({
  $and: [
    { categoria: "Electrónica" },
    { precio: { $lt: 400000 } }
  ]
}, { nombre: 1, categoria: 1, precio: 1, _id: 0 });
productosAnd.forEach(p => print(JSON.stringify(p)));
print("");

// --- Uso de $or ---
print("--- [READ] Clientes de Santiago o Valparaíso ($or) ---");
let clientesOr = db.clientes.find({
  $or: [
    { "direccion.ciudad": "Santiago" },
    { "direccion.ciudad": "Valparaíso" }
  ]
}, { nombre: 1, "direccion.ciudad": 1, _id: 0 });
clientesOr.forEach(c => print(JSON.stringify(c)));
print("");

// --- Expresiones regulares: búsqueda por nombre parcial ---
print("--- [READ] Clientes cuyo nombre contiene 'Mar' (regex) ---");
let clientesRegex = db.clientes.find(
  { nombre: { $regex: "Mar", $options: "i" } },  // "i" = case insensitive
  { nombre: 1, email: 1, _id: 0 }
);
clientesRegex.forEach(c => print(JSON.stringify(c)));
print("");

// --- Uso de $gte en stock ---
print("--- [READ] Productos con stock >= 20 ($gte) ---");
let productosStock = db.productos.find(
  { stock: { $gte: 20 } },
  { nombre: 1, stock: 1, _id: 0 }
);
productosStock.forEach(p => print(JSON.stringify(p)));
print("");

// ============================================================
// SECCIÓN 3: UPDATE (Actualizar)
// ============================================================

// --- Actualizar dato simple ---
print("--- [UPDATE] Actualizar email de CLI001 ---");
db.clientes.updateOne(
  { id_cliente: "CLI001" },
  { $set: { email: "ana.gonzalez.nuevo@email.com", telefono: "+56999888777" } }
);
print("✅ Email actualizado.");
print(JSON.stringify(db.clientes.findOne({ id_cliente: "CLI001" }, { nombre: 1, email: 1, _id: 0 })));
print("");

// --- Actualizar precio de producto ---
print("--- [UPDATE] Actualizar precio de PROD001 (Polera Nike) ---");
db.productos.updateOne(
  { id_producto: "PROD001" },
  { $set: { precio: 27990 } }
);
print("✅ Precio actualizado.");
print(JSON.stringify(db.productos.findOne({ id_producto: "PROD001" }, { nombre: 1, precio: 1, _id: 0 })));
print("");

// --- Actualizar elemento en arreglo: cambiar cantidad de un item en pedido ---
print("--- [UPDATE] Cambiar cantidad de PROD001 en PED001 (de 2 a 3) ---");
db.pedidos.updateOne(
  { id_pedido: "PED001", "detalle_pedido.producto": "PROD001" },
  { $set: { "detalle_pedido.$.cantidad": 3 } }
);
print("✅ Cantidad actualizada en el pedido.");
let pedidoActualizado = db.pedidos.findOne({ id_pedido: "PED001" }, { detalle_pedido: 1, _id: 0 });
print(JSON.stringify(pedidoActualizado));
print("");

// --- Actualizar stock con $inc ---
print("--- [UPDATE] Reducir stock de PROD002 en 1 ($inc) ---");
db.productos.updateOne(
  { id_producto: "PROD002" },
  { $inc: { stock: -1 } }
);
print("✅ Stock reducido.");
print(JSON.stringify(db.productos.findOne({ id_producto: "PROD002" }, { nombre: 1, stock: 1, _id: 0 })));
print("");

// ============================================================
// SECCIÓN 4: DELETE (Eliminar)
// ============================================================

print("--- [DELETE] Eliminar los 3 clientes insertados ---");
let delCli = db.clientes.deleteMany({ id_cliente: { $in: ["CLI011", "CLI012", "CLI013"] } });
print("✅ Clientes eliminados: " + delCli.deletedCount + "\n");

print("--- [DELETE] Eliminar los 3 productos insertados ---");
let delProd = db.productos.deleteMany({ id_producto: { $in: ["PROD011", "PROD012", "PROD013"] } });
print("✅ Productos eliminados: " + delProd.deletedCount + "\n");

print("--- [DELETE] Eliminar los 3 pedidos insertados ---");
let delPed = db.pedidos.deleteMany({ id_pedido: { $in: ["PED021", "PED022", "PED023"] } });
print("✅ Pedidos eliminados: " + delPed.deletedCount + "\n");

// ============================================================
// RESUMEN FINAL
// ============================================================
print("========================================");
print("  RESUMEN FINAL DE COLECCIONES");
print("========================================");
print("Clientes: " + db.clientes.countDocuments());
print("Productos: " + db.productos.countDocuments());
print("Pedidos:   " + db.pedidos.countDocuments());
print("\n¡Script completado exitosamente! ✅");
