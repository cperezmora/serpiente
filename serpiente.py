import tkinter as tk
from random import randint
from time import sleep

class AppSerpiente:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Juego de la Serpiente")
        self.en_juego = False
        
        self.vidas = 3
        self.mostrar_menu()
        self.ventana.mainloop()

    def mostrar_menu(self):
        """Muestra el menú inicial del juego."""
        self.en_juego = False
        self.vidas = 3  # Restablecer las vidas
        
        if hasattr(self, 'canvas'):
            self.canvas.destroy()

        self.menu = tk.Frame(self.ventana)
        self.menu.pack(pady=150)

        self.boton_inicio = tk.Button(self.menu, text="Iniciar Juego", command=self.iniciar_juego)
        self.boton_inicio.pack()

    def iniciar_juego(self):
        """Inicializa y comienza el juego."""
        if hasattr(self, 'menu'):
            self.menu.destroy()

        self.canvas = tk.Canvas(self.ventana, bg='black', width=400, height=400)
        self.canvas.pack(pady=20)

        self.reset_serpiente()

        # Generar obstáculos aleatorios, pero no en la posición inicial de la serpiente
        self.obstaculos = []
        while len(self.obstaculos) < 5:
            obs = (randint(0, 39)*10, randint(0, 39)*10)
            if obs not in self.serpiente and obs != self.comida:
                self.obstaculos.append(obs)

        self.dibujar()
        self.ventana.bind("<Left>", self.izquierda)
        self.ventana.bind("<Right>", self.derecha)
        self.ventana.bind("<Up>", self.arriba)
        self.ventana.bind("<Down>", self.abajo)
        
        self.en_juego = True
        self.jugar()

    def reset_serpiente(self):
        """Restablece la posición y dirección de la serpiente a su estado inicial."""
        self.serpiente = [(20, 20), (20, 30), (20, 40)]
        self.comida = (50, 50)
        self.direccion = "Derecha"

    def dibujar(self):
        """Dibuja la serpiente, la comida, los obstáculos y las vidas."""
        self.canvas.delete("all")

        for x, y in self.serpiente:
            self.canvas.create_rectangle(x, y, x+10, y+10, fill="green")
        
        for x, y in self.obstaculos:
            self.canvas.create_rectangle(x, y, x+10, y+10, fill="blue")

        x, y = self.comida
        self.canvas.create_oval(x, y, x+10, y+10, fill="red")

        # Dibujar vidas
        for i in range(self.vidas):
            self.canvas.create_text(380 - i*20, 10, text="❤", font=("Arial", 12), fill="red")

    def mostrar_cuenta_atras(self):
        """Muestra una cuenta atrás de 3 segundos."""
        for i in range(3, 0, -1):
            self.canvas.delete("all")
            self.canvas.create_text(200, 200, text=str(i), font=("Arial", 44), fill="white")
            self.ventana.update()
            sleep(1)

    def mover(self):
        cabeza = self.serpiente[-1]
        x, y = cabeza

        if self.direccion == "Derecha":
            nuevo = (x+10, y)
        elif self.direccion == "Izquierda":
            nuevo = (x-10, y)
        elif self.direccion == "Arriba":
            nuevo = (x, y-10)
        else:
            nuevo = (x, y+10)

        if nuevo == self.comida:
            self.serpiente.append(self.comida)
            self.comida = (randint(0, 39)*10, randint(0, 39)*10)
            
            # Cambiar la posición de los obstáculos
            self.obstaculos = [(randint(0, 39)*10, randint(0, 39)*10) for _ in range(5)]
        else:
            self.serpiente.append(nuevo)
            self.serpiente = self.serpiente[1:]

        # Condiciones de muerte
        if (nuevo[0] < 0 or nuevo[0] >= 400 or
            nuevo[1] < 0 or nuevo[1] >= 400 or
            len(self.serpiente) != len(set(self.serpiente)) or
            nuevo in self.obstaculos):
            self.vidas -= 1
            if self.vidas == 0:
                self.mostrar_menu()
                return
            else:
                self.reset_serpiente()  # Restablecer la posición y dirección de la serpiente
                self.mostrar_cuenta_atras()
        self.dibujar()

    def izquierda(self, _):
        if self.direccion != "Derecha":
            self.direccion = "Izquierda"
    
    def derecha(self, _):
        if self.direccion != "Izquierda":
            self.direccion = "Derecha"
    
    def arriba(self, _):
        if self.direccion != "Abajo":
            self.direccion = "Arriba"
    
    def abajo(self, _):
        if self.direccion != "Arriba":
            self.direccion = "Abajo"

    def jugar(self):
        if self.en_juego:
            self.mover()
            self.ventana.after(100, self.jugar)

if __name__ == "__main__":
    juego = AppSerpiente()
