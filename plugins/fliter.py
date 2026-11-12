from config.global_setting import global_setting


def fliter_group(gid)->bool:
    if global_setting.MODE=="WHITE":
        if gid in global_setting.WHITE:
            return True
    if global_setting.MODE=="BLACK":
        if gid not in global_setting.BLACK:
            return True

    return False