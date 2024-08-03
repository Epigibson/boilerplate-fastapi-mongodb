from enum import Enum


class ReceiptType(str, Enum):
    payment = "payment"
    refund = "refund"
    inscription = "inscription"
    package = "package"
    product = "product"
    service = "service"
