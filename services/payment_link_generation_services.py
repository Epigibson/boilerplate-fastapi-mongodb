from datetime import datetime

from models.choices.receipt_types import ReceiptType
from models.history_payment_model import HistoryPayment
from models.receipts_model import Receipts
from services.mercado_pago_checkout_service import MercadoPagoService
from services.product_services import ProductService
from services.user_services import UserService


class PaymentLinkGenerationService:

    @staticmethod
    async def generate_payment_link():
        products_amount = 0
        products_concepts = ''
        today = datetime.now()
        if today.day <= 15:
            raise Exception('No es el dia 10 de cada mes.')
        user_list = await UserService.get_users_inscribed_and_active()
        if not user_list:
            raise Exception('No hay usuarios inscritos.')
        for user in user_list:

            if (user.products_which_inscribed is None) or (len(user.products_which_inscribed) == 0):
                pass
                # raise Exception('No hay productos seleccionados.')
            for product_id in user.products_which_inscribed:
                product = await ProductService.get_product_by_object_id(product_id)
                if product.product_name == "Inscripcion":
                    product.price = product.price / 2
                products_amount += product.price
                products_concepts += f'{product.product_name}, '

            payment_link = await MercadoPagoService.create_preference(user.products_which_inscribed, user.user_id)

            if payment_link:
                new_receipt = Receipts(
                    user_id=user.id,
                    receipt_type=ReceiptType.payment,
                    receipt_amount=products_amount,
                    receipt_description=f'Recibo de {products_concepts}.',
                    receipt_status='Pendiente',
                    payment_link=payment_link['init_point'],
                )
                await new_receipt.insert()
                if new_receipt:
                    new_movement = HistoryPayment(
                        user=user.id,
                        receipt_id=new_receipt.id,
                        amount=products_amount,
                        status='Creado',
                        payment_type=new_receipt.receipt_type.value,
                        payment_method='',
                    )
                    await new_movement.insert()

            return payment_link
