from datetime import datetime
def validar_data(data_str: str | None) -> datetime | None:
    if not isinstance(data_str, str):
        return None
    try:
        return datetime.strptime(data_str, "%d/%m/%Y")
    except ValueError:
        return None