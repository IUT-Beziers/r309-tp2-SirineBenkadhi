import tkinter as tk
from PIL import Image, ImageTk
from tkinter import simpledialog
import os

# Classe représentant un élément du réseau
class ElementReseau:
    def __init__(self, canvas, x, y, chemin_image, nom):
        self.canvas = canvas
        self.nom = nom
        self.image = Image.open(chemin_image).resize((64, 64))
        self.icone = ImageTk.PhotoImage(self.image)
        self.etiquette = None
        self.x = x
        self.y = y
        self.id = canvas.create_image(x, y, image=self.icone, tags=nom)
        self.canvas.tag_bind(nom, "<ButtonPress-1>", self.on_clic)
        self.dernier_x = x
        self.dernier_y = y
        self.en_deplacement = False
        self.canvas.tag_bind(nom, "<Button-3>", lambda e: self.montrer_menu_contextuel(e))

        self.canvas.tag_bind(nom, "<ButtonPress-1>", self.on_appui_element)

    def on_appui_element(self, event):
        self.en_deplacement = True
        self.dernier_x = event.x
        self.dernier_y = event.y
        self.canvas.tag_bind(self.nom, "<B1-Motion>", self.on_deplacement_element)
        self.canvas.tag_bind(self.nom, "<ButtonRelease-1>", self.on_relachement_element)

    def on_deplacement_element(self, event):
        if self.en_deplacement:
            x, y = event.x, event.y
            dx = x - self.dernier_x
            dy = y - self.dernier_y
            self.x += dx
            self.y += dy
            self.canvas.move(self.id, dx, dy)
            if self.etiquette:
                self.canvas.move(self.etiquette, dx, dy)
            self.dernier_x, self.dernier_y = x, y

    def on_relachement_element(self, event):
        self.en_deplacement = False

    def on_clic(self, event):
        if mode_suppression.get():
            self.supprimer_element()
        else:
            self.canvas.tag_bind(self.nom, "<B1-Motion>", self.on_deplacement)

    def on_deplacement(self, event):
        if not mode_suppression.get() and not mode_creation.get():
            x, y = event.x, event.y
            if abs(x - self.dernier_x) < 50 and abs(y - self.dernier_y) < 50:
                self.x, self.y = x, y
                self.canvas.coords(self.id, x, y)
                if self.etiquette:
                    self.canvas.coords(self.etiquette, x, y + 70)
            self.dernier_x, self.dernier_y = x, y

            mode_creation = tk.BooleanVar()

    def montrer_menu_contextuel(self, event):
        menu = tk.Menu(self.canvas, tearoff=0)
        menu.add_command(label="Renommer", command=self.renommer_element)
        menu.add_command(label="Supprimer", command=self.supprimer_element)
        menu.post(event.x_root, event.y_root)

    def renommer_element(self):
        nouveau_nom = simpledialog.askstring("Renommer", "Entrez un nouveau nom:")
        if nouveau_nom:
            self.nom = nouveau_nom
            self.canvas.itemconfig(self.id, tags=nouveau_nom)
            self.maj_etiquette()

    def supprimer_element(self):
        if self.nom in elements:
            canvas.delete(self.id)
        if self.etiquette:
            canvas.delete(self.etiquette)
        elements.pop(self.nom, None)

    def maj_etiquette(self):
        if self.etiquette:
            canvas.delete(self.etiquette)
        x, y = self.x, self.y
        self.etiquette = canvas.create_text(x, y + 70, text=self.nom, anchor=tk.CENTER)

# Fonction pour basculer le mode de suppression
def basculer_mode_suppression():
    mode_suppression.set(not mode_suppression.get())
    if mode_suppression.get():
        bouton_switch.config(state=tk.DISABLED)
        bouton_pc.config(state=tk.DISABLED)
        bouton_router.config(state=tk.DISABLED)
        bouton_creation_lien.config(state=tk.DISABLED)
    else:
        bouton_switch.config(state=tk.NORMAL)
        bouton_pc.config(state=tk.NORMAL)
        bouton_router.config(state=tk.NORMAL)
        bouton_creation_lien.config(state=tk.NORMAL)

# Fonction pour ajouter un élément au réseau
def ajouter_element(type_element):
    if type_element in ["Switch", "Router", "PC"]:
        bouton_pc.config(state=tk.DISABLED)
        bouton_switch.config(state=tk.DISABLED)
        bouton_router.config(state=tk.DISABLED)
        bouton_creation_lien.config(state=tk.DISABLED)
        canvas.bind("<Button-1>", lambda event: placer_element(event, type_element))
    else:
        x = 50
        y = 50
        chemin_image = ""

        repertoire_script = os.path.dirname(os.path.abspath(__file__))

        if type_element == "PC":
            chemin_image = os.path.join(repertoire_script, "images", "pc_photo.jpg")
        element = ElementReseau(canvas, x, y, chemin_image, type_element)
        elements[element.nom] = element

        bouton_pc.config(state=tk.NORMAL)
        bouton_switch.config(state=tk.NORMAL)
        bouton_router.config(state=tk.NORMAL)
        bouton_creation_lien.config(state=tk.NORMAL)

# Fonction pour placer un élément au clic de la souris
def placer_element(event, type_element):
    x = event.x
    y = event.y
    chemin_image = ""

    repertoire_script = os.path.dirname(os.path.abspath(__file__))

    if type_element == "Switch":
        chemin_image = os.path.join(repertoire_script, "images", "switch_photo.jpg")
    elif type_element == "Router":
        chemin_image = os.path.join(repertoire_script, "images", "router_photo.jpg")
    elif type_element == "PC":
        chemin_image = os.path.join(repertoire_script, "images", "pc_photo.jpg")
    
    element = ElementReseau(canvas, x, y, chemin_image, type_element)
    elements[element.nom] = element

    bouton_pc.config(state=tk.NORMAL)
    bouton_switch.config(state=tk.NORMAL)
    bouton_router.config(state=tk.NORMAL)
    bouton_creation_lien.config(state=tk.NORMAL)

# Fonction pour basculer le mode de création de lien
def basculer_mode_creation_lien():
    mode_lien.set(not mode_lien.get())
    if mode_lien.get():
        bouton_switch.config(state=tk.DISABLED)
        bouton_pc.config(state=tk.DISABLED)
        bouton_router.config(state=tk.DISABLED)
        bouton_creation_lien.config(state=tk.DISABLED)
    else:
        bouton_switch.config(state=tk.NORMAL)
        bouton_pc.config(state=tk.NORMAL)
        bouton_router.config(state=tk.NORMAL)
        bouton_creation_lien.config(state=tk.NORMAL)

# Fonction pour créer le mode de lien
def creer_mode_lien():
    element_depart.set(None)
    basculer_mode_creation_lien()

elements_selectionnes = set()

# Fonction pour gérer le clic sur un élément du réseau
def on_clic_element(element):
    if mode_suppression.get():
        element.supprimer_element()
    elif mode_lien.get():
        if element_depart.get() is None:
            element_depart.set(element.nom)
        else:
            autre_element = elements.get(element_depart.get())
            if autre_element and autre_element != element:
                element.dessiner_lien(autre_element)
        basculer_mode_creation_lien()
    else:
        # Bascule la sélection
        if element.id in elements_selectionnes:
            canvas.itemconfig(element.id, outline="")
            elements_selectionnes.remove(element.id)
        else:
            canvas.itemconfig(element.id, outline="red")
            elements_selectionnes.add(element.id)

# Fonction pour supprimer les éléments sélectionnés
def supprimer_elements_selectionnes():
    for id_element in elements_selectionnes.copy():
        tags_element = canvas.gettags(id_element)
        for nom_element in tags_element:
            element = elements.get(nom_element)
            if element:
                element.supprimer_element()
                elements_selectionnes.remove(id_element)

# Fonction pour créer un nouvel élément à la position de la souris
def creer_element(event):
    x = event.x
    y = event.y
    chemin_image = ""
    type_element = ""  

    if event.char.lower() == "p":
        type_element = "PC"
    elif event.char.lower() == "s":
        type_element = "Switch"
    elif event.char.lower() == "r":
        type_element = "Router"

    repertoire_script = os.path.dirname(os.path.abspath(__file__))

    if type_element:
        if type_element == "PC":
            chemin_image = os.path.join(repertoire_script, "images", "pc_photo.jpg")
        elif type_element == "Switch":
            chemin_image = os.path.join(repertoire_script, "images", "switch_photo.jpg")
        elif type_element == "Router":
            chemin_image = os.path.join(repertoire_script, "images", "router_photo.jpg")
        
        element = ElementReseau(canvas, x, y, chemin_image, type_element)
        elements[element.nom] = element

        bouton_pc.config(state=tk.NORMAL)
        bouton_switch.config(state=tk.NORMAL)
        bouton_router.config(state=tk.NORMAL)
        bouton_creation_lien.config(state=tk.NORMAL)

# Création de la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Programmation Evennementielle")

# Création du canevas
canvas = tk.Canvas(fenetre, width=800, height=600, bg="white")
canvas.pack(fill="both", expand=True)

# Création des boutons
bouton_switch = tk.Button(fenetre, text="Switch", compound=tk.TOP, command=lambda: ajouter_element("Switch"))
bouton_pc = tk.Button(fenetre, text="PC", compound=tk.TOP, command=lambda: ajouter_element("PC"))
bouton_router = tk.Button(fenetre, text="Router", compound=tk.TOP, command=lambda: ajouter_element("Router"))
bouton_creation_lien = tk.Button(fenetre, text="Créer lien", command=creer_mode_lien)

# Chargement des images pour les boutons
repertoire_script = os.path.dirname(os.path.abspath(__file__))
image_switch_path = os.path.join(repertoire_script, "images", "switch_photo.jpg")
image_pc_path = os.path.join(repertoire_script, "images", "pc_photo.jpg")
image_router_path = os.path.join(repertoire_script, "images", "router_photo.jpg")

image_switch = Image.open(image_switch_path).resize((32, 32))
image_pc = Image.open(image_pc_path).resize((32, 32))
image_router = Image.open(image_router_path).resize((32, 32))

icone_switch = ImageTk.PhotoImage(image_switch)
icone_pc = ImageTk.PhotoImage(image_pc)
icone_router = ImageTk.PhotoImage(image_router)
icone_trait = ImageTk.PhotoImage(image_router)


bouton_switch.config(image=icone_switch)
bouton_pc.config(image=icone_pc)
bouton_router.config(image=icone_router)


bouton_switch.pack(side="left")
bouton_pc.pack(side="left")
bouton_router.pack(side="left")
bouton_creation_lien.pack(side="left")


elements = {}
mode_suppression = tk.BooleanVar()
mode_lien = tk.BooleanVar()
element_depart = tk.StringVar()


fenetre.bind("p", lambda event: creer_element(event))
fenetre.bind("s", lambda event: creer_element(event))
fenetre.bind("r", lambda event: creer_element(event))


fenetre.mainloop()
