from enum import Enum


class ModuleTypes(str, Enum):
    """
    Enum class for modules
    """
    auth = "autenticacion"
    inscription = "inscripciones"
    users = "usuarios"
    athletes = "atletas"
    payments = "pagos"
    history_balance = "historial de saldo"
    groups = "grupos"
    coaches = "entrenadores"
    memberships = "membresias"
    discounts = "descuentos"
    sales_products = "productos"
    sales_history = "historial de ventas"
    configurations = "configuraciones"
