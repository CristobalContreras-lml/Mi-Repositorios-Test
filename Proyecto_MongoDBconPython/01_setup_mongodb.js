// ============================================================
// PROYECTO MONGODB - SISTEMA DE VENTAS E-COMMERCE
// Creación de BD, Colecciones e Inserción
// ============================================================
// Cómo ejecutar: mongosh < 01_setup_mongodb.js
// ============================================================

// 1. Seleccionar/Crear la base de datos
use("tienda_ecommerce");

// 2. Eliminar colecciones si existen (para reiniciar limpio)
db.clientes.drop();
db.productos.drop();
db.pedidos.drop();

print("=== BASE DE DATOS: tienda_ecommerce ===");
print("Colecciones anteriores eliminadas.\n");

// ============================================================
// INSERCIÓN DE CLIENTES (mínimo 10)
// Usa subdocumento para 'direccion'
// ============================================================
db.clientes.insertMany([
  {
    id_cliente: "CLI001",
    nombre: "Ana González",
    email: "ana.gonzalez@email.com",
    telefono: "+56912345678",
    direccion: {                          // <-- SUBDOCUMENTO
      calle: "Av. Providencia 1234",
      ciudad: "Santiago",
      region: "Metropolitana",
    },
    fecha_registro: new Date("2023-01-15"),
    historial_compras: []
  },
  {
    id_cliente: "CLI002",
    nombre: "Carlos Martínez",
    email: "carlos.martinez@email.com",
    telefono: "+56987654321",
    direccion: {
      calle: "Calle Larga 567",
      ciudad: "Valparaíso",
      region: "Valparaíso",
    },
    fecha_registro: new Date("2023-03-20"),
    historial_compras: []
  },
  {
    id_cliente: "CLI003",
    nombre: "María López",
    email: "maria.lopez@email.com",
    telefono: "+56911223344",
    direccion: {
      calle: "Los Aromos 890",
      ciudad: "Concepción",
      region: "Biobío",
    },
    fecha_registro: new Date("2023-05-10"),
    historial_compras: []
  },
  {
    id_cliente: "CLI004",
    nombre: "Pedro Soto",
    email: "pedro.soto@email.com",
    telefono: "+56955443322",
    direccion: {
      calle: "Pasaje Norte 23",
      ciudad: "Temuco",
      region: "Araucanía",
    },
    fecha_registro: new Date("2023-06-01"),
    historial_compras: []
  },
  {
    id_cliente: "CLI005",
    nombre: "Valentina Rojas",
    email: "valentina.rojas@email.com",
    telefono: "+56966778899",
    direccion: {
      calle: "Av. Brasil 456",
      ciudad: "Santiago",
      region: "Metropolitana",
    },
    fecha_registro: new Date("2023-07-14"),
    historial_compras: []
  },
  {
    id_cliente: "CLI006",
    nombre: "Andrés Díaz",
    email: "andres.diaz@email.com",
    telefono: "+56933221100",
    direccion: {
      calle: "Las Hortensias 789",
      ciudad: "La Serena",
      region: "Coquimbo",
    },
    fecha_registro: new Date("2023-08-22"),
    historial_compras: []
  },
  {
    id_cliente: "CLI007",
    nombre: "Francisca Muñoz",
    email: "francisca.munoz@email.com",
    telefono: "+56944556677",
    direccion: {
      calle: "Calle del Río 101",
      ciudad: "Puerto Montt",
      region: "Los Lagos",
    },
    fecha_registro: new Date("2023-09-05"),
    historial_compras: []
  },
  {
    id_cliente: "CLI008",
    nombre: "Roberto Herrera",
    email: "roberto.herrera@email.com",
    telefono: "+56922334455",
    direccion: {
      calle: "Av. del Mar 234",
      ciudad: "Viña del Mar",
      region: "Valparaíso",
    },
    fecha_registro: new Date("2023-10-18"),
    historial_compras: []
  },
  {
    id_cliente: "CLI009",
    nombre: "Javiera Castillo",
    email: "javiera.castillo@email.com",
    telefono: "+56977889900",
    direccion: {
      calle: "Portales 678",
      ciudad: "Rancagua",
      region: "O'Higgins",
    },
    fecha_registro: new Date("2023-11-30"),
    historial_compras: []
  },
  {
    id_cliente: "CLI010",
    nombre: "Diego Torres",
    email: "diego.torres@email.com",
    telefono: "+56911223355",
    direccion: {
      calle: "Las Encinas 999",
      ciudad: "Antofagasta",
      region: "Antofagasta",
    },
    fecha_registro: new Date("2024-01-08"),
    historial_compras: []
  }
]);

print("✅ 10 clientes insertados.");

// ============================================================
// INSERCIÓN DE PRODUCTOS (mínimo 10)
// Usa subdocumento 'atributos' para información variable
// ============================================================
db.productos.insertMany([
  {
    id_producto: "PROD001",
    nombre: "Polera Deportiva Nike",
    categoria: "Ropa",
    precio: 25990,
    stock: 50,
    atributos: { talla: "M", color: "Azul", marca: "Nike", material: "Poliéster" }
  },
  {
    id_producto: "PROD002",
    nombre: "Laptop HP Pavilion 15",
    categoria: "Electrónica",
    precio: 549990,
    stock: 12,
    atributos: { marca: "HP", ram: "8GB", almacenamiento: "512GB SSD", procesador: "Intel i5" }
  },
  {
    id_producto: "PROD003",
    nombre: "Zapatillas Adidas Running",
    categoria: "Calzado",
    precio: 79990,
    stock: 35,
    atributos: { talla: "42", color: "Negro/Blanco", marca: "Adidas", tipo: "Running" }
  },
  {
    id_producto: "PROD004",
    nombre: "Smartphone Samsung Galaxy A54",
    categoria: "Electrónica",
    precio: 399990,
    stock: 20,
    atributos: { marca: "Samsung", ram: "6GB", almacenamiento: "128GB", color: "Blanco" }
  },
  {
    id_producto: "PROD005",
    nombre: "Sillón Gamer RGB",
    categoria: "Muebles",
    precio: 189990,
    stock: 8,
    atributos: { color: "Negro/Rojo", material: "Cuero sintético", peso_max: "120kg" }
  },
  {
    id_producto: "PROD006",
    nombre: "Auriculares Sony WH-1000XM5",
    categoria: "Electrónica",
    precio: 299990,
    stock: 15,
    atributos: { marca: "Sony", tipo: "Over-Ear", cancelacion_ruido: true, bateria: "30h" }
  },
  {
    id_producto: "PROD007",
    nombre: "Mochila Outdoor The North Face",
    categoria: "Accesorios",
    precio: 89990,
    stock: 25,
    atributos: { capacidad: "30L", color: "Verde", material: "Nylon", resistente_agua: true }
  },
  {
    id_producto: "PROD008",
    nombre: "Pantalón Jeans Levi's 501",
    categoria: "Ropa",
    precio: 49990,
    stock: 40,
    atributos: { talla: "32x30", color: "Azul Oscuro", marca: "Levi's", corte: "Recto" }
  },
  {
    id_producto: "PROD009",
    nombre: "Cafetera Nespresso Vertuo",
    categoria: "Electrodomésticos",
    precio: 129990,
    stock: 18,
    atributos: { marca: "Nespresso", capacidad: "1.1L", color: "Negro", tipo: "Cápsulas" }
  },
  {
    id_producto: "PROD010",
    nombre: "Monitor LG 27 pulgadas 4K",
    categoria: "Electrónica",
    precio: 349990,
    stock: 10,
    atributos: { marca: "LG", resolucion: "4K UHD", tamano: "27 pulgadas", panel: "IPS" }
  }
]);

print("✅ 10 productos insertados.");

// ============================================================
// INSERCIÓN DE PEDIDOS (mínimo 20)
// Usa cliente embebido + arreglo de subdocumentos en detalle_pedido
// ============================================================
db.pedidos.insertMany([
  {
    id_pedido: "PED001",
    fecha: new Date("2024-01-10"),
    estado: "entregado",
    cliente: { id_cliente: "CLI001", nombre: "Ana González", email: "ana.gonzalez@email.com" },
    detalle_pedido: [                         // <-- ARREGLO DE SUBDOCUMENTOS
      { producto: "PROD001", nombre: "Polera Deportiva Nike", cantidad: 2, precio_unitario: 25990 },
      { producto: "PROD007", nombre: "Mochila Outdoor The North Face", cantidad: 1, precio_unitario: 89990 }
    ],
    total: 141970
  },
  {
    id_pedido: "PED002",
    fecha: new Date("2024-01-15"),
    estado: "entregado",
    cliente: { id_cliente: "CLI002", nombre: "Carlos Martínez", email: "carlos.martinez@email.com" },
    detalle_pedido: [
      { producto: "PROD002", nombre: "Laptop HP Pavilion 15", cantidad: 1, precio_unitario: 549990 }
    ],
    total: 549990
  },
  {
    id_pedido: "PED003",
    fecha: new Date("2024-02-03"),
    estado: "entregado",
    cliente: { id_cliente: "CLI003", nombre: "María López", email: "maria.lopez@email.com" },
    detalle_pedido: [
      { producto: "PROD003", nombre: "Zapatillas Adidas Running", cantidad: 1, precio_unitario: 79990 },
      { producto: "PROD008", nombre: "Pantalón Jeans Levi's 501", cantidad: 2, precio_unitario: 49990 }
    ],
    total: 179970
  },
  {
    id_pedido: "PED004",
    fecha: new Date("2024-02-14"),
    estado: "enviado",
    cliente: { id_cliente: "CLI004", nombre: "Pedro Soto", email: "pedro.soto@email.com" },
    detalle_pedido: [
      { producto: "PROD004", nombre: "Smartphone Samsung Galaxy A54", cantidad: 1, precio_unitario: 399990 },
      { producto: "PROD006", nombre: "Auriculares Sony WH-1000XM5", cantidad: 1, precio_unitario: 299990 }
    ],
    total: 699980
  },
  {
    id_pedido: "PED005",
    fecha: new Date("2024-03-01"),
    estado: "entregado",
    cliente: { id_cliente: "CLI005", nombre: "Valentina Rojas", email: "valentina.rojas@email.com" },
    detalle_pedido: [
      { producto: "PROD005", nombre: "Sillón Gamer RGB", cantidad: 1, precio_unitario: 189990 }
    ],
    total: 189990
  },
  {
    id_pedido: "PED006",
    fecha: new Date("2024-03-15"),
    estado: "entregado",
    cliente: { id_cliente: "CLI001", nombre: "Ana González", email: "ana.gonzalez@email.com" },
    detalle_pedido: [
      { producto: "PROD009", nombre: "Cafetera Nespresso Vertuo", cantidad: 1, precio_unitario: 129990 }
    ],
    total: 129990
  },
  {
    id_pedido: "PED007",
    fecha: new Date("2024-04-02"),
    estado: "procesando",
    cliente: { id_cliente: "CLI006", nombre: "Andrés Díaz", email: "andres.diaz@email.com" },
    detalle_pedido: [
      { producto: "PROD010", nombre: "Monitor LG 27 pulgadas 4K", cantidad: 1, precio_unitario: 349990 },
      { producto: "PROD002", nombre: "Laptop HP Pavilion 15", cantidad: 1, precio_unitario: 549990 }
    ],
    total: 899980
  },
  {
    id_pedido: "PED008",
    fecha: new Date("2024-04-10"),
    estado: "entregado",
    cliente: { id_cliente: "CLI007", nombre: "Francisca Muñoz", email: "francisca.munoz@email.com" },
    detalle_pedido: [
      { producto: "PROD001", nombre: "Polera Deportiva Nike", cantidad: 3, precio_unitario: 25990 },
      { producto: "PROD003", nombre: "Zapatillas Adidas Running", cantidad: 1, precio_unitario: 79990 }
    ],
    total: 157960
  },
  {
    id_pedido: "PED009",
    fecha: new Date("2024-05-05"),
    estado: "entregado",
    cliente: { id_cliente: "CLI008", nombre: "Roberto Herrera", email: "roberto.herrera@email.com" },
    detalle_pedido: [
      { producto: "PROD006", nombre: "Auriculares Sony WH-1000XM5", cantidad: 1, precio_unitario: 299990 }
    ],
    total: 299990
  },
  {
    id_pedido: "PED010",
    fecha: new Date("2024-05-20"),
    estado: "enviado",
    cliente: { id_cliente: "CLI009", nombre: "Javiera Castillo", email: "javiera.castillo@email.com" },
    detalle_pedido: [
      { producto: "PROD007", nombre: "Mochila Outdoor The North Face", cantidad: 2, precio_unitario: 89990 },
      { producto: "PROD008", nombre: "Pantalón Jeans Levi's 501", cantidad: 1, precio_unitario: 49990 }
    ],
    total: 229970
  },
  {
    id_pedido: "PED011",
    fecha: new Date("2024-06-01"),
    estado: "entregado",
    cliente: { id_cliente: "CLI010", nombre: "Diego Torres", email: "diego.torres@email.com" },
    detalle_pedido: [
      { producto: "PROD004", nombre: "Smartphone Samsung Galaxy A54", cantidad: 1, precio_unitario: 399990 }
    ],
    total: 399990
  },
  {
    id_pedido: "PED012",
    fecha: new Date("2024-06-18"),
    estado: "entregado",
    cliente: { id_cliente: "CLI002", nombre: "Carlos Martínez", email: "carlos.martinez@email.com" },
    detalle_pedido: [
      { producto: "PROD009", nombre: "Cafetera Nespresso Vertuo", cantidad: 1, precio_unitario: 129990 },
      { producto: "PROD005", nombre: "Sillón Gamer RGB", cantidad: 1, precio_unitario: 189990 }
    ],
    total: 319980
  },
  {
    id_pedido: "PED013",
    fecha: new Date("2024-07-04"),
    estado: "cancelado",
    cliente: { id_cliente: "CLI003", nombre: "María López", email: "maria.lopez@email.com" },
    detalle_pedido: [
      { producto: "PROD010", nombre: "Monitor LG 27 pulgadas 4K", cantidad: 1, precio_unitario: 349990 }
    ],
    total: 349990
  },
  {
    id_pedido: "PED014",
    fecha: new Date("2024-07-22"),
    estado: "entregado",
    cliente: { id_cliente: "CLI004", nombre: "Pedro Soto", email: "pedro.soto@email.com" },
    detalle_pedido: [
      { producto: "PROD001", nombre: "Polera Deportiva Nike", cantidad: 1, precio_unitario: 25990 },
      { producto: "PROD003", nombre: "Zapatillas Adidas Running", cantidad: 1, precio_unitario: 79990 },
      { producto: "PROD008", nombre: "Pantalón Jeans Levi's 501", cantidad: 1, precio_unitario: 49990 }
    ],
    total: 155970
  },
  {
    id_pedido: "PED015",
    fecha: new Date("2024-08-10"),
    estado: "enviado",
    cliente: { id_cliente: "CLI005", nombre: "Valentina Rojas", email: "valentina.rojas@email.com" },
    detalle_pedido: [
      { producto: "PROD002", nombre: "Laptop HP Pavilion 15", cantidad: 1, precio_unitario: 549990 }
    ],
    total: 549990
  },
  {
    id_pedido: "PED016",
    fecha: new Date("2024-08-25"),
    estado: "entregado",
    cliente: { id_cliente: "CLI006", nombre: "Andrés Díaz", email: "andres.diaz@email.com" },
    detalle_pedido: [
      { producto: "PROD007", nombre: "Mochila Outdoor The North Face", cantidad: 1, precio_unitario: 89990 }
    ],
    total: 89990
  },
  {
    id_pedido: "PED017",
    fecha: new Date("2024-09-05"),
    estado: "procesando",
    cliente: { id_cliente: "CLI007", nombre: "Francisca Muñoz", email: "francisca.munoz@email.com" },
    detalle_pedido: [
      { producto: "PROD006", nombre: "Auriculares Sony WH-1000XM5", cantidad: 2, precio_unitario: 299990 }
    ],
    total: 599980
  },
  {
    id_pedido: "PED018",
    fecha: new Date("2024-09-18"),
    estado: "entregado",
    cliente: { id_cliente: "CLI008", nombre: "Roberto Herrera", email: "roberto.herrera@email.com" },
    detalle_pedido: [
      { producto: "PROD004", nombre: "Smartphone Samsung Galaxy A54", cantidad: 1, precio_unitario: 399990 },
      { producto: "PROD007", nombre: "Mochila Outdoor The North Face", cantidad: 1, precio_unitario: 89990 }
    ],
    total: 489980
  },
  {
    id_pedido: "PED019",
    fecha: new Date("2024-10-01"),
    estado: "entregado",
    cliente: { id_cliente: "CLI009", nombre: "Javiera Castillo", email: "javiera.castillo@email.com" },
    detalle_pedido: [
      { producto: "PROD005", nombre: "Sillón Gamer RGB", cantidad: 1, precio_unitario: 189990 },
      { producto: "PROD010", nombre: "Monitor LG 27 pulgadas 4K", cantidad: 1, precio_unitario: 349990 }
    ],
    total: 539980
  },
  {
    id_pedido: "PED020",
    fecha: new Date("2024-10-15"),
    estado: "enviado",
    cliente: { id_cliente: "CLI010", nombre: "Diego Torres", email: "diego.torres@email.com" },
    detalle_pedido: [
      { producto: "PROD001", nombre: "Polera Deportiva Nike", cantidad: 2, precio_unitario: 25990 },
      { producto: "PROD009", nombre: "Cafetera Nespresso Vertuo", cantidad: 1, precio_unitario: 129990 }
    ],
    total: 181970
  }
]);

print("✅ 20 pedidos insertados.");
print("\n=== RESUMEN ===");
print("Clientes: " + db.clientes.countDocuments());
print("Productos: " + db.productos.countDocuments());
print("Pedidos:   " + db.pedidos.countDocuments());
print("\n¡Base de datos lista! 🎉");
