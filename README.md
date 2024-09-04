
---

# Sistema de Inventario

Este proyecto es un sistema de gestión de inventarios desarrollado en Python, utilizando **SQLAlchemy** para manejar la base de datos SQLite. El sistema permite gestionar productos, proveedores, clientes, ventas y productos seleccionados, ofreciendo funciones CRUD para todas estas entidades.

## Actualizaciones Recientes

### PDF generados y abiertos automáticamente:
![Vista de PDF generados](https://github.com/user-attachments/assets/8c0a723d-e840-46f8-b61f-3f3dff43dd6e)

### Vistas del inventario, ventas, clientes, etc.:
![Vista del inventario](https://github.com/user-attachments/assets/9593b6cb-b6e1-4c73-b99e-9b6a03ba45d8)
![Vista de ventas](https://github.com/user-attachments/assets/5cbc7f49-f8dc-4053-ae6e-fe897cb4366b)

### Gráficos automáticos de la base de datos:
![Vista de gráficos](https://github.com/user-attachments/assets/7e3b7e38-353c-4269-a09a-a03783cc3878)

### Cambios en el estilo general:
![Nuevo estilo de la interfaz](https://github.com/user-attachments/assets/a71aabef-4795-435e-91cd-e4e503973561)

---

## Modelo de Base de Datos

### 1. **Cliente**
   - Representa a los clientes.
   - **Atributos**:
     - `id`: Identificador único.
     - `nombre`, `apellido`: Nombre y apellido.
     - `cedula`: Documento de identidad.
     - `correo`: Correo electrónico.
     - `telefono`, `direccion`, `notas_adicionales`: Información de contacto.

### 2. **Venta**
   - Información de las ventas realizadas.
   - **Atributos**:
     - `id`: Identificador único.
     - `fecha_venta`: Fecha de la venta.
     - `realizada_por`: Usuario que realizó la venta.
     - `cliente_id`: Identificador del cliente.
     - `porcentaje_iva`, `metodo_pago`, `metodo_envio`, `total_venta`: Detalles de la venta.
     - `productos`: Productos vendidos.

### 3. **Producto**
   - Representa los productos en el inventario.
   - **Atributos**:
     - `id`, `nombre`, `codigo`: Identificación y nombre.
     - `descripcion`, `categoria`, `marca`: Detalles del producto.
     - `precio_compra`, `precio_venta`, `precio_mayorista`: Precios del producto.
     - `cantidad_unidades`: Stock disponible.
     - `temporada_producto`, `fecha_adquisicion`, `fecha_vencimiento`: Fechas relevantes.
     - `fragilidad`, `tipo_producto`: Clasificación del producto.
     - `proveedor_id`: Relación con el proveedor.

### 4. **ProductoVendido**
   - Almacena productos vendidos.
   - **Atributos**:
     - `id`, `producto_id`: Identificadores.
     - `cantidad`, `precio_venta_unitario`: Detalles de la venta.

### 5. **Proveedor**
   - Información de los proveedores.
   - **Atributos**:
     - `id`, `nombre_contacto`, `nombre_empresa`: Información de contacto.
     - `numero_proveedor`, `correo_proveedor`, `nit_empresa`: Información fiscal.
     - `pagina_web`, `direccion_empresa`, `notas_adicionales`: Detalles adicionales.

### 6. **ProductoSeleccionado**
   - Productos seleccionados para una venta.
   - **Atributos**:
     - `id`, `producto_id`: Identificadores.
     - `cantidad_unidades`, `tipo_precio`, `precio_venta`, `nombre`, `codigo`, `descuento`: Detalles del producto seleccionado.

---

## Funciones CRUD

Todas las operaciones están decoradas con `manejar_excepcion_sqlalchemy` para manejar errores y realizar un rollback en caso de fallos.

1. **agregar_producto**: Añade un nuevo producto.
2. **agregar_proveedor**: Registra un proveedor.
3. **agregar_cliente**: Añade un nuevo cliente.
4. **agregar_producto_seleccionado**: Registra un producto para una venta.
5. **agregar_venta**: Registra una venta completa.
6. **eliminar_producto_por_id**: Elimina un producto por su ID.
7. **agregar_producto_vendido**: Registra un producto vendido.

---

## Uso

1. Para crear la base de datos, ejecuta el archivo principal:

    ```bash
    python nombre_del_archivo.py
    ```

2. Las funciones CRUD se pueden ejecutar de la siguiente forma:

    ```python
    agregar_producto("Laptop", 12345, "Laptop de alta gama", "Electrónica", "Dell", 1000, 1500, 1400, 50, "Primavera", datetime.now(), None, "Frágil", "Electrónico", 1, "Disponible")
    ```

---

## Requisitos

- **Python 3.x**
- **Tkinter** (para la interfaz gráfica)
- **SQLAlchemy** (para la gestión de la base de datos)

## Instalación

1. Clona el repositorio.
2. Instala las dependencias:

    ```bash
    pip install -r requirements.txt
    ```

3. Ejecuta la aplicación:

    ```bash
    python nombre_del_archivo.py
    ```

---

## Ejemplos de Bases de Datos en SQLite con SQLAlchemy:

![Vista de bases de datos](https://github.com/user-attachments/assets/a499c55b-6a2d-4868-bbe3-1f6ede0d0cd2)
![Ejemplo de bases de datos](https://github.com/user-attachments/assets/08576857-aff8-4718-bb7c-ddb87da5a2f6)

---

## API de Facturación:

![Vista de la API de facturación](https://github.com/user-attachments/assets/05b0239e-d7cd-4488-9d38-3d80eb615a64)

![Interfaz de la API](https://github.com/user-attachments/assets/5bafdd49-2ca3-4cd4-ba78-f1a8572afa50)
![Vista adicional de la API](https://github.com/user-attachments/assets/6c652b5a-6d39-48d9-816a-b8788b2f000f)

---

