import customtkinter
import customtkinter as ctk
import os
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from CrearFactura import *
from CTkPDFViewer import *
from tkinter import *
from tkinter import ttk
from CTkXYFrame import *
from CTkToolTip import *
from datetime import datetime, timedelta
from CrearFactura.invoice_generator import *
from tkinter import messagebox
from typing import Union, Callable
from CTkScrollableDropdown import *
from CTkPopupKeyboard import PopupNumpad
from Crud_Base_Datos import * 
from BaseDeDatosInventario import Producto, Proveedor, session
from sqlalchemy import func


class frame_seleccion_nuemeros(customtkinter.CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 step_size: Union[int, float] = 1,
                 command: Callable = None,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.step_size = step_size
        self.command = command

        self.configure(fg_color=("gray78", "gray28"))  # set frame color

        self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand
        self.grid_columnconfigure(1, weight=1)  # entry expands

        self.subtract_button = customtkinter.CTkButton(self, text="-", width=height-6, height=height-6,
                                                       command=self.subtract_button_callback)
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

        self.entry = customtkinter.CTkEntry(self, width=width-(2*height), height=height-6, border_width=0)
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")

        self.add_button = customtkinter.CTkButton(self, text="+", width=height-6, height=height-6,
                                                  command=self.add_button_callback)
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

        # default value
        self.entry.insert(0, "0.0")

    def add_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = float(self.entry.get()) + self.step_size
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return

    def subtract_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = float(self.entry.get()) - self.step_size
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return

    def get(self) -> Union[float, None]:
        try:
            return float(self.entry.get())
        except ValueError:
            return None

    def set(self, value: float):
        self.entry.delete(0, "end")
        self.entry.insert(0, str(float(value)))

class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")
   

class aplicacion(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        w, h = self.winfo_screenwidth(), self.winfo_screenheight()                                    
        self.geometry("%dx%d+0+0" % (w, h))
        self.minsize(1000,650)
        self.grid_rowconfigure(2, weight=1, uniform='a')  
        self.grid_columnconfigure(1, weight=1, uniform='a')
        self.title("Inventory")
        
        # Frame arriba menu:
        self.frame_menu_parte_alta = customtkinter.CTkFrame(master=self, width= 50, height= 50, fg_color="#2b2b2b")
        self.frame_menu_parte_alta.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        #Configuramos el grid:
        self.frame_menu_parte_alta.grid_columnconfigure((0,1,2,3,4,5), weight=1, uniform='a')
    
        # Frames barra de menú:
        self.frame_menu = customtkinter.CTkFrame(master=self, fg_color="#2b2b2b")
        self.frame_menu.grid(row=1, column=0, padx=5, rowspan=2, pady=5, sticky="nsew")
        #Frame base para todo el inicio
        self.frame_Menu_base= customtkinter.CTkFrame(master=self, fg_color="transparent") 
        self.frame_Menu_base.grid(row=1, column=1, padx=5, rowspan=2, pady=5, sticky="nsew")
        #Configuramos el grid:3
        self.frame_Menu_base.grid_columnconfigure((0,1), weight=1, uniform='a')
        self.frame_Menu_base.grid_rowconfigure((0,1), weight=1, uniform='a')
        
        #Frames principales para los menus dentro del menu lateral:
        self.frame_Menu_inicio= customtkinter.CTkFrame(master=self.frame_Menu_base, fg_color="#242424")
        self.frame_Menu_analitica = customtkinter.CTkScrollableFrame(master=self.frame_Menu_base, fg_color="#242424", orientation="vertical")
        self.frame_Menu_contactos = customtkinter.CTkFrame(master=self.frame_Menu_base, fg_color="#242424")
        self.frame_Menu_inventario = customtkinter.CTkFrame(master=self.frame_Menu_base, fg_color="#242424")
        self.frame_Menu_catalogo = customtkinter.CTkFrame(master=self.frame_Menu_base, fg_color="#242424")
        self.frame_Menu_tiendas = customtkinter.CTkFrame(master=self.frame_Menu_base, fg_color="#242424")
        self.frame_Menu_ventas = customtkinter.CTkFrame(master=self.frame_Menu_base, fg_color="#242424")
        self.frame_Menu_vacio_N1 = customtkinter.CTkFrame(master=self.frame_Menu_base, fg_color="#242424")
        
        #configuramos el grid
        self.frame_Menu_ventas.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20), weight=1, uniform='a')  
        self.frame_Menu_ventas.grid_columnconfigure((0,1), weight=1, uniform='a')
        #configuramos el grid
        self.frame_Menu_vacio_N1.grid_rowconfigure((0,1,2), weight=1, uniform='a')  
        self.frame_Menu_vacio_N1.grid_columnconfigure((0,1), weight=1, uniform='a')
        
        #Configuramos el grid:
        self.frame_Menu_inicio.grid_rowconfigure((0,1), weight=1, uniform='a')  
        self.frame_Menu_inicio.grid_columnconfigure((0,1), weight=1, uniform='a')
        #
        self.frame_Menu_inicio_N1 = customtkinter.CTkFrame(master=self.frame_Menu_inicio, fg_color="#2b2b2b")
        self.frame_Menu_inicio_N1.grid(row=0, column=0, padx=5,  pady=5, sticky="nsew")
        self.frame_Menu_inicio_N2 = customtkinter.CTkFrame(master=self.frame_Menu_inicio, fg_color="#2b2b2b")
        self.frame_Menu_inicio_N2.grid(row=1, column=0, padx=5,  pady=5, sticky="nsew")
        self.frame_Menu_inicio_N3 = customtkinter.CTkFrame(master=self.frame_Menu_inicio, fg_color="#2b2b2b")
        self.frame_Menu_inicio_N3.grid(row=0, column=1, padx=5,  pady=5, sticky="nsew")
        self.frame_Menu_inicio_N4 = customtkinter.CTkFrame(master=self.frame_Menu_inicio, fg_color="#2b2b2b")
        self.frame_Menu_inicio_N4.grid(row=1, column=1, padx=5,  pady=5, sticky="nsew")
        
        # Configurar el contenedor principal para que ocupe todo el espacio disponible
        self.frame_Menu_analitica.grid_rowconfigure((0, 1, 2, 3), weight=1, uniform='a')
        self.frame_Menu_analitica.grid_columnconfigure(0, weight=1, uniform='a')

        # Crear los frames y colocarlos en la cuadrícula
        self.frame_Menu_analitica_N1 = customtkinter.CTkScrollableFrame(
            master=self.frame_Menu_analitica,
            fg_color="#ffffff",
            orientation="horizontal",
            height=800  
        )
        self.frame_Menu_analitica_N1.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.frame_Menu_analitica_N2 = customtkinter.CTkScrollableFrame(
            master=self.frame_Menu_analitica,
            fg_color="#ffffff",
            orientation="horizontal",
            height=800 
        )
        self.frame_Menu_analitica_N2.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.frame_Menu_analitica_N3 = customtkinter.CTkScrollableFrame(
            master=self.frame_Menu_analitica,
            fg_color="#ffffff",
            orientation="horizontal",
            height=800  
        )
        self.frame_Menu_analitica_N3.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

        self.frame_Menu_analitica_N4 = customtkinter.CTkScrollableFrame(
            master=self.frame_Menu_analitica,
            fg_color="#ffffff",
            orientation="horizontal",
            height=800  
        )
        self.frame_Menu_analitica_N4.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")

        
        #Frames para el menu de contactanos:
        self.frame_Menu_contactos.grid_rowconfigure((0), weight=1, uniform='a')  
        self.frame_Menu_contactos.grid_columnconfigure((0), weight=1, uniform='a')
        #Frame Base contactos
        self.frame_Menu_contactos_base =  customtkinter.CTkScrollableFrame(master=self.frame_Menu_contactos, fg_color="#2b2b2b", orientation="horizontal")
        self.frame_Menu_contactos_base.grid(row=0, rowspan=1, column=0, columnspan=1, padx=1,  pady=1, sticky="nsew")
       
        
        #Frames para el menu de inventarios:
        self.frame_Menu_inventario.grid_rowconfigure((0), weight=1, uniform='a')  
        self.frame_Menu_inventario.grid_columnconfigure((0), weight=1, uniform='a')
        #
        self.frame_Menu_inventario_N1 =  customtkinter.CTkScrollableFrame(master=self.frame_Menu_inventario, fg_color="#2b2b2b", orientation="horizontal")
        self.frame_Menu_inventario_N1.grid(row=0, column=0, padx=5,  pady=5, sticky="nsew")
       
        
        #Frames para el menu de catalogo:
        self.frame_Menu_catalogo.grid_rowconfigure((0,1), weight=1, uniform='a')  
        self.frame_Menu_catalogo.grid_columnconfigure((0,1), weight=1, uniform='a')
        #
        self.frame_Menu_catalogo_N1 = customtkinter.CTkFrame(master=self.frame_Menu_catalogo, fg_color="#2b2b2b")
        self.frame_Menu_catalogo_N1.grid(row=0, column=0, padx=5,  pady=5, sticky="nsew")
        self.frame_Menu_catalogo_N2 = customtkinter.CTkFrame(master=self.frame_Menu_catalogo, fg_color="#2b2b2b")
        self.frame_Menu_catalogo_N2.grid(row=1, column=0, padx=5,  pady=5, sticky="nsew")
        self.frame_Menu_catalogo_N3 = customtkinter.CTkFrame(master=self.frame_Menu_catalogo, fg_color="#2b2b2b")
        self.frame_Menu_catalogo_N3.grid(row=0, column=1, padx=5,  pady=5, sticky="nsew")
        self.frame_Menu_catalogo_N4 = customtkinter.CTkFrame(master=self.frame_Menu_catalogo, fg_color="#2b2b2b")
        self.frame_Menu_catalogo_N4.grid(row=1, column=1, padx=5,  pady=5, sticky="nsew")
       
        #Frames para el menu de tiendas:
        self.frame_Menu_tiendas.grid_rowconfigure((0,1), weight=1, uniform='a')  
        self.frame_Menu_tiendas.grid_columnconfigure((0,1), weight=1, uniform='a')
        #
        self.frame_Menu_tiendas_N1 = customtkinter.CTkFrame(master=self.frame_Menu_tiendas, fg_color="#2b2b2b")
        self.frame_Menu_tiendas_N1.grid(row=0, column=0, padx=5,  pady=5, sticky="nsew")
        self.frame_Menu_tiendas_N2 = customtkinter.CTkFrame(master=self.frame_Menu_tiendas, fg_color="#2b2b2b")
        self.frame_Menu_tiendas_N2.grid(row=1, column=0, padx=5,  pady=5, sticky="nsew")
        self.frame_Menu_tiendas_N3 = customtkinter.CTkFrame(master=self.frame_Menu_tiendas, fg_color="#2b2b2b")
        self.frame_Menu_tiendas_N3.grid(row=0, column=1, padx=5,  pady=5, sticky="nsew")
        self.frame_Menu_tiendas_N4 = customtkinter.CTkFrame(master=self.frame_Menu_tiendas, fg_color="#2b2b2b")
        self.frame_Menu_tiendas_N4.grid(row=1, column=1, padx=5,  pady=5, sticky="nsew")
       
        #Frames para el menu de ventas:
        self.frame_Menu_ventas_N1 = customtkinter.CTkFrame(master=self.frame_Menu_ventas, fg_color="#2b2b2b", )#width=1745, height=48
        self.frame_Menu_ventas_N1.grid(row=0, column=0, rowspan=1 ,columnspan=2, padx=5, pady=5, sticky="nsew")
        #Configuramos el grid:
        self.frame_Menu_ventas_N1.grid_rowconfigure((0), weight=1, uniform='a')
        self.frame_Menu_ventas_N1.grid_columnconfigure((0), weight=1, uniform='a')
        #
        self.frame_Menu_ventas_N2 = customtkinter.CTkFrame(master=self.frame_Menu_ventas, fg_color="#212121", )#width=1745, height=410 3c3c3c
        self.frame_Menu_ventas_N2.grid(row=1, column=0,  rowspan=11, columnspan=2, padx=5, pady=5, sticky="nsew")
        #Configuramos el grid:
        self.frame_Menu_ventas_N2.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9,10), weight=1, uniform='a')  
        self.frame_Menu_ventas_N2.grid_columnconfigure((0,1,2,3), weight=1, uniform='a')
        #        
        self.frame_Menu_ventas_N3 = customtkinter.CTkFrame(master=self.frame_Menu_ventas, fg_color="#212121", )#width=1745, height=50 3c3c3c
        self.frame_Menu_ventas_N3.grid(row=12, column=0,  rowspan=9, columnspan=2, padx=5,  pady=5, sticky="nsew")
        #Configuramos el grid:
        self.frame_Menu_ventas_N3.grid_rowconfigure((0,1,2,3,4,5,6), weight=1, uniform='a')  
        self.frame_Menu_ventas_N3.grid_columnconfigure((0,1,2,3), weight=1, uniform='a')
           
        #sub frames 
        self.frame_1 = customtkinter.CTkFrame(master=self.frame_Menu_ventas_N3, fg_color="#2b2b2b", )
        self.frame_1.grid(row=0, column=0,  padx=5,  pady=5, sticky="nsew")
        #
        self.frame_2 = customtkinter.CTkFrame(master=self.frame_Menu_ventas_N3, fg_color="#2b2b2b", )
        self.frame_2.grid(row=1, column=0, rowspan=6, padx=5,  pady=5, sticky="nsew")
         #
        self.frame_2_scroll = customtkinter.CTkScrollableFrame(master=self.frame_2, fg_color="#2b2b2b", orientation="horizontal" )
        self.frame_2_scroll.pack(fill="both", expand=True)
        #
        self.frame_3 = customtkinter.CTkFrame(master=self.frame_Menu_ventas_N3, fg_color="#2b2b2b", )
        self.frame_3.grid(row=0, column=1, columnspan=2, padx=5,  pady=5, sticky="nsew")
        #
        self.frame_4 = customtkinter.CTkFrame(master=self.frame_Menu_ventas_N3, fg_color="#2b2b2b", )
        self.frame_4.grid(row=1, column=1,  padx=5,  pady=5, sticky="nsew")
        #
        self.frame_5 = customtkinter.CTkFrame(master=self.frame_Menu_ventas_N3, fg_color="#2b2b2b", )
        self.frame_5.grid(row=2, column=1,  padx=5,  pady=5, sticky="nsew")
        #
        self.frame_7 = customtkinter.CTkFrame(master=self.frame_Menu_ventas_N3, fg_color="#2b2b2b", )
        self.frame_7.grid(row=3, column=1, padx=5,  pady=5, sticky="nsew")
        #
        self.frame_8 = customtkinter.CTkFrame(master=self.frame_Menu_ventas_N3, fg_color="#2b2b2b", )
        self.frame_8.grid(row=1, column=2,  padx=5,  pady=5, sticky="nsew")
        #
        self.frame_9 = customtkinter.CTkFrame(master=self.frame_Menu_ventas_N3, fg_color="#2b2b2b", )
        self.frame_9.grid(row=2, column=2,  padx=5,  pady=5, sticky="nsew")
        #
        self.frame_10 = customtkinter.CTkFrame(master=self.frame_Menu_ventas_N3, fg_color="#2b2b2b", )
        self.frame_10.grid(row=3, column=2, padx=5,  pady=5, sticky="nsew")
        #
        self.frame_12 = customtkinter.CTkFrame(master=self.frame_Menu_ventas_N3, fg_color="#212121", )
        self.frame_12.grid(row=4, rowspan= 4, column= 1, columnspan= 2 ,padx=5,  pady=5, sticky="nsew")
        #
        self.frame_factura = customtkinter.CTkFrame(master=self.frame_Menu_ventas_N3, fg_color="#212121", ) #1e1e1e
        self.frame_factura.grid(row=0, rowspan=7, column=3,  padx=5,  pady=5, sticky="nsew")
        #
        self.frame_factura.grid_rowconfigure((0,1,2,3,4,5), weight=1, uniform='a') 
        self.frame_factura.grid_columnconfigure((0,1), weight=1, uniform='a')
        #
        self.frame_factura_1 = customtkinter.CTkFrame(master=self.frame_factura, fg_color="#2b2b2b", )
        self.frame_factura_1.grid(row=0, column=0, columnspan=2, padx=5,  pady=(0,20), sticky="nsew")
        #
        self.frame_factura_2 = customtkinter.CTkFrame(master=self.frame_factura, fg_color="#2b2b2b", )
        self.frame_factura_2.grid(row=1, column=0, columnspan=1, padx=5,  pady=5, sticky="nsew")
        #
        self.frame_factura_3 = customtkinter.CTkFrame(master=self.frame_factura, fg_color="#2b2b2b", )
        self.frame_factura_3.grid(row=2, column=0, columnspan=1, padx=5,  pady=5, sticky="nsew")
        #
        self.frame_factura_4 = customtkinter.CTkFrame(master=self.frame_factura, fg_color="#2b2b2b", )
        self.frame_factura_4.grid(row=3, column=0, columnspan=1, padx=5,  pady=5, sticky="nsew")
        #
        self.frame_factura_5 = customtkinter.CTkFrame(master=self.frame_factura, fg_color="#2b2b2b", )
        self.frame_factura_5.grid(row=4, column=0, columnspan=1, padx=5,  pady=5, sticky="nsew")
        
        self.frame_factura_6 = customtkinter.CTkFrame(master=self.frame_factura, fg_color="#2b2b2b", )
        self.frame_factura_6.grid(row=5, column=0, columnspan=2, padx=5,  pady=5, sticky="nsew")
        #
        self.frame_factura_7 = customtkinter.CTkFrame(master=self.frame_factura, fg_color="#2b2b2b", )
        self.frame_factura_7.grid(row=1, column=1, columnspan=1, padx=5,  pady=5, sticky="nsew")
        #
        self.frame_factura_8 = customtkinter.CTkFrame(master=self.frame_factura, fg_color="#2b2b2b", )
        self.frame_factura_8.grid(row=2, column=1, columnspan=1, padx=5,  pady=5, sticky="nsew")
        #
        self.frame_factura_9 = customtkinter.CTkFrame(master=self.frame_factura, fg_color="#2b2b2b", )
        self.frame_factura_9.grid(row=3, column=1, columnspan=1, padx=5,  pady=5, sticky="nsew")
        #
        self.frame_factura_10 = customtkinter.CTkFrame(master=self.frame_factura, fg_color="#2b2b2b", )
        self.frame_factura_10.grid(row=4, column=1, columnspan=1, padx=5,  pady=5, sticky="nsew")
        #
       
        #Frames barra de busqueda
        self.busqueda_frame_1 = customtkinter.CTkFrame(master=self.frame_Menu_ventas_N1, fg_color="#2b2b2b", )
        self.busqueda_frame_1.grid(row=0, column=0, padx=5,  pady=1, sticky="nsew")
    
        #frames par la base de datos:
        self.frame_database = customtkinter.CTkFrame(master=self.frame_Menu_ventas_N2, fg_color="#2b2b2b")
        self.frame_database.grid(row=0, column=0,  padx=5, rowspan=10, columnspan=4,  pady=(5,5), sticky="nsew")
        #
        self.frame_database_scroll = customtkinter.CTkScrollableFrame(master=self.frame_database, fg_color="#2b2b2b", orientation="horizontal")
        self.frame_database_scroll.pack(fill="both", expand=True)
        #
        self.frame_database_numero_unidades = customtkinter.CTkFrame(master=self.frame_Menu_ventas_N2, fg_color="#2b2b2b")
        self.frame_database_numero_unidades.grid(row=10, column=0,  padx=5,  pady=(0,5), sticky="nsew")
        #
        self.frame_database_tipo_precio = customtkinter.CTkFrame(master=self.frame_Menu_ventas_N2, fg_color="#2b2b2b")
        self.frame_database_tipo_precio.grid(row=10, column=1,  padx=5,  pady=(0,5), sticky="nsew")
        #
        self.frame_database_elemento_descuento = customtkinter.CTkFrame(master=self.frame_Menu_ventas_N2, fg_color="#2b2b2b")
        self.frame_database_elemento_descuento.grid(row=10, column=2,  padx=5,  pady=(0,5), sticky="nsew")
        #        
        self.frame_database_boton_anadir = customtkinter.CTkFrame(master=self.frame_Menu_ventas_N2, fg_color="#2b2b2b")
        self.frame_database_boton_anadir.grid(row=10, column=3,  padx=5,  pady=(0,5), sticky="nsew")
   
        # Aplicar pack_propagate(0) o grid_propagate(0) a todos los frames
        # Frames para el menu de ventas
        self.frame_Menu_ventas.pack_propagate(0)
        self.frame_Menu_ventas_N1.pack_propagate(0)
        self.frame_Menu_ventas_N2.pack_propagate(0)
        self.frame_Menu_ventas_N3.pack_propagate(0)
        self.frame_1.pack_propagate(0)
        self.frame_2.pack_propagate(0)
        self.frame_3.pack_propagate(0)
        self.frame_4.pack_propagate(0)
        self.frame_5.pack_propagate(0)
        #self.frame_6.pack_propagate(0)
        self.frame_7.pack_propagate(0)
        self.frame_8.pack_propagate(0)
        self.frame_9.pack_propagate(0)
        self.frame_10.pack_propagate(0)
        #self.frame_11.pack_propagate(0)
        self.frame_12.pack_propagate(0)
        self.frame_factura.pack_propagate(0)
        self.frame_factura_1.pack_propagate(0)
        self.frame_factura_2.pack_propagate(0)
        self.frame_factura_3.pack_propagate(0)
        self.frame_factura_4.pack_propagate(0)
        self.frame_factura_5.pack_propagate(0)
        self.frame_factura_6.pack_propagate(0)
        self.frame_factura_7.pack_propagate(0)
        self.frame_factura_8.pack_propagate(0)
        self.frame_factura_9.pack_propagate(0)
        self.frame_factura_10.pack_propagate(0)
        #self.frame_factura_11.pack_propagate(0)
        # Frames barra de busqueda
        self.busqueda_frame_1.pack_propagate(0)
        # Frames para la base de datos
        self.frame_database.pack_propagate(0)
        self.frame_database_numero_unidades.pack_propagate(0)
        self.frame_database_tipo_precio.pack_propagate(0)
        self.frame_database_elemento_descuento.pack_propagate(0)
        self.frame_database_boton_anadir.pack_propagate(0)

        
        self.titulo_busqueda_data_base_nombre = customtkinter.CTkLabel(self.busqueda_frame_1,
                                                        text="Busqueda por nombre del producto:")
        self.titulo_busqueda_data_base_nombre.pack(side="left", padx=5, pady=5)
        #
        self.busqueda_data_base_nombre = customtkinter.CTkEntry(self.busqueda_frame_1,
                                                         width=240, placeholder_text="Nombre producto")
        self.busqueda_data_base_nombre.pack(side="left", padx=5, pady=5)
        #
        self.titulo_busqueda_data_base_codigo = customtkinter.CTkLabel(self.busqueda_frame_1,
                                                        text="Busqueda por el codigo asignado:")
        self.titulo_busqueda_data_base_codigo.pack(side="left", padx=5, pady=5)
        #
        self.busqueda_data_base_codigo = customtkinter.CTkEntry(self.busqueda_frame_1,
                                                         width=240, placeholder_text="Codigo producto")
        self.busqueda_data_base_codigo.pack(side="left", padx=5, pady=5)
        #
        self.boton_filtrar_busqueda = customtkinter.CTkButton(self.busqueda_frame_1,
                                                        text="Filtar datos", command= lambda: self.filtrar_por_codigo())
        self.boton_filtrar_busqueda.pack(side="left", padx=5, pady=5)
        #
        self.boton_reestablecer_vista = customtkinter.CTkButton(self.busqueda_frame_1,
                                                        text="Reestablecer datos", command= lambda: self.reestablecer_todos_los_datos())
        self.boton_reestablecer_vista.pack(side="left", padx=5, pady=5)
        #
        self.unidades_producto_data_base = customtkinter.CTkLabel(self.frame_database_numero_unidades,
                                                        text="Digita la cantidad de unidades:")
        self.unidades_producto_data_base.pack(side="left", padx=5, pady=5)
        #
        self.cantidad_de_productos_entrada = frame_seleccion_nuemeros(self.frame_database_numero_unidades,width=150, step_size=1 )
        self.cantidad_de_productos_entrada.pack(side="left", padx=(30,5), pady=0)
        #
        self.seleccionar_precio_producto_data_base = customtkinter.CTkLabel(self.frame_database_tipo_precio,
                                                        text="Selecciona el tipo de precio:")
        self.seleccionar_precio_producto_data_base.pack(side="left", padx=5, pady=5)
        #
        self.valores_tipo_precio = ["Normal","Mayorista"]
        self.tipo_de_precio_entrada= customtkinter.CTkOptionMenu(self.frame_database_tipo_precio, width=180)
        self.tipo_de_precio_entrada.pack(side="left", padx=(30,5), pady=5)
        self.tipo_de_precio_entrada.set("Normal")
        CTkScrollableDropdown(self.tipo_de_precio_entrada, values=self.valores_tipo_precio)
        #
        self.descuento_producto_data_base = customtkinter.CTkLabel(self.frame_database_elemento_descuento,
                                                        text="Si aplica descuesto para el producto:")
        self.descuento_producto_data_base.pack(side="left", padx=5, pady=5)
        #
        self.descuento_de_productos_entrada = frame_seleccion_nuemeros(self.frame_database_elemento_descuento,width=150, step_size=1 )
        self.descuento_de_productos_entrada.pack(side="left", padx=(30,5), pady=0)
        #
        self.seleccionar_producto_data_base = customtkinter.CTkLabel(self.frame_database_boton_anadir,
                                                        text="Añadir el elemento seleccionado")
        self.seleccionar_producto_data_base.pack(side="left", padx=5, pady=5)
        #
        self.anadir_producto_seleccionado_boton = customtkinter.CTkButton(self.frame_database_boton_anadir, 
                                                                          text="Añadir elemento", width= 180, command= lambda: self.obtener_elemento_seleccionado())
        self.anadir_producto_seleccionado_boton.pack(side="left", padx=(30,5), pady=0)
        #
        self.producto_seleccionado_data_base = customtkinter.CTkLabel(self.frame_1,
                                                        text="Lista de los productos seleccionados")
        self.producto_seleccionado_data_base.pack(side="left", padx=5, pady=5)
        #
        self.boton_eleminar_producto_selecionado = customtkinter.CTkButton(self.frame_1,
                                                        text="Eliminar producto", command= lambda: self.eliminar_elemento_seleccionado())
        self.boton_eleminar_producto_selecionado.pack(side="left", padx=(20,5), pady=5)
        #
        self.informacion_cliente_data_base = customtkinter.CTkLabel(self.frame_3,
                                                        text="Imformacion basica del cliente:")
        self.informacion_cliente_data_base.pack(side="left", padx=5, pady=5)
        #
        self.buscar_cliente_data_base = customtkinter.CTkLabel(self.frame_3,
                                                        text="Si el cliente ya se ha regsitrado con anterioridad:")
        self.buscar_cliente_data_base.pack(side="left", padx=(125,5), pady=5)
        #
        self.busqueda_cliente_por_cedula = customtkinter.CTkEntry(self.frame_3,
                                                         width=240, placeholder_text="Cedula del cliente")
        self.busqueda_cliente_por_cedula.pack(side="left", padx=5, pady=5)
        #
        self.nombre_cliente = customtkinter.CTkLabel(self.frame_4,
                                                        text="Ingrese el nombre del cliente:")
        self.nombre_cliente.pack(side="left", padx=5, pady=5)
        #
        self.nombre_cliente_entrada = customtkinter.CTkEntry(self.frame_4,
                                                         width=180, placeholder_text="Nombre cliente")
        self.nombre_cliente_entrada.pack(side="right", padx=(5,20), pady=5)
        #
        self.apellido_cliente = customtkinter.CTkLabel(self.frame_8,
                                                        text="Ingrese el apellido del cliente:")
        self.apellido_cliente.pack(side="left", padx=5, pady=5)
        #
        self.apellido_cliente_entrada = customtkinter.CTkEntry(self.frame_8,
                                                         width=180, placeholder_text="Apellido cliente")
        self.apellido_cliente_entrada.pack(side="right", padx=(5,20), pady=5)
        #
        self.cedula_cliente = customtkinter.CTkLabel(self.frame_5,
                                                        text="Digita la cedula del cliente:")
        self.cedula_cliente.pack(side="left", padx=5, pady=5)
        #
        self.cedula_cliente_entrada = customtkinter.CTkEntry(self.frame_5,
                                                         width=180, placeholder_text="Cedula cliente")
        self.cedula_cliente_entrada.pack(side="right", padx=(5,20), pady=5)
        #
        self.correo_cliente = customtkinter.CTkLabel(self.frame_9,
                                                        text="Ingresa el correo del cliente:")
        self.correo_cliente.pack(side="left", padx=5, pady=5)
        #
        self.correo_cliente_entrada = customtkinter.CTkEntry(self.frame_9,
                                                         width=180, placeholder_text="Correo cliente")
        self.correo_cliente_entrada.pack(side="right", padx=(5,20), pady=5)
        #
        self.numero_cliente = customtkinter.CTkLabel(self.frame_10,
                                                        text="Digita el telefeono del cliente:")
        self.numero_cliente.pack(side="left", padx=5, pady=5)
        #
        self.numero_cliente_entrada = customtkinter.CTkEntry(self.frame_10,
                                                         width=180, placeholder_text="Numero cliente")
        self.numero_cliente_entrada.pack(side="right", padx=(5,20), pady=5)
        PopupNumpad(self.numero_cliente_entrada)
        self.herramienta_consejo_numero = CTkToolTip(self.numero_cliente_entrada, message="Haz doble click para mostar el teclado por pantalla")
        #
        self.dirrecion_cliente = customtkinter.CTkLabel(self.frame_7,
                                                        text="Ingresa la dirrecion del cliente:")
        self.dirrecion_cliente.pack(side="left", padx=5, pady=5)
        #
        self.dirrecion_cliente_entrada = customtkinter.CTkEntry(self.frame_7,
                                                         width=180, placeholder_text="Dirrecion del cliente")
        self.dirrecion_cliente_entrada.pack(side="right", padx=(5,20), pady=5)
        #
        self.notas_adiccionales_cliente = customtkinter.CTkTextbox(master=self.frame_12, width=860, fg_color="#2b2b2b")
        self.notas_adiccionales_cliente.insert("0.0", "Ingresa en esta apartado las notas addicionales respecto al cliente. Haz click para empezar a escribir")
        self.notas_adiccionales_cliente.pack(side="left", padx=5, pady=5)
        #
        self.titulo_facturacion = customtkinter.CTkLabel(self.frame_factura_1, text="Imformacion sobre la factura")
        self.titulo_facturacion.pack(pady=15)
        #
        self.label_vendedor = customtkinter.CTkLabel(self.frame_factura_2, text="Nombre del vendedor:")
        self.label_vendedor.pack(side="left", padx=(5,20), pady=5)
        #
        self.label_medio_pago = customtkinter.CTkLabel(self.frame_factura_3, text="Seleccionar medio de pago:")
        self.label_medio_pago.pack(side="left", padx=(5,20), pady=5)
        #
        self.label_metodo_envio = customtkinter.CTkLabel(self.frame_factura_4, text="Seleccionar metodo de envio:")
        self.label_metodo_envio.pack(side="left", padx=(5,20), pady=5)
        #
        self.label_porcentaje_iva = customtkinter.CTkLabel(self.frame_factura_5, text="Ingresar porcentaje de IVA:")
        self.label_porcentaje_iva.pack(side="left", padx=(5,20), pady=5)
        #
        self.el_total_compra = customtkinter.CTkButton(self.frame_factura_6, text="Completar la compra", command= lambda: self.crear_factura() , height=35)
        self.el_total_compra.pack(pady=15)
        #
        self.valores_empleados =["Empleado 1","Empleado 2","Empleado 3","Empleado 4","Empleado 5","Empleado 6"]
        self.empleado_que_vendio_entrada = customtkinter.CTkComboBox(self.frame_factura_7, width=180)
        self.empleado_que_vendio_entrada.pack(padx=5, pady=(13,13))
        self.empleado_que_vendio_entrada.set("Empleado 1")
        CTkScrollableDropdown(self.empleado_que_vendio_entrada, values=self.valores_empleados)
        #
        self.valores_medio_de_pago = ["Medio pago 1","Medio pago 2","Medio pago 3","Medio pago 4","Medio pago 5","Medio pago 6"]
        self.medio_de_pago_entrada = customtkinter.CTkOptionMenu(self.frame_factura_8, width=180)
        self.medio_de_pago_entrada.pack(padx=5, pady=(11,5))
        self.medio_de_pago_entrada.set("Medio pago 1")
        CTkScrollableDropdown(self.medio_de_pago_entrada, values=self.valores_medio_de_pago)
        #
        self.valores_metodo_de_envio = ["Envio 1","Envio 2","Envior 3","Envio 4","Envio 5","Envio 6"]
        self.metodo_de_envio_entrada = customtkinter.CTkOptionMenu(self.frame_factura_9, width=180)
        self.metodo_de_envio_entrada.set("Envio 1")
        self.metodo_de_envio_entrada.pack(padx=5, pady=(13,13))
        CTkScrollableDropdown(self.metodo_de_envio_entrada, values=self.valores_metodo_de_envio)
        #
        self.porcentaje_de_iva_entrada = frame_seleccion_nuemeros(self.frame_factura_10, width=180, step_size=1 )
        self.porcentaje_de_iva_entrada.pack(padx=5, pady=(10,10))
        #Frames para el menu de incio:
        self.frame_Menu_vacio_N1_N1 = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1, fg_color="#212121", )
        self.frame_Menu_vacio_N1_N1.grid(row=0, column=0, columnspan=2, padx=5,  pady=5, sticky="nsew")
        #
        self.frame_Menu_vacio_N1_N1.grid_rowconfigure((0,1,2,3,4), weight=1, uniform='a')  
        self.frame_Menu_vacio_N1_N1.grid_columnconfigure((0,1,2,3), weight=1, uniform='a')
        #
        self.frame_Menu_vacio_N1_N2 = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1, fg_color="#212121", )
        self.frame_Menu_vacio_N1_N2.grid(row=1, column=0, columnspan=2, padx=5,  pady=5, sticky="nsew")
        #
        self.frame_Menu_vacio_N1_N2.grid_rowconfigure((0,1,2,3,4), weight=1, uniform='a')  
        self.frame_Menu_vacio_N1_N2.grid_columnconfigure((0,1,2,3), weight=1, uniform='a')
        #
        self.frame_Menu_vacio_N1_N3 = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1, fg_color="#212121", )
        self.frame_Menu_vacio_N1_N3.grid(row=2, column=0, columnspan=2, padx=5,  pady=5, sticky="nsew")
        #
        self.frame_Menu_vacio_N1_N3.grid_rowconfigure((0,1,2,3,4), weight=1, uniform='a') 
        self.frame_Menu_vacio_N1_N3.grid_columnconfigure((0,1,2,3), weight=1, uniform='a')
        #
        self.frame_titulo_producto = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1_N1, fg_color="#2b2b2b", )
        self.frame_titulo_producto.grid(row=0, column=0, columnspan=4, padx=5,  pady=5, sticky="nsew")
        #
        self.frame_titulo_producto1 = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1_N1, fg_color="#2b2b2b", )
        self.frame_titulo_producto1.grid(row=1, column=0,  padx=5,  pady=5, sticky="nsew")
        #
        self.frame_titulo_producto2 = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1_N1, fg_color="#2b2b2b", )
        self.frame_titulo_producto2.grid(row=1, column=1,  padx=5,  pady=5, sticky="nsew")
        #
        self.frame_titulo_producto3 = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1_N1, fg_color="#2b2b2b", )
        self.frame_titulo_producto3.grid(row=2, column=0,  padx=5,  pady=5, sticky="nsew")
        #
        self.frame_titulo_producto4 = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1_N1, fg_color="#2b2b2b", )
        self.frame_titulo_producto4.grid(row=2, column=1,  padx=5,  pady=5, sticky="nsew")
        #
        self.frame_titulo_producto5 = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1_N1, fg_color="#2b2b2b", )
        self.frame_titulo_producto5.grid(row=3, column=0,  padx=5,  pady=5, sticky="nsew")
        #
        self.frame_titulo_producto6 = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1_N1, fg_color="#2b2b2b", )
        self.frame_titulo_producto6.grid(row=3, column=1,  padx=5,  pady=5, sticky="nsew")
        #
        self.frame_titulo_producto7 = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1_N1, fg_color="#2b2b2b", )
        self.frame_titulo_producto7.grid(row=4, column=0, padx=5,  pady=5, sticky="nsew")
        #
        self.frame_titulo_producto8 = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1_N1, fg_color="#2b2b2b", )
        self.frame_titulo_producto8.grid(row=4, column=1,  padx=5,  pady=5, sticky="nsew")
        #
        self.frame_titulo_producto9 = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1_N1, fg_color="#2b2b2b", )
        self.frame_titulo_producto9.grid(row=1, column=2,  padx=5,  pady=5, sticky="nsew")
        #
        self.frame_titulo_producto10 = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1_N1, fg_color="#2b2b2b", )
        self.frame_titulo_producto10.grid(row=1, column=3,  padx=5,  pady=5, sticky="nsew")
        #
        self.frame_titulo_producto11 = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1_N1, fg_color="#2b2b2b", )
        self.frame_titulo_producto11.grid(row=2, column=2,  padx=5,  pady=5, sticky="nsew")
        #
        self.frame_titulo_producto12 = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1_N1, fg_color="#2b2b2b", )
        self.frame_titulo_producto12.grid(row=2, column=3,  padx=5,  pady=5, sticky="nsew")
        #
        self.frame_titulo_producto13 = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1_N1, fg_color="#2b2b2b", )
        self.frame_titulo_producto13.grid(row=3, column=2,  padx=5,  pady=5, sticky="nsew")
        #
        self.frame_titulo_producto14 = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1_N1, fg_color="#2b2b2b", )
        self.frame_titulo_producto14.grid(row=3, column=3,  padx=5,  pady=5, sticky="nsew")
        #
        self.frame_titulo_producto15 = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1_N1, fg_color="#2b2b2b", )
        self.frame_titulo_producto15.grid(row=4, column=2, padx=5,  pady=5, sticky="nsew")
        #
        self.frame_titulo_producto16 = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1_N1, fg_color="#2b2b2b", )
        self.frame_titulo_producto16.grid(row=4, column=3,  padx=5,  pady=5, sticky="nsew")
        #
        self.titulo_nuevo_producto = customtkinter.CTkLabel(self.frame_titulo_producto,
                                                        text="Informacion principal del producto. Por favor, Completa todos los campos presentes:")
        self.titulo_nuevo_producto.pack(side= "left", padx=5, pady=5)
        
        self.titulo_anadir_producto = customtkinter.CTkLabel(self.frame_titulo_producto,
                                                        text="Si ya haz completado todos los campos, añade el producto a la base de datos:")
        self.titulo_anadir_producto.pack(side= "left",padx=(600,5), pady=5)
        #
        self.nombre_nuevo_producto = customtkinter.CTkLabel(self.frame_titulo_producto1,
                                                        text="Escribe el nombre del nuevo producto:")
        self.nombre_nuevo_producto.grid(row=0, column=0, padx=5, pady=12, sticky="nsew")
        #
        self.codigo_nuevo_producto = customtkinter.CTkLabel(self.frame_titulo_producto3,
                                                        text="Digita el codigo del producto:")
        self.codigo_nuevo_producto.grid(row=0, column=0, padx=5, pady=12, sticky="nsew")
        #
        self.descripcion_nuevo_producto = customtkinter.CTkLabel(self.frame_titulo_producto5,
                                                        text="Escribe una descripsion corta para el producto:")
        self.descripcion_nuevo_producto.grid(row=0, column=0, padx=5, pady=12, sticky="nsew")
        #
        self.marca_nuevo_producto = customtkinter.CTkLabel(self.frame_titulo_producto7,
                                                        text="Selecciona una marca registrada o escribe la marca:")
        self.marca_nuevo_producto.grid(row=0, column=0, padx=5, pady=12, sticky="nsew")
        #
        self.categoria_nuevo_producto = customtkinter.CTkLabel(self.frame_titulo_producto9,
                                                        text="Selecciona una categoria registrada o escribe una:")
        self.categoria_nuevo_producto.grid(row=0, column=0, padx=5, pady=12, sticky="nsew")
        #
        self.codigo_auto_nuevo_producto = customtkinter.CTkLabel(self.frame_titulo_producto11,
                                                        text="Seleciona el recuadro para generar el codigo:")
        self.codigo_auto_nuevo_producto.grid(row=0, column=0, padx=5, pady=12, sticky="nsew")
        #
        self.temporada_nuevo_producto = customtkinter.CTkLabel(self.frame_titulo_producto13,
                                                        text="Digita la temporada para el producto:")
        self.temporada_nuevo_producto.grid(row=0, column=0, padx=5, pady=12, sticky="nsew")
        #
        self.tienda_nuevo_producto = customtkinter.CTkLabel(self.frame_titulo_producto15,
                                                        text="Escribe o selecciona el estado del produto")
        self.tienda_nuevo_producto.grid(row=0, column=0, padx=5, pady=12, sticky="nsew")
        #
        self.boton_anadir_producto_db = customtkinter.CTkButton(self.frame_titulo_producto, 
                                                    text="Añadir proructo", command= lambda: self.obtener_datos_producto_nuevo())
        self.boton_anadir_producto_db.pack(side= "left", padx=5, pady=5)
        #
        self.nombre_nuevo_producto_entrada = customtkinter.CTkEntry(self.frame_titulo_producto2,
                                                        width=380, placeholder_text="Nombre producto",)
        self.nombre_nuevo_producto_entrada.grid(row=0, column=0, padx=22, pady=12, sticky="nsew")
        #
        self.codigo_nuevo_producto_entrada = customtkinter.CTkEntry(self.frame_titulo_producto4,
                                                         width=380, placeholder_text="Codigo producto")
        self.codigo_nuevo_producto_entrada.grid(row=0, column=0, padx=22, pady=12, sticky="nsew")
        PopupNumpad(self.codigo_nuevo_producto_entrada)
        self.herramienta_consejo_codigo = CTkToolTip(self.codigo_nuevo_producto_entrada, message="Haz doble click para mostar el teclado por pantalla")
        #
        self.descripcion_nuevo_producto_entrada = customtkinter.CTkEntry(self.frame_titulo_producto6,
                                                         width=380, placeholder_text="Descripcion producto")
        self.descripcion_nuevo_producto_entrada.grid(row=0, column=0, padx=22, pady=12, sticky="nsew")
        #
        self.valores_marcas= ["Marca 1","Marca 2","Marca 3","Marca 4","Marca 5","Marca 6"]
        self.marca_nuevo_producto_entrada = customtkinter.CTkComboBox(self.frame_titulo_producto8, width=380)
        self.marca_nuevo_producto_entrada.grid(row=0, column=0, padx=22, pady=12, sticky="nsew")
        self.marca_nuevo_producto_entrada.set("Seleciona / Escribe")
        CTkScrollableDropdown(self.marca_nuevo_producto_entrada, values=self.valores_marcas, justify="left", button_color="transparent")
        #
        self.valores_categoria= ["categoria 1","categoria 2","categoria 3","categoria 4","categoria 5","categoria 6"]
        self.categoria_nuevo_producto_entrada = customtkinter.CTkComboBox(self.frame_titulo_producto10, width=380)
        self.categoria_nuevo_producto_entrada.grid(row=0, column=0, padx=22, pady=12, sticky="nsew")
        self.categoria_nuevo_producto_entrada.set("Seleciona / Escribe")
        CTkScrollableDropdown(self.categoria_nuevo_producto_entrada, values=self.valores_categoria, justify="left", button_color="transparent")
        #
        self.codigo_auto_nuevo_producto_entrada= customtkinter.CTkCheckBox(self.frame_titulo_producto12, text="Generar codigo", command=self, onvalue="on", offvalue="off")
        self.codigo_auto_nuevo_producto_entrada.grid(row=0, column=0, padx=22, pady=12, sticky="nsew")
        self.codigo_auto_nuevo_producto_entrada2= customtkinter.CTkCheckBox(self.frame_titulo_producto12, text="Codigo manual", command=self, onvalue="on", offvalue="off")
        self.codigo_auto_nuevo_producto_entrada2.grid(row=0, column=1, padx=22, pady=12, sticky="nsew")
        #
        self.valores_temporada= ["temporada 1","temporada 2","temporada 3","temporada 4","temporada 5","temporada 6"]
        self.temporada_nuevo_producto_entrada = customtkinter.CTkComboBox(self.frame_titulo_producto14, width=380)
        self.temporada_nuevo_producto_entrada.grid(row=0, column=0, padx=22, pady=12, sticky="nsew")
        self.temporada_nuevo_producto_entrada.set("Seleciona / Escribe")
        CTkScrollableDropdown(self.temporada_nuevo_producto_entrada, values=self.valores_temporada, justify="left", button_color="transparent")
        #
        self.valores_estado= ["estado 1","estado 2","estado 3","estado 4","estado 5","estado 6"]
        self.tienda_nuevo_producto_entrada = customtkinter.CTkComboBox(self.frame_titulo_producto16, width=380)
        self.tienda_nuevo_producto_entrada.grid(row=0, column=0, padx=22, pady=12, sticky="nsew")
        self.tienda_nuevo_producto_entrada.set("Seleciona / Escribe")
        CTkScrollableDropdown(self.tienda_nuevo_producto_entrada, values=self.valores_estado, justify="left", button_color="transparent")
        #
        self.frame_producto = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1_N2, fg_color="#2b2b2b", )
        self.frame_producto.grid(row=0, column=0, columnspan=4, padx=5,  pady=5, sticky="nsew")
        #
        self.frame_producto1 = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1_N2, fg_color="#2b2b2b", )
        self.frame_producto1.grid(row=1, column=0,  padx=5,  pady=5, sticky="nsew")
        #
        self.frame_producto2 = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1_N2, fg_color="#2b2b2b", )
        self.frame_producto2.grid(row=1, column=1,  padx=5,  pady=5, sticky="nsew")
        #
        self.frame_producto3 = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1_N2, fg_color="#2b2b2b", )
        self.frame_producto3.grid(row=2, column=0,  padx=5,  pady=5, sticky="nsew")
        #
        self.frame_producto4 = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1_N2, fg_color="#2b2b2b", )
        self.frame_producto4.grid(row=2, column=1,  padx=5,  pady=5, sticky="nsew")
        #
        self.frame_producto5 = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1_N2, fg_color="#2b2b2b", )
        self.frame_producto5.grid(row=3, column=0,  padx=5,  pady=5, sticky="nsew")
        #
        self.frame_producto6 = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1_N2, fg_color="#2b2b2b", )
        self.frame_producto6.grid(row=3, column=1,  padx=5,  pady=5, sticky="nsew")
        #
        self.frame_producto7 = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1_N2, fg_color="#2b2b2b", )
        self.frame_producto7.grid(row=4, column=0, padx=5,  pady=5, sticky="nsew")
        #
        self.frame_producto8 = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1_N2, fg_color="#2b2b2b", )
        self.frame_producto8.grid(row=4, column=1,  padx=5,  pady=5, sticky="nsew")
        #
        self.frame_producto9 = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1_N2, fg_color="#2b2b2b", )
        self.frame_producto9.grid(row=1, column=2,  padx=5,  pady=5, sticky="nsew")
        #
        self.frame_producto10 = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1_N2, fg_color="#2b2b2b", )
        self.frame_producto10.grid(row=1, column=3,  padx=5,  pady=5, sticky="nsew")
        #
        self.frame_producto11 = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1_N2, fg_color="#2b2b2b", )
        self.frame_producto11.grid(row=2, column=2,  padx=5,  pady=5, sticky="nsew")
        #
        self.frame_producto12 = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1_N2, fg_color="#2b2b2b", )
        self.frame_producto12.grid(row=2, column=3,  padx=5,  pady=5, sticky="nsew")
        #
        self.frame_producto13 = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1_N2, fg_color="#2b2b2b", )
        self.frame_producto13.grid(row=3, column=2,  padx=5,  pady=5, sticky="nsew")
        #
        self.frame_producto14 = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1_N2, fg_color="#2b2b2b", )
        self.frame_producto14.grid(row=3, column=3,  padx=5,  pady=5, sticky="nsew")
        #
        self.frame_producto15 = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1_N2, fg_color="#2b2b2b", )
        self.frame_producto15.grid(row=4, column=2, padx=5,  pady=5, sticky="nsew")
        #
        self.frame_producto16 = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1_N2, fg_color="#2b2b2b", )
        self.frame_producto16.grid(row=4, column=3,  padx=5,  pady=5, sticky="nsew")
        #
        self.titulo_nuevo_producto_numeros = customtkinter.CTkLabel(self.frame_producto,
                                                        text="Informacion de cuantitativa del producto. Por favor, completa todos los campos presentes:")
        self.titulo_nuevo_producto_numeros.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        #
        self.precio_compra_nuevo_producto_numeros = customtkinter.CTkLabel(self.frame_producto1,
                                                        text="Digita el precio de compra del producto. Por unidad")
        self.precio_compra_nuevo_producto_numeros.grid(row=0, column=0, padx=5, pady=12, sticky="nsew")
        #
        self.precio_venta_nuevo_producto_numeros = customtkinter.CTkLabel(self.frame_producto3,
                                                        text="Digita el precio de venta para el producto. Por unidad")
        self.precio_venta_nuevo_producto_numeros.grid(row=0, column=0, padx=5, pady=12, sticky="nsew")
        #
        self.precio_venta_por_mayor_nuevo_producto_numeros = customtkinter.CTkLabel(self.frame_producto5,
                                                        text="Digita el precio de venta para el producto al por mayor. Por unidad")
        self.precio_venta_por_mayor_nuevo_producto_numeros.grid(row=0, column=0, padx=12, pady=12, sticky="nsew")
        #
        self.unidades_nuevo_producto_numeros = customtkinter.CTkLabel(self.frame_producto7,
                                                        text="Digita la cantidad de unidades compradas")
        self.unidades_nuevo_producto_numeros.grid(row=0, column=0, padx=5, pady=12, sticky="nsew")
        #
        self.fecha_compra_nuevo_producto_numeros = customtkinter.CTkLabel(self.frame_producto9,
                                                        text="Elige o escribe la fecha de compra del producto")
        self.fecha_compra_nuevo_producto_numeros.grid(row=0, column=0, padx=5, pady=12, sticky="nsew")
        #
        self.fecha_vencimiento_nuevo_producto_numeros = customtkinter.CTkLabel(self.frame_producto11,
                                                        text="Elige o escribe la fecha de compra del producto")
        self.fecha_vencimiento_nuevo_producto_numeros.grid(row=0, column=0, padx=5, pady=12, sticky="nsew")
        #
        self.fragilidad_nuevo_producto_numeros = customtkinter.CTkLabel(self.frame_producto13,
                                                        text="Elige el tipo de fragilidad acorde al producto")
        self.fragilidad_nuevo_producto_numeros.grid(row=0, column=0, padx=5, pady=12, sticky="nsew")
        #
        self.tipo_nuevo_producto_numeros = customtkinter.CTkLabel(self.frame_producto15,
                                                        text="Elige el tipo al que pertenece el producto ")
        self.tipo_nuevo_producto_numeros.grid(row=0, column=0, padx=5, pady=12, sticky="nsew")
        #
        self.precio_compra_nuevo_producto_numeros_entrada = customtkinter.CTkEntry(self.frame_producto2,
                                                        width=380, placeholder_text="Precio de compra producto")
        self.precio_compra_nuevo_producto_numeros_entrada.grid(row=0, column=0, padx=22, pady=12, sticky="nsew")
        PopupNumpad(self.precio_compra_nuevo_producto_numeros_entrada)
        self.herramienta_consejo_precio = CTkToolTip(self.precio_compra_nuevo_producto_numeros_entrada, message="Haz doble click para mostar el teclado por pantalla")
        #
        self.precio_venta_nuevo_producto_numeros_entrada = customtkinter.CTkEntry(self.frame_producto4,
                                                         width=380, placeholder_text="Precio de venta producto")
        self.precio_venta_nuevo_producto_numeros_entrada.grid(row=0, column=0, padx=22, pady=12, sticky="nsew")
        PopupNumpad(self.precio_venta_nuevo_producto_numeros_entrada)
        self.herramienta_consejo_precio = CTkToolTip(self.precio_venta_nuevo_producto_numeros_entrada, message="Haz doble click para mostar el teclado por pantalla")
        #
        self.precio_mayorista_nuevo_producto_numeros_entrada = customtkinter.CTkEntry(self.frame_producto6,
                                                         width=380, placeholder_text="Precio a mayorista del producto")
        self.precio_mayorista_nuevo_producto_numeros_entrada.grid(row=0, column=0, padx=22, pady=12, sticky="nsew")
        PopupNumpad(self.precio_mayorista_nuevo_producto_numeros_entrada)
        self.herramienta_consejo_precio = CTkToolTip(self.precio_mayorista_nuevo_producto_numeros_entrada, message="Haz doble click para mostar el teclado por pantalla")
        #
        self.unidades_nuevo_producto_numeros_entrada = frame_seleccion_nuemeros(self.frame_producto8, width=380, step_size=1)
        self.unidades_nuevo_producto_numeros_entrada.grid(row=0, column=0, padx=22, pady=12, sticky="nsew")
        #
        self.fecha_compra_nuevo_producto_numeros_entrada = customtkinter.CTkEntry(self.frame_producto10,
                                                            width=380, placeholder_text="AAAA-MM-DD")
        self.fecha_compra_nuevo_producto_numeros_entrada.grid(row=0, column=0, padx=22, pady=12, sticky="nsew")
        PopupNumpad(self.fecha_compra_nuevo_producto_numeros_entrada)
        self.herramienta_consejo_fecha = CTkToolTip(self.fecha_compra_nuevo_producto_numeros_entrada, message="Haz doble click para mostar el teclado por pantalla")
        #
        self.fecha_vencimiento_compra_nuevo_producto_numeros_entrada = customtkinter.CTkEntry(self.frame_producto12,
                                                                         width=380, placeholder_text="AAAA-MM-DD")
        self.fecha_vencimiento_compra_nuevo_producto_numeros_entrada.grid(row=0, column=0, padx=22, pady=12, sticky="nsew")
        PopupNumpad(self.fecha_vencimiento_compra_nuevo_producto_numeros_entrada)
        self.herramienta_consejo_fecha = CTkToolTip(self.fecha_vencimiento_compra_nuevo_producto_numeros_entrada, message="Haz doble click para mostar el teclado por pantalla")
        #
        self.valores_fragilidad = ["fragilidad 1","fragilidad 2","fragilidad 3","fragilidad 4","fragilidad 5","fragilidad 6"]
        self.fragilidad_compra_nuevo_producto_numeros_entrada = customtkinter.CTkComboBox(self.frame_producto14, width=380)
        self.fragilidad_compra_nuevo_producto_numeros_entrada.grid(row=0, column=0, padx=22, pady=12, sticky="nsew")
        self.fragilidad_compra_nuevo_producto_numeros_entrada.set("Seleciona / Escribe")
        CTkScrollableDropdown(self.fragilidad_compra_nuevo_producto_numeros_entrada, values=self.valores_fragilidad, justify="left", button_color="transparent")
        #4
        self.valores_tipo = ["tipo 1","tipo 2","tipo 3","tipo 4","tipo 5","tipo 6"]
        self.tipo_compra_nuevo_producto_numeros_entrada = customtkinter.CTkComboBox(self.frame_producto16, width=380)
        self.tipo_compra_nuevo_producto_numeros_entrada.grid(row=0, column=0, padx=22, pady=12, sticky="nsew")
        self.tipo_compra_nuevo_producto_numeros_entrada.set("Seleciona / Escribe")
        CTkScrollableDropdown(self.tipo_compra_nuevo_producto_numeros_entrada, values=self.valores_tipo, justify="left", button_color="transparent")
        #
        self.frame_producto_proveedor = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1_N3, fg_color="#2b2b2b", )
        self.frame_producto_proveedor.grid(row=0, column=0, columnspan=4, padx=5,  pady=5, sticky="nsew")
        #
        self.frame_producto1_proveedor = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1_N3, fg_color="#2b2b2b", )
        self.frame_producto1_proveedor.grid(row=1, column=0,  padx=5,  pady=5, sticky="nsew")
        #
        self.frame_producto2_proveedor = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1_N3, fg_color="#2b2b2b", )
        self.frame_producto2_proveedor.grid(row=1, column=1,  padx=5,  pady=5, sticky="nsew")
        #
        self.frame_producto3_proveedor = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1_N3, fg_color="#2b2b2b", )
        self.frame_producto3_proveedor.grid(row=2, column=0,  padx=5,  pady=5, sticky="nsew")
        #
        self.frame_producto4_proveedor = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1_N3, fg_color="#2b2b2b", )
        self.frame_producto4_proveedor.grid(row=2, column=1,  padx=5,  pady=5, sticky="nsew")
        #
        self.frame_producto5_proveedor = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1_N3, fg_color="#2b2b2b", )
        self.frame_producto5_proveedor.grid(row=3, column=0,  padx=5,  pady=5, sticky="nsew")
        #
        self.frame_producto6_proveedor = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1_N3, fg_color="#2b2b2b", )
        self.frame_producto6_proveedor.grid(row=3, column=1,  padx=5,  pady=5, sticky="nsew")
        #
        self.frame_producto7_proveedor = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1_N3, fg_color="#2b2b2b", )
        self.frame_producto7_proveedor.grid(row=4, column=0, padx=5,  pady=5, sticky="nsew")
        #
        self.frame_producto8_proveedor = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1_N3, fg_color="#2b2b2b", )
        self.frame_producto8_proveedor.grid(row=4, column=1,  padx=5,  pady=5, sticky="nsew")
        #
        self.frame_producto9_proveedor = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1_N3, fg_color="#2b2b2b", )
        self.frame_producto9_proveedor.grid(row=1, column=2,  padx=5,  pady=5, sticky="nsew")
        #
        self.frame_producto10_proveedor = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1_N3, fg_color="#2b2b2b", )
        self.frame_producto10_proveedor.grid(row=1, column=3,  padx=5,  pady=5, sticky="nsew")
        #
        self.frame_producto11_proveedor = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1_N3, fg_color="#2b2b2b", )
        self.frame_producto11_proveedor.grid(row=2, column=2,  padx=5,  pady=5, sticky="nsew")
        #
        self.frame_producto12_proveedor = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1_N3, fg_color="#2b2b2b", )
        self.frame_producto12_proveedor.grid(row=2, column=3,  padx=5,  pady=5, sticky="nsew")
        #
        self.frame_producto13_proveedor = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1_N3, fg_color="#2b2b2b", )
        self.frame_producto13_proveedor.grid(row=3, column=2,  padx=5,  pady=5, sticky="nsew")
        #
        self.frame_producto14_proveedor = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1_N3, fg_color="#2b2b2b", )
        self.frame_producto14_proveedor.grid(row=3, column=3,  padx=5,  pady=5, sticky="nsew")
        #
        self.frame_producto15_proveedor = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1_N3, fg_color="#2b2b2b", )
        self.frame_producto15_proveedor.grid(row=4, column=2, padx=5,  pady=5, sticky="nsew")
        #
        self.frame_producto16_proveedor = customtkinter.CTkFrame(master=self.frame_Menu_vacio_N1_N3, fg_color="#2b2b2b", )
        self.frame_producto16_proveedor.grid(row=4, column=3,  padx=5,  pady=5, sticky="nsew")
        #
        self.titulo_proveedores= customtkinter.CTkLabel(self.frame_producto_proveedor,
                                                        text="Informacion general sobre el proveedor. Por favor, Completa todos los campos presentes, de lo contrario.")
        self.titulo_proveedores.pack(side="left", padx=5, pady=5)
        #
        self.funcion_relleno_proveedores_label= customtkinter.CTkLabel(self.frame_producto_proveedor,
                                                        text="Selecciona un proveedor que haya sido registrado con anterioridad:")
        self.funcion_relleno_proveedores_label.pack(side="left", padx=(100,5), pady=5)
        #
        self.valores_proveedor = ["proveedor 1","proveedor 2","proveedor 3","proveedor 4","proveedor 5","proveedor 6"]
        self.funcion_relleno_proveedores= customtkinter.CTkComboBox(self.frame_producto_proveedor, width= 240)
        self.funcion_relleno_proveedores.pack(side="left", padx=5, pady=5)
        self.funcion_relleno_proveedores.set("Seleciona / Escribe")
        CTkScrollableDropdown(self.funcion_relleno_proveedores, values=self.valores_proveedor, justify="left", button_color="transparent")
        #
        #
        self.boton_anadir_proveedor = customtkinter.CTkButton(self.frame_producto_proveedor,
                                                          text="Añadir proveedor", command= lambda: self.obtener_datos_proveedor_nuevo())
        self.boton_anadir_proveedor.pack(side="left", padx=(200,5), pady=5)
        
        
        self.tipo_proveedores = customtkinter.CTkLabel(self.frame_producto1_proveedor,
                                                        text="Escribre el un nombre de conctacto de la empresa o proveedor:")
        self.tipo_proveedores.grid(row=0, column=0, padx=5, pady=12, sticky="nsew")
        #
        self.nombre_proveedores = customtkinter.CTkLabel(self.frame_producto3_proveedor,
                                                        text="Escribe el nombre del proveedor:")
        self.nombre_proveedores.grid(row=0, column=0, padx=5, pady=12, sticky="nsew")
        #
        self.telefono_proveedores = customtkinter.CTkLabel(self.frame_producto5_proveedor,
                                                        text="Digita el numero telefonico del proveedor:")
        self.telefono_proveedores.grid(row=0, column=0, padx=5, pady=12, sticky="nsew")
        #
        self.mail_proveedores = customtkinter.CTkLabel(self.frame_producto7_proveedor,
                                                        text="Escribre el correo electronico del proveedor:")
        self.mail_proveedores.grid(row=0, column=0, padx=5, pady=12, sticky="nsew")
        #
        self.nit_proveedores = customtkinter.CTkLabel(self.frame_producto9_proveedor,
                                                        text="Digita el NIT de la empresa del proveedor:")
        self.nit_proveedores.grid(row=0, column=0, padx=5, pady=12, sticky="nsew")
        #
        self.nombre_empresa_proveedores = customtkinter.CTkLabel(self.frame_producto11_proveedor,
                                                        text="Escribe la dirrecion del proveedor:")
        self.nombre_empresa_proveedores.grid(row=0, column=0, padx=5, pady=12, sticky="nsew")
        #
        self.web_empresa_proveedores = customtkinter.CTkLabel(self.frame_producto13_proveedor,
                                                        text="Escribe el nombre de la pagina web del proveedor:")
        self.web_empresa_proveedores.grid(row=0, column=0, padx=5, pady=12, sticky="nsew")
        #
        self.nota_empresa_proveedores = customtkinter.CTkLabel(self.frame_producto15_proveedor,
                                                        text="Espacio para notas adiccionales sobre el proveedor:")
        self.nota_empresa_proveedores.grid(row=0, column=0, padx=5, pady=12, sticky="nsew")
        #
        self.nombre_contacto_empresa_entrada = customtkinter.CTkEntry(self.frame_producto2_proveedor, width=380, placeholder_text="Nombre de contacto de la empresa")
        self.nombre_contacto_empresa_entrada .grid(row=0, column=0, padx=22, pady=12, sticky="nsew")
        #
        self.nombre_proveedores_entrada = customtkinter.CTkEntry(self.frame_producto4_proveedor,
                                                            width=380, placeholder_text="Nombre de la empresa")
        self.nombre_proveedores_entrada.grid(row=0, column=0, padx=22, pady=12, sticky="nsew")
        #
        self.telefono_proveedores_entrada = customtkinter.CTkEntry(self.frame_producto6_proveedor,
                                                            width=380, placeholder_text="Numero del proveedor")
        self.telefono_proveedores_entrada.grid(row=0, column=0, padx=22, pady=12, sticky="nsew")
        PopupNumpad(self.telefono_proveedores_entrada, x=1012, y=800)
        self.herramienta_consejo_telefono = CTkToolTip(self.telefono_proveedores_entrada, message="Haz doble click para mostar el teclado por pantalla")
        #
        self.mail_proveedores_entrada = customtkinter.CTkEntry(self.frame_producto8_proveedor,
                                                            width=380, placeholder_text="Correo del proveedor")
        self.mail_proveedores_entrada.grid(row=0, column=0, padx=22, pady=12, sticky="nsew")
        #
        self.nit_proveedores_entrada = customtkinter.CTkEntry(self.frame_producto10_proveedor,
                                                            width=380, placeholder_text="NIT de la empresa")
        self.nit_proveedores_entrada.grid(row=0, column=0, padx=22, pady=12, sticky="nsew")
        PopupNumpad(self.nit_proveedores_entrada)
        self.herramienta_consejo_nit = CTkToolTip(self.nit_proveedores_entrada, message="Haz doble click para mostar el teclado por pantalla")
        #
        self.dirrecion_empresa_proveedores_entrada = customtkinter.CTkEntry(self.frame_producto12_proveedor,
                                                            width=380, placeholder_text="Dirrecion de la empresa")
        self.dirrecion_empresa_proveedores_entrada.grid(row=0, column=0, padx=22, pady=12, sticky="nsew")
        #
        self.web_empresa_proveedores_entrada = customtkinter.CTkEntry(self.frame_producto14_proveedor,
                                                            width=380, placeholder_text="URL de la pagina web")
        self.web_empresa_proveedores_entrada.grid(row=0, column=0, padx=22, pady=12, sticky="nsew")
        #
        self.nota_empresa_proveedores = customtkinter.CTkEntry(self.frame_producto16_proveedor,
                                                            width=380, placeholder_text="Notas adiccionales")
        self.nota_empresa_proveedores.grid(row=0, column=0, padx=22, pady=12, sticky="nsew")
        #
      
        #Botones menu lateral:
        self.Menu_analitica_boton = customtkinter.CTkButton(self.frame_menu, height=40, border_spacing=10, text="Analitica",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   anchor="w", command=self.Menu_analitica_evento)
        self.Menu_analitica_boton.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        #
        self.Menu_contactos_boton = customtkinter.CTkButton(self.frame_menu,  height=40, border_spacing=10, text="Contactos",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   anchor="w", command=self.Menu_contactanos_evento)
        self.Menu_contactos_boton.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
        #
        self.Menu_inventario_boton = customtkinter.CTkButton(self.frame_menu,  height=40, border_spacing=10, text="Inventarios",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   anchor="w", command=self.Menu_inventario_evento)
        self.Menu_inventario_boton.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")
       
        self.Menu_ventas_boton = customtkinter.CTkButton(self.frame_menu,  height=40, border_spacing=10, text="Realizar venta",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   anchor="w", command=self.Menu_ventas_evento)
        self.Menu_ventas_boton.grid(row=6, column=0, padx=5, pady=5, sticky="nsew")
        #
        self.Menu_vacio_N1_boton = customtkinter.CTkButton(self.frame_menu,  height=40, border_spacing=10, text="Ingreso de datos",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   anchor="w", command=self.Menu_vacio_N1_evento)
        self.Menu_vacio_N1_boton.grid(row=7, column=0, padx=5, pady=5, sticky="nsew")
        
        #Labels menu arriba:
        self.titulo_app = customtkinter.CTkButton(self.frame_menu_parte_alta,  height=40, border_spacing=10, text="Titulo aplicacion",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   anchor="w", command=self)
        self.titulo_app.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
       
    
        # Ejecutamos las funciones necesarias:
        self.Mostrar_menu_seleccionado("Menu_inicio")
        self.generar_visualizacion_db()
        self.generar_visualizacion_proveedores()
        self.generar_visualizacion_db_selecionados()
        self.generar_visualizacion_db_inventario()
        self.create_graphics()
    
    def Mostrar_menu_seleccionado(self, name):
        # set button color for selected button
        self.Menu_analitica_boton.configure(fg_color=("gray75", "gray25") if name == "Menu_analitica" else "transparent")
        self.Menu_contactos_boton.configure(fg_color=("gray75", "gray25") if name == "Menu_contactanos" else "transparent")
        self.Menu_inventario_boton.configure(fg_color=("gray75", "gray25") if name == "Menu_inventario" else "transparent")
        self.Menu_ventas_boton.configure(fg_color=("gray75", "gray25") if name == "Menu_ventas" else "transparent")
        self.Menu_vacio_N1_boton.configure(fg_color=("gray75", "gray25") if name == "Menu_vacio_N1" else "transparent")
        
        
        # show selected frame
        if name == "Menu_analitica":
            self.frame_Menu_analitica.grid(row=0, column=0, columnspan= 2, rowspan=2,  sticky="nsew")
        else:
            self.frame_Menu_analitica.grid_forget()
        if name == "Menu_contactanos":
            self.frame_Menu_contactos.grid(row=0, column=0, columnspan= 2, rowspan=2,  sticky="nsew")
        else:
            self.frame_Menu_contactos.grid_forget()
        if name == "Menu_inventario":
            self.frame_Menu_inventario.grid(row=0, column=0, columnspan= 2, rowspan=2,  sticky="nsew")
        else:
            self.frame_Menu_inventario.grid_forget()
        if name == "Menu_ventas":
            self.frame_Menu_ventas.grid(row=0, column=0, columnspan= 2, rowspan=2,  sticky="nsew")
        else:
            self.frame_Menu_ventas.grid_forget()
        if name == "Menu_vacio_N1":
            self.frame_Menu_vacio_N1.grid(row=0, column=0, columnspan= 2, rowspan=2,  sticky="nsew")
        else:
            self.frame_Menu_vacio_N1.grid_forget()    
                              
    def Menu_inicio_evento(self):
        self.Mostrar_menu_seleccionado("Menu_inicio")

    def Menu_analitica_evento(self):
        self.Mostrar_menu_seleccionado("Menu_analitica")

    def Menu_contactanos_evento(self):
        self.Mostrar_menu_seleccionado("Menu_contactanos")
    
    def Menu_inventario_evento(self):
        self.Mostrar_menu_seleccionado("Menu_inventario")

    def Menu_catalogo_evento(self):
        self.Mostrar_menu_seleccionado("Menu_catalogo")

    def Menu_tiendas_evento(self):
        self.Mostrar_menu_seleccionado("Menu_tiendas")
        
    def Menu_ventas_evento(self):
        self.Mostrar_menu_seleccionado("Menu_ventas")

    def Menu_vacio_N1_evento(self):
        self.Mostrar_menu_seleccionado("Menu_vacio_N1")

    def obtener_datos_producto_nuevo(self):
        # Obtener datos de la GUI
        nombre_obtenido = self.nombre_nuevo_producto_entrada.get()
        codigo_obtenido = self.codigo_nuevo_producto_entrada.get()
        descripcion_obtenido = self.descripcion_nuevo_producto_entrada.get()
        categoria_obtenido = self.categoria_nuevo_producto_entrada.get()
        marca_obtenido = self.marca_nuevo_producto_entrada.get()
        precio_compra_obtenido = self.precio_compra_nuevo_producto_numeros_entrada.get()
        precio_venta_obtenido = self.precio_venta_nuevo_producto_numeros_entrada.get()
        precio_mayorista_obtenido = self.precio_mayorista_nuevo_producto_numeros_entrada.get()
        cantidad_unidades_obtenido = self.unidades_nuevo_producto_numeros_entrada.get()
        temporada_producto_obtenido = self.temporada_nuevo_producto_entrada.get()
        fecha_adquisicion = self.fecha_compra_nuevo_producto_numeros_entrada.get()
        fecha_vencimiento = self.fecha_vencimiento_compra_nuevo_producto_numeros_entrada.get()
        fecha_adquisicion_obtenido = datetime.strptime(fecha_adquisicion, "%Y/%m/%d")
        fecha_vencimiento_obtenido = datetime.strptime(fecha_vencimiento, "%Y/%m/%d")
        fragilidad_obtenido = self.fragilidad_compra_nuevo_producto_numeros_entrada.get()
        tipo_producto_obtenido = self.tipo_compra_nuevo_producto_numeros_entrada.get()
        estado_obtenido = self.tienda_nuevo_producto_entrada.get()

        # Validar campos obligatorios
        if not nombre_obtenido or not codigo_obtenido or not precio_compra_obtenido or not precio_venta_obtenido:
            messagebox.showerror("Error", "Los campos obligatorios no pueden estar en blanco.")
            return

        # Validar que los campos numéricos sean del tipo correcto
        try:
            codigo_obtenido = int(codigo_obtenido)
            precio_compra_obtenido = float(precio_compra_obtenido)
            precio_venta_obtenido = float(precio_venta_obtenido)
            precio_mayorista_obtenido = float(precio_mayorista_obtenido)
            cantidad_unidades_obtenido = int(cantidad_unidades_obtenido)
            proveedor_id_obtenido = self.obtener_id_proveedor_por_nombre()
        except ValueError:
            messagebox.showerror("Error", "Los campos numéricos deben ser números válidos.")
            return
        
        # Agregar el producto y el proveedor en la base de datos
        agregar_producto(
            nombre_obtenido,
            codigo_obtenido,
            descripcion_obtenido,
            categoria_obtenido,
            marca_obtenido,
            precio_compra_obtenido,
            precio_venta_obtenido,
            precio_mayorista_obtenido,
            cantidad_unidades_obtenido,
            temporada_producto_obtenido,
            fecha_adquisicion_obtenido,
            fecha_vencimiento_obtenido,
            fragilidad_obtenido,
            tipo_producto_obtenido,
            proveedor_id_obtenido,
            estado_obtenido
        )

    def obtener_datos_proveedor_nuevo(self):
        #Obtener datos del proveedor GUI        
        nombre_contacto_obtenido = self.nombre_contacto_empresa_entrada.get()
        nombre_empresa_obtenido = self.nombre_proveedores_entrada.get()
        numero_proveedor_obtenido = self.telefono_proveedores_entrada.get()
        correo_proveedor_obtenido = self.mail_proveedores_entrada.get()
        nit_empresa_obtenido = self.nit_proveedores_entrada.get()
        pagina_web_obtenido = self.web_empresa_proveedores_entrada.get()
        direccion_empresa_obtenido = self.dirrecion_empresa_proveedores_entrada.get()
        notas_adicionales_obtenido = self.nota_empresa_proveedores.get()
        
        
        # Validar campos obligatorios
        if not nombre_contacto_obtenido or not nombre_empresa_obtenido or not numero_proveedor_obtenido or not correo_proveedor_obtenido:
            messagebox.showerror("Error", "Los campos obligatorios no pueden estar en blanco.")
            return
        
        
        # Validar que los campos numéricos sean del tipo correcto
        try:
            numero_proveedor_obtenido = int(numero_proveedor_obtenido)
            nit_empresa_obtenido = int(nit_empresa_obtenido)
        except ValueError:
            return

        # Agregar el proveedor en la base de dato
        agregar_proveedor(
            nombre_contacto_obtenido,
            nombre_empresa_obtenido,
            numero_proveedor_obtenido,
            correo_proveedor_obtenido,
            nit_empresa_obtenido,
            pagina_web_obtenido,
            direccion_empresa_obtenido,
            notas_adicionales_obtenido
        )
        
    def obtener_id_proveedor_por_nombre(self, nombre_empresa):
        try:
            # Realiza una consulta para buscar el proveedor por nombre de empresa
            proveedor = session.query(Proveedor).filter_by(nombre_empresa=nombre_empresa).first()

            if proveedor:
                # Si se encuentra un proveedor con ese nombre de empresa, devuelve su ID
                return proveedor.id
            else:
                # Si no se encuentra un proveedor con ese nombre de empresa, devuelve None o un valor indicativo
                return None
        except Exception as e:
            print(f"Error al buscar proveedor: {e}")
            return None
    
    def generar_visualizacion_proveedores(self):
        # Configuración de colores y estilos para el Treeview
        bg_color = self.frame_Menu_contactos_base._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"])
        text_color = self.frame_Menu_contactos_base._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkLabel"]["text_color"])
        selected_color = self.frame_Menu_contactos_base._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkButton"]["fg_color"])
        
        treestyle = ttk.Style()
        treestyle.theme_use('default')
        treestyle.configure("Treeview", background=bg_color, foreground=text_color, fieldbackground=bg_color, borderwidth=0 , rowheight=40)
        treestyle.map('Treeview', background=[('selected', bg_color)], foreground=[('selected', selected_color)])
        
        # Extraemos la data de la tabla de proveedores usando SQLAlchemy
        datos_proveedores = session.query(Proveedor).all()
        print(datos_proveedores)
        
        # Crear el Treeview
        self.treeview_proveedores = ttk.Treeview(self.frame_Menu_contactos_base, columns=(
            "ID", "Nombre Contacto", "Nombre Empresa", "Número Proveedor", 
            "Correo Proveedor", "NIT Empresa", "Página Web", "Dirección Empresa", 
            "Notas Adicionales"
        ), show="headings")

        # Configurar los encabezados de las columnas
        self.treeview_proveedores.heading("ID", text="ID")
        self.treeview_proveedores.heading("Nombre Contacto", text="Nombre Contacto")
        self.treeview_proveedores.heading("Nombre Empresa", text="Nombre Empresa")
        self.treeview_proveedores.heading("Número Proveedor", text="Número Proveedor")
        self.treeview_proveedores.heading("Correo Proveedor", text="Correo Proveedor")
        self.treeview_proveedores.heading("NIT Empresa", text="NIT Empresa")
        self.treeview_proveedores.heading("Página Web", text="Página Web")
        self.treeview_proveedores.heading("Dirección Empresa", text="Dirección Empresa")
        self.treeview_proveedores.heading("Notas Adicionales", text="Notas Adicionales")

        # Limpiar cualquier dato previo en el Treeview
        for fila in self.treeview_proveedores.get_children():
            self.treeview_proveedores.delete(fila)

        # Llenar el Treeview con los datos de los proveedores
        for proveedor in datos_proveedores:
            valores = (
                proveedor.id,
                proveedor.nombre_contacto,
                proveedor.nombre_empresa,
                proveedor.numero_proveedor,
                proveedor.correo_proveedor,
                proveedor.nit_empresa,
                proveedor.pagina_web,
                proveedor.direccion_empresa,
                proveedor.notas_adicionales
            )
            self.treeview_proveedores.insert("", "end", values=valores)    
            
        # Establecer anchos específicos para cada columna (en píxeles)
        self.treeview_proveedores.column("ID", width=25,  anchor="center")
        self.treeview_proveedores.column("Nombre Contacto", width=160, anchor="center")
        self.treeview_proveedores.column("Nombre Empresa", width=160, anchor="center")
        self.treeview_proveedores.column("Número Proveedor", width=120, anchor="center")
        self.treeview_proveedores.column("Correo Proveedor", width=200, anchor="center")
        self.treeview_proveedores.column("NIT Empresa", width=120, anchor="center")
        self.treeview_proveedores.column("Página Web", width=150, anchor="center")
        self.treeview_proveedores.column("Dirección Empresa", width=400, anchor="center")
        self.treeview_proveedores.column("Notas Adicionales", width=600, anchor="center")
        
        # Empacar el Treeview
        self.treeview_proveedores.pack(fill="both", expand=True)

    def create_graphics(self):
        # Gráfica 1: Stock de productos por categoría
        categorias_stock = session.query(Producto.categoria, func.sum(Producto.cantidad_unidades)).group_by(Producto.categoria).all()
        if categorias_stock:
            categorias, stock_por_categoria = zip(*categorias_stock)
            fig1, ax1 = plt.subplots(figsize=(16, 5))
            ax1.bar(categorias, stock_por_categoria, color='skyblue')
            ax1.set_title('Stock de Productos por Categoría')
            ax1.set_xlabel('Categoría')
            ax1.set_ylabel('Cantidad en Stock')
            ax1.grid(True)
            self.display_graph(fig1, self.frame_Menu_analitica_N1)
        else:
            print("No hay datos para la gráfica de stock por categoría")

        # Gráfica 2: Precios de productos por tipo
        tipos_precios = session.query(Producto.tipo_producto, func.avg(Producto.precio_venta)).group_by(Producto.tipo_producto).all()
        if tipos_precios:
            tipos, precios_promedio = zip(*tipos_precios)
            fig2, ax2 = plt.subplots(figsize=(16, 5))
            ax2.bar(tipos, precios_promedio, color='lightcoral')
            ax2.set_title('Precios Promedio de Productos por Tipo')
            ax2.set_xlabel('Tipo de Producto')
            ax2.set_ylabel('Precio Promedio')
            ax2.grid(True)
            self.display_graph(fig2, self.frame_Menu_analitica_N2)
        else:
            print("No hay datos para la gráfica de precios por tipo")

        # Gráfica 3: Ventas totales por producto
        productos_ventas = session.query(Producto.id, func.sum(ProductoVendido.cantidad * ProductoVendido.precio_venta_unitario)).join(ProductoVendido, Producto.id == ProductoVendido.producto_id).group_by(Producto.id).all()
        if productos_ventas:
            ids_productos, ventas_totales = zip(*productos_ventas)
            fig3, ax3 = plt.subplots(figsize=(16, 5))
            ax3.bar(ids_productos, ventas_totales, color='seagreen')
            ax3.set_title('Ventas Totales por Producto')
            ax3.set_xlabel('ID Producto')
            ax3.set_ylabel('Ventas Totales')
            ax3.grid(True)
            self.display_graph(fig3, self.frame_Menu_analitica_N3)
        else:
            print("No hay datos para la gráfica de ventas totales por producto")

        # Gráfica 4: Precio de compra vs. precio de venta por producto
        productos_precios = session.query(Producto.nombre, Producto.precio_compra, Producto.precio_venta).all()
        if productos_precios:
            nombres, precios_compra, precios_venta = zip(*productos_precios)
            fig4, ax4 = plt.subplots(figsize=(20, 5))
            ax4.plot(nombres, precios_compra, 'o-', label='Precio de Compra', color='orange')
            ax4.plot(nombres, precios_venta, 's-', label='Precio de Venta', color='purple')
            ax4.set_title('Precio de Compra vs. Precio de Venta por Producto')
            ax4.set_xlabel('Nombre del Producto')
            ax4.set_ylabel('Precio')
            ax4.legend()
            ax4.grid(True)
            ax4.tick_params(axis='x', rotation=90)
            self.display_graph(fig4, self.frame_Menu_analitica_N4)
        else:
            print("No hay datos para la gráfica de precios de compra vs. precios de venta")


    def display_graph(self, fig, frame):
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def generar_visualizacion_db(self):
        
        # Configuración de colores y estilos para el Treeview
        bg_color = self.frame_database_scroll._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"])
        text_color = self.frame_database_scroll._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkLabel"]["text_color"])
        selected_color = self.frame_database_scroll._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkButton"]["fg_color"])
        
        
        treestyle = ttk.Style()
        treestyle.theme_use('default')
        treestyle.configure("Treeview", background=bg_color, foreground=text_color, fieldbackground=bg_color, borderwidth=0 , rowheight=35)
        treestyle.map('Treeview', background=[('selected', bg_color)], foreground=[('selected', selected_color)])
        
        # Extraemos la data de la tabla de productos usando SQLAlchemy
        datos = session.query(Producto).all()
        
        # Crear el Treeview
        self.treeview = ttk.Treeview(self.frame_database_scroll, columns=(
            "ID", "Nombre", "Código", "Descripción", "Categoría",
            "Marca", "Precio Compra", "Precio Venta", "Precio Mayorista",
            "Cantidad Unidades", "Temporada Producto", "Fecha Adquisición",
            "Fecha Vencimiento", "Fragilidad", "Tipo Producto", "Proveedor ID",
            "Estado"
        ), show="headings")

        # Configurar los encabezados de las columnas
        self.treeview.heading("ID", text="ID")
        self.treeview.heading("Nombre", text="Nombre")
        self.treeview.heading("Código", text="Código")
        self.treeview.heading("Descripción", text="Descripción")
        self.treeview.heading("Categoría", text="Categoría")
        self.treeview.heading("Marca", text="Marca")
        self.treeview.heading("Precio Compra", text="Precio Compra")
        self.treeview.heading("Precio Venta", text="Precio Venta")
        self.treeview.heading("Precio Mayorista", text="Precio Mayorista")
        self.treeview.heading("Cantidad Unidades", text="Cantidad Unidades")
        self.treeview.heading("Temporada Producto", text="Temporada Producto")
        self.treeview.heading("Fecha Adquisición", text="Fecha Adquisición")
        self.treeview.heading("Fecha Vencimiento", text="Fecha Vencimiento")
        self.treeview.heading("Fragilidad", text="Fragilidad")
        self.treeview.heading("Tipo Producto", text="Tipo Producto")
        self.treeview.heading("Proveedor ID", text="Proveedor ID")
        self.treeview.heading("Estado", text="Estado")

        # Limpiar cualquier dato previo en el Treeview
        for fila in self.treeview.get_children():
            self.treeview.delete(fila)

        # Llenar el Treeview con los datos
        for dato in datos:
            # Crear una tupla con los atributos del objeto Producto en el orden deseado
            valores = (
                dato.id,
                dato.nombre,
                dato.codigo,
                dato.descripcion,
                dato.categoria,
                dato.marca,
                dato.precio_compra,
                dato.precio_venta,
                dato.precio_mayorista,
                dato.cantidad_unidades,
                dato.temporada_producto,
                dato.fecha_adquisicion,  
                dato.fecha_vencimiento,  
                dato.fragilidad,
                dato.tipo_producto,
                dato.proveedor_id,
                dato.estado
            )
            self.treeview.insert("", "end", values=valores)    
        
        # Establecer anchos específicos para cada columna (en píxeles)
        self.treeview.column("ID", width=25, anchor="center")
        self.treeview.column("Nombre", width=160, anchor="center")
        self.treeview.column("Código", width=90, anchor="center")
        self.treeview.column("Descripción", width=200, anchor="center")
        self.treeview.column("Categoría", width=90, anchor="center")
        self.treeview.column("Marca", width=90, anchor="center")
        self.treeview.column("Precio Compra", width=100, anchor="center")
        self.treeview.column("Precio Venta", width=100, anchor="center")
        self.treeview.column("Precio Mayorista", width=100, anchor="center")
        self.treeview.column("Cantidad Unidades", width=110, anchor="center")
        self.treeview.column("Temporada Producto", width=120, anchor="center")
        self.treeview.column("Fecha Adquisición", width=110, anchor="center")
        self.treeview.column("Fecha Vencimiento", width=110, anchor="center")
        self.treeview.column("Fragilidad", width=100, anchor="center")
        self.treeview.column("Tipo Producto", width=100, anchor="center")
        self.treeview.column("Proveedor ID", width=100, anchor="center")
        self.treeview.column("Estado", width=70, anchor="center")
        
        # Empacar el Treeview
        self.treeview.pack(fill="both", expand=True)
    
    def generar_visualizacion_db_inventario(self):
        
        # Configuración de colores y estilos para el Treeview
        bg_color = self.frame_database_scroll._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"])
        text_color = self.frame_database_scroll._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkLabel"]["text_color"])
        selected_color = self.frame_database_scroll._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkButton"]["fg_color"])
        
        
        treestyle = ttk.Style()
        treestyle.theme_use('default')
        treestyle.configure("Treeview", background=bg_color, foreground=text_color, fieldbackground=bg_color, borderwidth=0 , rowheight=35)
        treestyle.map('Treeview', background=[('selected', bg_color)], foreground=[('selected', selected_color)])
        
        # Extraemos la data de la tabla de productos usando SQLAlchemy
        datos = session.query(Producto).all()
        
        # Crear el Treeview
        self.treeview_inventario = ttk.Treeview(self.frame_Menu_inventario_N1, columns=(
            "ID", "Nombre", "Código", "Descripción", "Categoría",
            "Marca", "Precio Compra", "Precio Venta", "Precio Mayorista",
            "Cantidad Unidades", "Temporada Producto", "Fecha Adquisición",
            "Fecha Vencimiento", "Fragilidad", "Tipo Producto", "Proveedor ID",
            "Estado"
        ), show="headings")

        # Configurar los encabezados de las columnas
        self.treeview_inventario.heading("ID", text="ID")
        self.treeview_inventario.heading("Nombre", text="Nombre")
        self.treeview_inventario.heading("Código", text="Código")
        self.treeview_inventario.heading("Descripción", text="Descripción")
        self.treeview_inventario.heading("Categoría", text="Categoría")
        self.treeview_inventario.heading("Marca", text="Marca")
        self.treeview_inventario.heading("Precio Compra", text="Precio Compra")
        self.treeview_inventario.heading("Precio Venta", text="Precio Venta")
        self.treeview_inventario.heading("Precio Mayorista", text="Precio Mayorista")
        self.treeview_inventario.heading("Cantidad Unidades", text="Cantidad Unidades")
        self.treeview_inventario.heading("Temporada Producto", text="Temporada Producto")
        self.treeview_inventario.heading("Fecha Adquisición", text="Fecha Adquisición")
        self.treeview_inventario.heading("Fecha Vencimiento", text="Fecha Vencimiento")
        self.treeview_inventario.heading("Fragilidad", text="Fragilidad")
        self.treeview_inventario.heading("Tipo Producto", text="Tipo Producto")
        self.treeview_inventario.heading("Proveedor ID", text="Proveedor ID")
        self.treeview_inventario.heading("Estado", text="Estado")

        # Limpiar cualquier dato previo en el Treeview
        for fila in self.treeview_inventario.get_children():
            self.treeview_inventario.delete(fila)

        # Llenar el Treeview con los datos
        for dato in datos:
            # Crear una tupla con los atributos del objeto Producto en el orden deseado
            valores = (
                dato.id,
                dato.nombre,
                dato.codigo,
                dato.descripcion,
                dato.categoria,
                dato.marca,
                dato.precio_compra,
                dato.precio_venta,
                dato.precio_mayorista,
                dato.cantidad_unidades,
                dato.temporada_producto,
                dato.fecha_adquisicion,  
                dato.fecha_vencimiento,  
                dato.fragilidad,
                dato.tipo_producto,
                dato.proveedor_id,
                dato.estado
            )
            self.treeview_inventario.insert("", "end", values=valores)    
        
        # Establecer anchos específicos para cada columna (en píxeles)
        self.treeview_inventario.column("ID", width=25, anchor="center")
        self.treeview_inventario.column("Nombre", width=160, anchor="center")
        self.treeview_inventario.column("Código", width=90, anchor="center")
        self.treeview_inventario.column("Descripción", width=200, anchor="center")
        self.treeview_inventario.column("Categoría", width=90, anchor="center")
        self.treeview_inventario.column("Marca", width=90, anchor="center")
        self.treeview_inventario.column("Precio Compra", width=100, anchor="center")
        self.treeview_inventario.column("Precio Venta", width=100, anchor="center")
        self.treeview_inventario.column("Precio Mayorista", width=100, anchor="center")
        self.treeview_inventario.column("Cantidad Unidades", width=110, anchor="center")
        self.treeview_inventario.column("Temporada Producto", width=120, anchor="center")
        self.treeview_inventario.column("Fecha Adquisición", width=110, anchor="center")
        self.treeview_inventario.column("Fecha Vencimiento", width=110, anchor="center")
        self.treeview_inventario.column("Fragilidad", width=100, anchor="center")
        self.treeview_inventario.column("Tipo Producto", width=100, anchor="center")
        self.treeview_inventario.column("Proveedor ID", width=100, anchor="center")
        self.treeview_inventario.column("Estado", width=70, anchor="center")
        
        # Empacar el Treeview
        self.treeview_inventario.pack(fill="both", expand=True)
    
    
    def filtrar_por_codigo(self):
        try:
            #Obtenemos el codigo del entry
            codigo_sin_verificar = self.busqueda_data_base_codigo.get()
            
            if codigo_sin_verificar == "":
                self.filtrar_por_nombre()
                return
            else:
                self.busqueda_data_base_codigo.delete(0, customtkinter.END)
                codigo = int (codigo_sin_verificar)
                
                # Limpiar cualquier dato previo en el Treeview
                for fila in self.treeview.get_children():
                    self.treeview.delete(fila)
                
                # Extraer la data de la tabla de productos usando SQLAlchemy
                datos = session.query(Producto).filter(Producto.codigo == codigo).all()
                
                # Llenar el Treeview con los datos filtrados
                for dato in datos:
                    # Crear una tupla con los atributos del objeto Producto en el orden deseado
                    valores = (
                        dato.id,
                        dato.nombre,
                        dato.codigo,
                        dato.descripcion,
                        dato.categoria,
                        dato.marca,
                        dato.precio_compra,
                        dato.precio_venta,
                        dato.precio_mayorista,
                        dato.cantidad_unidades,
                        dato.temporada_producto,
                        dato.fecha_adquisicion,  
                        dato.fecha_vencimiento,  
                        dato.fragilidad,
                        dato.tipo_producto,
                        dato.proveedor_id,
                        dato.estado
                    )
                    self.treeview.insert("", "end", values=valores)
        except Exception as e:
            print(e)
    
    def filtrar_por_nombre(self):
        try:
            #Obtenemos el codigo del entry
            nombre = self.busqueda_data_base_nombre.get()
            
            if nombre == "":
                return
            else:
                self.busqueda_data_base_nombre.delete(0, customtkinter.END)
            
                # Limpiar cualquier dato previo en el Treeview
                for fila in self.treeview.get_children():
                    self.treeview.delete(fila)
                
                # Extraer la data de la tabla de productos usando SQLAlchemy
                datos = session.query(Producto).filter(Producto.nombre == nombre).all()
                
                # Llenar el Treeview con los datos filtrados
                for dato in datos:
                    # Crear una tupla con los atributos del objeto Producto en el orden deseado
                    valores = (
                        dato.id,
                        dato.nombre,
                        dato.codigo,
                        dato.descripcion,
                        dato.categoria,
                        dato.marca,
                        dato.precio_compra,
                        dato.precio_venta,
                        dato.precio_mayorista,
                        dato.cantidad_unidades,
                        dato.temporada_producto,
                        dato.fecha_adquisicion,  
                        dato.fecha_vencimiento,  
                        dato.fragilidad,
                        dato.tipo_producto,
                        dato.proveedor_id,
                        dato.estado
                    )
                    self.treeview.insert("", "end", values=valores)
        except Exception as e:
            print(e)
    
    def reestablecer_todos_los_datos(self):
        # Limpiar cualquier dato previo en el Treeview
        for fila in self.treeview.get_children():
            self.treeview.delete(fila)
        
        # Extraer la data de la tabla de productos usando SQLAlchemy
        datos = session.query(Producto).all()
        
        # Llenar el Treeview con los datos
        for dato in datos:
            # Crear una tupla con los atributos del objeto Producto en el orden deseado
            valores = (
                dato.id,
                dato.nombre,
                dato.codigo,
                dato.descripcion,
                dato.categoria,
                dato.marca,
                dato.precio_compra,
                dato.precio_venta,
                dato.precio_mayorista,
                dato.cantidad_unidades,
                dato.temporada_producto,
                dato.fecha_adquisicion,  
                dato.fecha_vencimiento,  
                dato.fragilidad,
                dato.tipo_producto,
                dato.proveedor_id,
                dato.estado
            )
            self.treeview.insert("", "end", values=valores)

    def obtener_elemento_seleccionado(self):
        try:
            # Obtener la lista de identificadores de filas seleccionadas
            seleccion = self.treeview.selection()
            unidades = self.cantidad_de_productos_entrada.get()
            descuento = self.descuento_de_productos_entrada.get()
            tipo_precio = self.tipo_de_precio_entrada.get()
            print(seleccion)
            if seleccion:
                # Tomar el primer elemento seleccionado (asumiendo selección única)
                fila_seleccionada = seleccion[0]
                
                # Obtener los valores de la fila seleccionada
                valores = self.treeview.item(fila_seleccionada, "values")        
            else:
                print("fallo en la selecion")
                return
            
            if valores:
                # Acceder a valores específicos en la tupla
                codigo_producto = valores[2]  
                nombre_producto = valores[1]
                id_producto = valores[0]
                
                if tipo_precio == "Normal":
                    precio_venta = valores[7]
                else:

                    #Precio para mayorista
                    precio_venta = valores[8]
            else:
                return
        
            if not valores or not unidades:
                return
            else:
                agregar_producto_seleccionado(
                    id_producto,
                    unidades,
                    tipo_precio,
                    precio_venta, 
                    nombre_producto,
                    codigo_producto,
                    descuento
                )
                
                #Restauramos los valores:
                self.cantidad_de_productos_entrada.set(0.0)
                self.descuento_de_productos_entrada.set(0.0)
                self.tipo_de_precio_entrada.set("Normal")
                #Actulizamos la visualizacion
                self.actualizar_datos_db_selecionados()
        except Exception as e:
            print(e)
        
    def generar_visualizacion_db_selecionados(self):
        # Configuración de colores y estilos para el Treeview
        bg_color = self.frame_2_scroll._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"])
        text_color = self.frame_2_scroll._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkLabel"]["text_color"])
        selected_color = self.frame_2_scroll._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkButton"]["fg_color"])
        
        
        treestyle = ttk.Style()
        treestyle.theme_use('default')
        treestyle.configure("Treeview", background=bg_color, foreground=text_color, fieldbackground=bg_color, borderwidth=0)
        treestyle.map('Treeview', background=[('selected', bg_color)], foreground=[('selected', selected_color)])
        
        # Extraemos la data de la tabla de productos usando SQLAlchemy
        datos = session.query(ProductoSelecionado).all()
        
        # Crear el Treeview
        self.treeview_seleccionados = ttk.Treeview(self.frame_2_scroll, columns=("ID", "Producto", "Codigo", "Unidades",
                                                        "Tipo precio", "Precio venta", "Descuento"), show="headings")
        
         # Configurar los encabezados de las columnas en el nuevo orden
        self.treeview_seleccionados.heading("ID", text="ID")
        self.treeview_seleccionados.heading("Producto", text="Producto")
        self.treeview_seleccionados.heading("Codigo", text="Codigo")
        self.treeview_seleccionados.heading("Unidades", text="Unidades")
        self.treeview_seleccionados.heading("Tipo precio", text="Tipo precio")
        self.treeview_seleccionados.heading("Precio venta", text="Precio venta")
        self.treeview_seleccionados.heading("Descuento", text="Descuento")
        
        # Limpiar cualquier dato previo en el Treeview
        for fila in self.treeview_seleccionados.get_children():
            self.treeview_seleccionados_seleccionados.delete(fila)
            
        for dato in datos:
            # Crear una tupla con los atributos del objeto Producto en el nuevo orden deseado
            valores = (
                dato.producto_id,
                dato.nombre,
                dato.codigo,
                dato.cantidad_unidades,
                dato.tipo_precio,
                dato.precio_venta,
                dato.descuento,
            )
            self.treeview_seleccionados.insert("", "end", values=valores) 

        # Configurar ancho y alineación para cada columna
        self.treeview_seleccionados.column("ID", width=20, anchor="center")
        self.treeview_seleccionados.column("Producto", width=150, anchor="w") 
        self.treeview_seleccionados.column("Codigo", width=55, anchor="center")
        self.treeview_seleccionados.column("Unidades", width=55, anchor="center")
        self.treeview_seleccionados.column("Tipo precio", width=70, anchor="center")
        self.treeview_seleccionados.column("Precio venta", width=70, anchor="center")
        self.treeview_seleccionados.column("Descuento", width=60, anchor="center")
        
        # Empacar el Treeview
        self.treeview_seleccionados.pack(fill="both", expand=True)
        
    def actualizar_datos_db_selecionados(self):
        # Limpiar cualquier dato previo en el Treeview
        for fila in self.treeview_seleccionados.get_children():
            self.treeview_seleccionados.delete(fila)
        
        # Extraer la data de la tabla de productos usando SQLAlchemy
        datos = session.query(ProductoSelecionado).all()
        
        # Llenar el Treeview con los datos
        for dato in datos:
            # Crear una tupla con los atributos del objeto Producto en el nuevo orden deseado
            valores = (
                dato.producto_id,
                dato.nombre,
                dato.codigo,
                dato.cantidad_unidades,
                dato.tipo_precio,
                dato.precio_venta,
                dato.descuento,
            )
            self.treeview_seleccionados.insert("", "end", values=valores)
    
    def eliminar_elemento_seleccionado(self):
        try:
            # Obtener la lista de identificadores de filas seleccionadas
            seleccion_eliminar = self.treeview_seleccionados.selection()
            
            if seleccion_eliminar:
                # Tomar el primer elemento seleccionado (asumiendo selección única)
                fila_seleccionada = seleccion_eliminar[0]
                
                # Obtener los valores de la fila seleccionada
                valores = self.treeview_seleccionados.item(fila_seleccionada, "values")        
            else:
                print("Fallo en la selección")
                return
            
            if valores:
                # Acceder a valores específicos en la tupla
                id_producto = valores[0]
                
                # Eliminar el elemento seleccionado de la base de datos (código para eliminarlo depende de cómo esté implementada tu base de datos)
                eliminar_producto_por_id(id_producto)
                
                # Eliminar el elemento seleccionado del Treeview
                self.treeview_seleccionados.delete(fila_seleccionada)
                #Actulizar la visualiacion
                self.actualizar_datos_db_selecionados()
            else:
                return
        except Exception as e:
            print(e)

    def crear_factura(self):
        # Crear una lista para almacenar los elementos seleccionados
        productos_seleccionados = []
        try:            
            seleccion = self.treeview_seleccionados.get_children()
            if seleccion:
                for fila in self.treeview_seleccionados.get_children():
                    self.treeview_seleccionados.delete(fila)
                for fila_seleccionada in seleccion:
                    valores = self.treeview_seleccionados.item(fila_seleccionada, "values")

                    if valores:
                        producto_id_srt = valores[0]
                        producto_id = int(producto_id_srt)
                        nombre_producto = valores[1]
                        codigo_producto = valores[2]
                        numero_unidades_str = valores[3]
                        numero_unidades =float(numero_unidades_str)
                        cantidad = int(numero_unidades_str)
                        tipo_precio = valores[4]
                        precio_str = valores[5]
                        precio = float(precio_str)
                        descuento_str = valores[6]
                        descuento =float(descuento_str)
                        
                        #Creamos una descripsion breve el producto
                        descripcion_producto = f"Codigo: {codigo_producto} / Tipo de precio: {tipo_precio} / Descuento producto: {descuento} %"

                        if descuento > 0:
                            total_descuento = precio * (descuento / 100)
                            precio_descuentado = precio - total_descuento
                        else:
                            precio_descuentado = precio
                            
                        #Agregamos el producto a vendido a la base de datos:    
                        agregar_producto_vendido(
                            producto_id,
                            cantidad,
                            precio
                        )    
                        
                        # Agrega los datos a la lista de productos seleccionados
                        productos_seleccionados.append({
                            "nombre_producto": nombre_producto,
                            "codigo_producto": codigo_producto,
                            "numero_unidades": numero_unidades,
                            "tipo_precio": tipo_precio,
                            "descuento": descuento,
                            "descripcion": descripcion_producto,
                            "precio_descuentado": precio_descuentado
                        })
                        
                        total_de_la_venta = 000000
                            
                    else:
                        return
            else:
                return
            
            #Obtenemos la cedula
            cedula_cliente = self.busqueda_cliente_por_cedula.get()
            
            if cedula_cliente != "":
                #Verificamos si el cliente ya existe:
                cliente_verificasion = session.query(Cliente).filter_by(cedula=cedula_cliente).one()
                id_del_cliente = cliente_verificasion.id
                
                if cliente_verificasion is not None:
                    # Si el cliente existe, obtén su nombre
                    nombre_del_cliente = cliente_verificasion.nombre
                
            else:
                #Obtenemos los datos del cliente nuevo:
                nombre_cliente_obtenido = self.nombre_cliente_entrada.get()
                apellido_cliente_obtenido = self.apellido_cliente_entrada.get()
                cedula_cliente_obtenido_str = self.cedula_cliente_entrada.get()
                cedula_cliente_obtenido = int(cedula_cliente_obtenido_str)
                correo_cliente_obtenido = self.correo_cliente_entrada.get()
                numero_cliente_obtenido_str = self.numero_cliente_entrada.get()
                numero_cliente_obtenido = int(numero_cliente_obtenido_str)
                direccion_cliente_obtenido = self.dirrecion_cliente_entrada.get()
                notas_cliente_obtenido = self.notas_adiccionales_cliente.get("1.0", "end-1c")
                
                if (nombre_cliente_obtenido != "" and apellido_cliente_obtenido != "" and cedula_cliente_obtenido != ""):
                    #Agregamos el cliente a la base de datos
                    agregar_cliente(
                        nombre_cliente_obtenido,
                        apellido_cliente_obtenido,
                        cedula_cliente_obtenido,
                        correo_cliente_obtenido,
                        numero_cliente_obtenido,
                        direccion_cliente_obtenido,
                        notas_cliente_obtenido
                    )
                    
                    cliente_recien_anadido = session.query(Cliente).filter_by(cedula=cedula_cliente_obtenido).one()
                    id_del_cliente = cliente_recien_anadido.id
                else:
                    return
                
            if id_del_cliente:
                #Obtenemos todos los valores de la factura:
                empleado_obtenido = self.empleado_que_vendio_entrada.get()
                medio_pago_obtenido = self.medio_de_pago_entrada.get()
                metodo_envio_obtenido = self.metodo_de_envio_entrada.get()
                iva_obtenido_float = self.porcentaje_de_iva_entrada.get()
                iva_obtenido = int(iva_obtenido_float)
                productos_json = json.dumps(productos_seleccionados)
                
                
                agregar_venta(
                    id_del_cliente,
                    empleado_obtenido,
                    medio_pago_obtenido,
                    metodo_envio_obtenido,
                    total_de_la_venta,
                    iva_obtenido_float,
                    productos_json
                )

            # Obtén la fecha actual
            fecha_actual = datetime.now().date()
            
            # Suma un día a la fecha actual para obtener la fecha de mañana
            fecha_manana = fecha_actual + timedelta(days=1)

            info_empresa =f"Empleado a cargo de la factura: {empleado_obtenido}\nNumero de contacto: +1 (555) 123-4567\nDirrecion de nuestra tienda: 123 Calle Ficticia, Ciudad Imaginaria, País de las Maravillas"
            
            factura = InvoiceGenerator(
                sender="Nombre empresa, XXXX.",
                to=nombre_del_cliente,
                logo="https://avatars.githubusercontent.com/u/141779507?v=4",
                number=000000,
                notes= info_empresa,
                shipping=000000,
                currency = "COP",
                tax=iva_obtenido,
                due_date = fecha_manana ,
                terms = "▹Pago Neto a 30 Días:\n\n    El importe total de esta factura debe pagarse en su totalidad dentro de los 30 días siguientes a la fecha de emisión de la factura.\n\n▹Formas de Pago:\n\n     Se aceptan pagos mediante transferencia bancaria, cheque o tarjeta de crédito. Los detalles bancarios se proporcionan a continuación"
            )
            
            # Agregar elementos a la factura
            for producto in productos_seleccionados:
                factura.add_item(
                    name=producto["nombre_producto"],
                    quantity=producto["numero_unidades"],
                    unit_cost=producto["precio_descuentado"],
                    description=producto["descripcion"]
                )

            # Genera la factura en un archivo PDF
            TituloFactura = f"Main\Facturas\Factura_{nombre_del_cliente}.pdf"
            factura.download(TituloFactura)
            self.VerFactura(TituloFactura)

        except Exception as e:
                print(e)
                         
    def VerFactura(self, ruta_pdf):
        try:
            time.sleep(5)
            os.startfile(ruta_pdf)
        except Exception as e:
            print(e)
   
        
if __name__ == "__main__":
    aplicacion = aplicacion()
    aplicacion.mainloop()
    