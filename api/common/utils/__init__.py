from datetime import datetime
import pytz


def adjust_datetime_to_utc(date: datetime) -> datetime:
    """
    Ajusta uma data para UTC e garante que seja offset-aware.

    :param date: A data a ser ajustada.
    :return: A data ajustada para UTC e offset-aware.
    """
    if date.tzinfo is None:
        return date.replace(tzinfo=pytz.UTC)
    else:
        return date.astimezone(pytz.UTC)
