import tkinter as tk
from random import randint

class AppSerpiente:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Juego de la Serpiente")
        self.en_juego = False  # Variable que controla si el juego está en ejecución
        
        self.mostrar_menu()
        self.ventana.mainloop()

    def mostrar_menu(self):
        """Muestra el menú inicial del juego."""
        self.en_juego = False  # Se detiene el juego
        
        if hasattr(self, 'canvas'):
            self.canvas.destroy()

        self.menu = tk.Frame(self.ventana)
        self.menu.pack(pady=150)

        self.boton_inicio = tk.Button(self.menu, text="Iniciar Juego", command=self.iniciar_juego)
        self.boton_inicio.pack()

    def iniciar_juego(self):
        """Inicializa y comienza el juego."""
        self.menu.destroy()

        self.canvas = tk.Canvas(self.ventana, bg='black', width=400, height=400)
        self.canvas.pack(pady=20)

        self.serpiente = [(20, 20), (20, 30), (20, 40)]
        self.comida = (50, 50)
        self.direccion = "Derecha"
        
        self.dibujar()
        self.ventana.bind("<Left>", self.izquierda)
        self.ventana.bind("<Right>", self.derecha)
        self.ventana.bind("<Up>", self.arriba)
        self.ventana.bind("<Down>", self.abajo)
        
        self.en_juego = True  # Se inicia el juego
        self.jugar()

    def dibujar(self):
        """Dibuja la serpiente y la comida en el canvas."""
        self.canvas.delete("all")

        for x, y in self.serpiente:
            self.canvas.create_rectangle(x, y, x+10, y+10, fill="green")

        x, y = self.comida
        self.canvas.create_oval(x, y, x+10, y+10, fill="red")

    def mover(self):
        """Mueve la serpiente en la dirección actual."""
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
        else:
            self.serpiente.append(nuevo)
            self.serpiente = self.serpiente[1:]

        if (nuevo[0] < 0 or nuevo[0] >= 400 or
            nuevo[1] < 0 or nuevo[1] >= 400 or
            len(self.serpiente) != len(set(self.serpiente))):
            self.mostrar_menu()
            return

        self.dibujar()

    def jugar(self):
        """Lógica principal del juego."""
        if self.en_juego:  # Solo se mueve si el juego está en ejecución
            self.mover()
            self.ventana.after(100, self.jugar)

    # Métodos de control de dirección
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

if __name__ == "__main__":
    juego = AppSerpiente()