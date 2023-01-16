import json

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
    
class Horoscopo(metaclass=Singleton):
    def __init__(self):
        with open("data/horoscopo.json", "r") as jsonfile:
            self.horoscopo = json.load(jsonfile)
    def get_horoscopo_name(self,fecha_horoscopo):
        mes_birthday = fecha_horoscopo[1]
        dia_birthday = fecha_horoscopo[0]
        for horoscopo in self.horoscopo['horoscopos']:
            if mes_birthday == horoscopo['mes_inicio']:
                if dia_birthday >= horoscopo['dia_inicio']:
                    return horoscopo['nombre']
            if mes_birthday == horoscopo['mes_fin']:
                if dia_birthday <= horoscopo['dia_fin']:
                    return horoscopo['nombre']  