import asyncio


async def periodic_task_runner():
    while True:
        # Llama a tu función que revisa y actualiza los estados de pago
        await asyncio.sleep(86400)
