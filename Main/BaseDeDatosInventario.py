from sqlalchemy import Column, Integer, DateTime, Float, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///Main/Inventario.db', echo=True)
Base = declarative_base()

class Cliente(Base):
    __tablename__ = 'Clientes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    apellido = Column(String(255))
    cedula = Column(Integer, unique=True)
    correo = Column(String(255), unique=True)
    telefono = Column(Integer)
    direccion = Column(String(255))
    notas_adicionales = Column(String(500))

class Venta(Base):
    __tablename__ = 'Ventas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha_venta = Column(DateTime, default=datetime.now(), nullable=False)
    realizada_por = Column(String(255))
    cliente_id = Column(Integer, nullable=False)
    porcentaje_iva = Column(Float, nullable=False)
    metodo_pago = Column(String(100))
    metodo_envio = Column(String(100))
    total_venta = Column(Float, nullable=False)
    total_productos = Column(Integer, nullable=False)
    productos = Column(Text)
    
class Producto(Base):
    __tablename__ = 'Productos'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    codigo = Column(Integer, unique=True)
    descripcion = Column(String(500))
    categoria = Column(String(100))
    marca = Column(String(100))
    precio_compra = Column(Float)
    precio_venta = Column(Float)
    precio_mayorista = Column(Float)
    cantidad_unidades = Column(Integer)
    temporada_producto = Column(String(100))
    fecha_adquisicion = Column(DateTime, default=datetime.now())
    fecha_vencimiento = Column(DateTime)
    fragilidad = Column(String(50))
    tipo_producto = Column(String(50))
    proveedor_id = Column(Integer, ForeignKey('Proveedores.id'))
    estado = Column(String(50))

    # Relación con la tabla Proveedor
    proveedor = relationship('Proveedor', back_populates='productos')
    
class ProductoVendido(Base):
    __tablename__ = 'ProductosVendidos'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    producto_id = Column(Integer, nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_venta_unitario = Column(Float, nullable=False)
    
class Proveedor(Base):
    __tablename__ = 'Proveedores'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_contacto = Column(String(255), nullable=False)
    nombre_empresa = Column(String(255), nullable=False)
    numero_proveedor = Column(Integer, unique=True)
    correo_proveedor = Column(String(255), unique=True)
    nit_empresa = Column(Integer, unique=True)
    pagina_web = Column(String(255))
    direccion_empresa = Column(String(255))
    notas_adicionales = Column(String(500))
    
    # Relación inversa con la tabla Producto
    productos = relationship('Producto', back_populates='proveedor')
    
class ProductoSelecionado(Base):
    __tablename__ = 'ProductosSelecionados'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    producto_id = Column(Integer, nullable=False)
    cantidad_unidades = Column(Integer, nullable=False)
    tipo_precio = Column(String(255), nullable=False)
    precio_venta = Column(Float, nullable=False)
    nombre = Column(String(255), nullable=False)
    codigo = Column(Integer)
    descuento = Column(Float)
    
    
    
    
Session = sessionmaker(bind=engine)
session = Session()

if __name__ == '__main__':
    Base.metadata.create_all(engine)
