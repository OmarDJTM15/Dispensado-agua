import asyncio

async def simular_despacho(litros, callback):
    """Simula el llenado de agua (sin hardware)."""
    actual = 0
    while actual < litros:
        await asyncio.sleep(0.2)
        actual += 0.5
        callback(actual)
