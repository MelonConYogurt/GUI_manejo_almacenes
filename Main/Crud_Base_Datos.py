from Main.BaseDeDatosInventario import Producto, Proveedor, Cliente, Venta, ProductoVendido, session, ProductoSelecionado
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

def manejar_excepcion_sqlalchemy(func):
    def manejo_erorres(*args, **kwargs):
        try:
            resultado = func(*args, **kwargs)
            session.commit()
            return resultado
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Ha ocurrido un error: {e} ") 
    return manejo_erorres

@manejar_excepcion_sqlalchemy
def agregar_producto(nombre, codigo, descripcion, categoria, marca, precio_compra,
                     precio_venta, precio_mayorista, cantidad_unidades, temporada_producto, 
                     fecha_adquisicion, fecha_vencimiento, fragilidad, tipo_producto, proveedor_id, estado):
    producto_nuevo = Producto(
        nombre=nombre,
        codigo=codigo,
        descripcion=descripcion,
        categoria=categoria,
        marca=marca,
        precio_compra=precio_compra,
        precio_venta=precio_venta,
        precio_mayorista=precio_mayorista,
        cantidad_unidades=cantidad_unidades,
        temporada_producto=temporada_producto,
        fecha_adquisicion=fecha_adquisicion,
        fecha_vencimiento=fecha_vencimiento,
        fragilidad=fragilidad,
        tipo_producto=tipo_producto,
        proveedor_id=proveedor_id,
        estado=estado
    )
    session.add(producto_nuevo)

@manejar_excepcion_sqlalchemy
def agregar_proveedor(nombre_contacto, nombre_empresa, numero_proveedor, 
                      correo_proveedor, nit_empresa, pagina_web, direccion_empresa,
                      notas_adicionales):
    proveedor = Proveedor(
        nombre_contacto=nombre_contacto,
        nombre_empresa=nombre_empresa,
        numero_proveedor=numero_proveedor,
        correo_proveedor=correo_proveedor,
        nit_empresa=nit_empresa,
        pagina_web=pagina_web,
        direccion_empresa=direccion_empresa,
        notas_adicionales=notas_adicionales
    )
    session.add(proveedor)

@manejar_excepcion_sqlalchemy
def agregar_cliente(nombre, apellido, cedula, correo, telefono, direccion, notas_adicionales):
    nuevo_cliente = Cliente(
        nombre=nombre,
        apellido=apellido,
        cedula=cedula,
        correo=correo,
        telefono=telefono, 
        direccion=direccion,
        notas_adicionales=notas_adicionales
    )
    session.add(nuevo_cliente)

@manejar_excepcion_sqlalchemy
def agregar_producto_seleccionado(producto_id, cantidad_unidades, tipo_precio, precio_venta, nombre, codigo, descuento):
    nueva_producto_seleccionado = ProductoSelecionado(
        producto_id=producto_id,
        cantidad_unidades=cantidad_unidades,
        tipo_precio=tipo_precio,
        precio_venta=precio_venta,
        nombre=nombre,
        codigo=codigo,
        descuento=descuento
    )
    session.add(nueva_producto_seleccionado)

@manejar_excepcion_sqlalchemy
def agregar_venta(cliente_id, realizada_por, metodo_pago ,metodo_envio ,total_venta, porcentaje_iva ,productos_vendidos):
    nueva_venta = Venta(
        cliente_id=cliente_id,
        realizada_por=realizada_por,
        metodo_pago=metodo_pago,
        metodo_envio=metodo_envio,
        total_venta=total_venta,
        porcentaje_iva=porcentaje_iva,
        total_productos=len(productos_vendidos),
        productos=(productos_vendidos)  
    )
    session.add(nueva_venta)

@manejar_excepcion_sqlalchemy
def eliminar_producto_por_id(id_producto):
    producto = session.query(ProductoSelecionado).filter_by(producto_id=id_producto).one()
    session.delete(producto)

@manejar_excepcion_sqlalchemy
def agregar_producto_vendido(producto_id, cantidad, precio_venta_unitario):
    producto_vendido = ProductoVendido(
        producto_id=producto_id,
        cantidad=cantidad,
        precio_venta_unitario=precio_venta_unitario
    )
    session.add(producto_vendido)


    
    
