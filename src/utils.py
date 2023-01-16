from src.horoscopo import Horoscopo
import uuid
_months = ["enero", "febrero", "marzo", "abri", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

class Utils:
    @staticmethod
    def get_horoscopo(birthday_text):
        horoscopos = Horoscopo()
        tuple_nacimiento = Utils.get_birthday_format(birthday_text)
        return horoscopos.get_horoscopo_name(tuple_nacimiento)
        
    @staticmethod
    def get_birthday_format(birthday_text):
        fecha_nacimiento_format = birthday_text.split('Fecha de nacimiento: ')[1]
        return (int(fecha_nacimiento_format.split(' de ')[0]),_months.index(fecha_nacimiento_format.split(' de ')[1])+1)
    

    class Files:
        def __init__(self):
            self.files = []
            self.configurations = []
            self.keys = []
           
        def new_fichero(self,path,operation):
            if (path,operation) not in self.configurations:
                self.files.append(open(path, operation,encoding="utf-8"))
                self.configurations.append((path,operation))
                identificator = str(uuid.uuid4().fields[-1])[:5]
                self.keys.append(identificator) 
                return identificator
            index = self.configurations.index((path,operation))
            return self.keys[index]
            
        def action(self,identificator,text = None):
            index = self.keys.index(identificator)
            operation = self.configurations[index][1]
            file = self.files[index]
            if operation == 'a':
                file.write(text)
            if operation == 'r':
                return file.readlines()
            
        def close(self,identificator):
            index = self.keys.index(identificator)
            file = self.files[index]
            self.files.pop(index)
            self.configurations.pop(index)
            self.keys.pop(index)
            file.close()
            
        def print():
            print('Lo tengo')