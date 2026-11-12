async def error_output(msg_handler,e):
    await msg_handler.finish(f"失败了！只找到一串神秘咒语，也许交给主人看看会不会有线索？{e}")