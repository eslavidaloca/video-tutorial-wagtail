class newClass():
    number = 800
    cadenita = 'Esto seria un string en python'
    
    def myFunction(self):
        for i in range(10):
            print(i)
        print(self.number)
        print(f'Hola, {self.cadenita}')
            
newCadenita = 'Esto no entra en la clase de arriba'

a = newClass()
a.myFunction()
