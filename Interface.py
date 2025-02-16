import tkinter as tk
import random
import math
import GeneticAlgorithm as ga
class interface:
    def __init__(self, population):
        self.population = population
        self.gen_number = 0
        self.labels = []

    def draw_flower(self, canvas, x, y, flower):
        stem_color = random.choice(['darkgreen'])
        petal_color = "#%02x%02x%02x" % flower.petals_color
        center_color = "#%02x%02x%02x" % flower.center_color

        # Draw stem
        canvas.create_line(x, y, x, y + 100, fill=stem_color, width=5)

        petal_radius = 20
        petal_distance = 40  
        for i in range(flower.petals_number):
            angle = math.radians(i * (360 / flower.petals_number))  # even distribution
            petal_x = x + petal_distance * math.cos(angle)
            petal_y = y + petal_distance * math.sin(angle)
            
            # Draw petal
            canvas.create_oval(petal_x - petal_radius, petal_y - petal_radius,
                            petal_x + petal_radius, petal_y + petal_radius,
                            fill=petal_color, outline='')

        # Draw flower center
        center_radius = flower.center_size #10
        canvas.create_oval(x - center_radius, y - center_radius, 
                        x + center_radius, y + center_radius, 
                        fill=center_color, outline='')
        

    def update_canvas(self, canvas):
        canvas.delete("all") 
        for i, flower in enumerate(self.population):
            self.draw_flower(canvas, 60 + i * 200, 150, flower)
            self.labels[i].config(text=f"Fitness: {flower.fitness}")  

    def evolve_and_update(self, canvas, gen_label):
        self.gen_number += 1
        gen_label.config(text=f'Generation: {self.gen_number}')
        ga.evolve_population()  
        self.update_canvas(canvas) 
        

    def on_hover(self, event, canvas):
        x, y = event.x, event.y
        
        for i, flower in enumerate(self.population):
            flower_x = 60 + i * 200  
            flower_y = 150  
            
            if (flower_x - 40 < x < flower_x + 40) and (flower_y - 40 < y < flower_y + 140):
                flower.fitness += 1 
                print(f"Flower {i} fitness increased to {flower.fitness}")  
                self.labels[i].config(text=f"Fitness: {flower.fitness}") 
                break  

    def run(self):
        root = tk.Tk()
        root.title("Flowers in Tkinter")
        canvas = tk.Canvas(root, width=1920, height=1080, bg="lightblue")
        gen_label = tk.Label(root, text=f'Generation: {self.gen_number}')
        gen_label.place(x = 60, y = 500)
        evolve_button = tk.Button(root, text="Evolve Population", command=lambda: self.evolve_and_update(canvas, gen_label))
        evolve_button.place(x=720, y=540)
        canvas.pack()

        start_x = 60
        spacing = 200
        for i in range(len(self.population)):
            self.draw_flower(canvas, start_x + i * spacing, 150, self.population[i])
            label = tk.Label(root, text=f"Fitness: {self.population[i].fitness}")
            label.place(x=60 + i * 195, y=300)  
            self.labels.append(label) 

        canvas.bind("<Motion>", lambda event: self.on_hover(event, canvas))

        
        root.mainloop()

population = ga.init_population()
start = interface(population)
start.run()
