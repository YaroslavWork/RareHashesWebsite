from datetime import datetime

def log(title, message, with_timestamp: bool = True):
    """
    Logs for debugging

    Args:
        title (_type_): Log title
        message (_type_): Log description
        with_timestamp (bool, optional): With time mark or without. Defaults to True.
    """
    
    if with_timestamp:
        now = datetime.now()
        formatted = now.strftime("%d.%m.%Y %H:%M:%S.") + f"{now.microsecond:03d}"
        print(f"({formatted}) {title}: {message}")