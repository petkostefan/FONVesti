from datetime import datetime, timedelta


def predmetDatum(datum):
    sada = datetime.now()
    
    if datetime.strptime(datum, '%d.%m.%Y.') + timedelta(days=5)>=sada:
        return 'warning'
    else:
        return 'info'

def formatirajDatum(datum, formatDatuma):
    return datetime.strptime(datum, formatDatuma).strftime('%d.%m.%Y.')