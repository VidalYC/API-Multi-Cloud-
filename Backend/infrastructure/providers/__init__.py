"""
Paquete de Proveedores de Infraestructura

Este __init__.py exporta todas las implementaciones concretas de proveedores,
permitiendo que otras partes de la aplicación las importen desde un único lugar.
"""
from .aws import AWS
from .azure import Azure
from .google import Google
from .onpremise import OnPremise