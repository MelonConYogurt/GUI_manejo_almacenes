from Crud_Base_Datos import *
from faker import Faker
import random

fake = Faker()

for _ in range(100):
    agregar_producto(
    nombre=fake.word(),
    codigo=random.randint(1000, 9999),
    descripcion=fake.sentence(),
    categoria=fake.word(),
    marca=fake.company(),
    precio_compra=random.uniform(1.0, 100.0),
    precio_venta=random.uniform(100.0, 200.0),
    precio_mayorista=random.uniform(80.0, 150.0),
    cantidad_unidades=random.randint(1, 100),
    temporada_producto=fake.word(),
    fecha_adquisicion=fake.date_time_between(start_date="-1y", end_date="now"),
    fecha_vencimiento=fake.date_time_between(start_date="now", end_date="+1y"),
    fragilidad=random.choice(["Alta", "Media", "Baja"]),
    tipo_producto=random.choice(["Electrónica", "Ropa", "Alimentación", "Hogar"]),
    proveedor_id= random.randint(1000, 9999),
    estado=random.choice(["Activo", "Inactivo"])
        )
    
    agregar_proveedor(
    nombre_contacto=fake.name(),
    nombre_empresa=fake.company(),
    numero_proveedor=random.randint(1000, 9999),
    correo_proveedor=fake.email(),
    nit_empresa=random.randint(10000000, 99999999),
    pagina_web=fake.uri(),
    direccion_empresa=fake.address(),
    notas_adicionales=fake.text()
        )
    

    agregar_cliente(
    nombre=fake.first_name(),
    apellido=fake.last_name(),
    cedula=random.randint(10000000, 99999999),
    correo=fake.email(),
    telefono=fake.phone_number(),
    direccion=fake.address(),
    notas_adicionales=fake.text()
        )
    
