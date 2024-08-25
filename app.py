import tkinter as tk
from tkinter import messagebox

class NotesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestionnaire de Notes")
        
        # Chemin du fichier pour stocker les notes
        self.filename = "data/info.txt"
        
        # Liste pour stocker les notes
        self.notes = []
        
        # Charger les notes depuis le fichier
        self.load_notes()
        
        # Interface
        self.create_widgets()

    def create_widgets(self):
        # Entrée pour le titre de la note
        self.title_label = tk.Label(self.root, text="Titre:")
        self.title_label.pack(pady=5)
        
        self.title_entry = tk.Entry(self.root, width=50)
        self.title_entry.pack(pady=5)
        
        # Entrée pour le contenu de la note
        self.content_label = tk.Label(self.root, text="Contenu:")
        self.content_label.pack(pady=5)
        
        self.content_text = tk.Text(self.root, width=50, height=10)
        self.content_text.pack(pady=5)

        # Entrée pour le mot de passe pour encrypter
        self.key_label = tk.Label(self.root, text="key")
        self.key_label.pack(pady=5)

        self.key_text = tk.Entry(self.root, width=50)
        self.key_text.pack(pady=5)
        
        # Bouton pour ajouter la note
        self.add_button = tk.Button(self.root, text="Ajouter Note", command=self.add_note)
        self.add_button.pack(pady=5)
        
        # Liste pour afficher les titres des notes
        self.notes_listbox = tk.Listbox(self.root, width=50, height=10)
        self.notes_listbox.pack(pady=5)
        
        # Bouton pour afficher le contenu de la note sélectionnée
        self.view_button = tk.Button(self.root, text="Voir Contenu", command=self.view_note)
        self.view_button.pack(pady=5)
        
        # Ajouter les titres de notes existants à la liste
        self.update_notes_listbox()

    def add_note(self):
        title = self.title_entry.get()
        content = self.content_text.get("1.0", tk.END).strip()
        key = self.key_text.get().strip()
                    
        if title and content and key:
            encrypted_content = self.encrypt(content, key)  # Appel de la méthode avec self
            self.notes.append({"title": title, "content": encrypted_content})
            self.notes_listbox.insert(tk.END, title)
            self.save_note_to_file(title, encrypted_content)
            self.title_entry.delete(0, tk.END)
            self.content_text.delete("1.0", tk.END)
            self.key_text.delete(0, tk.END)  # Optionnel : nettoyer le champ de clé après l'ajout
        else:
            messagebox.showwarning("Entrée invalide", "Le titre, le contenu et la clé ne doivent pas être vides!")


    def encrypt(self, content, key):
        encrypted_chars = []
        # On itère sur chaque caractère du message
        for i in range(len(content)):
            # XOR le caractère du message avec le caractère de la clé correspondante
            key_c = key[i % len(key)]  # Récupère le caractère de la clé (elle se répète si nécessaire)
            encrypted_c = chr(ord(content[i]) ^ ord(key_c))  # XOR entre les codes ASCII des caractères
            encrypted_chars.append(encrypted_c)
        
        # Retourner la chaîne encryptée (ou décryptée si on applique à nouveau la fonction)
        return ''.join(encrypted_chars)


    def ask_key(self):
        # Créer et afficher les champs pour la clé
        self.key_label = tk.Label(self.root, text="Entrez la clé pour déchiffrer la note :")
        self.key_label.pack(pady=5)
        
        self.key_entry = tk.Entry(self.root, width=50, show="*")  # Utiliser show="*" pour masquer la clé lors de la saisie
        self.key_entry.pack(pady=5)
        
        # Ajouter un bouton pour confirmer la clé et cacher les widgets après saisie
        def confirm_key():
            self.entered_key = self.key_entry.get().strip()
            self.key_label.pack_forget()
            self.key_entry.pack_forget()
            self.confirm_button.pack_forget()
            self.root.quit()  # Arrête la boucle de l'interface pour continuer l'exécution

        self.confirm_button = tk.Button(self.root, text="Confirmer", command=confirm_key)
        self.confirm_button.pack(pady=5)
        
        # Lancer une boucle pour attendre la saisie de la clé
        self.root.mainloop()
        
        return self.entered_key

    def view_note(self):
        selected_note_index = self.notes_listbox.curselection()
        
        if selected_note_index:
            note = self.notes[selected_note_index[0]]
            key = self.ask_key()  # Obtenir la clé de l'utilisateur
            decrypted_content = self.encrypt(note["content"], key)  # Décrypter le contenu avec la clé
            
            # Afficher la note déchiffrée
            messagebox.showinfo(note["title"], decrypted_content)
        else:
            messagebox.showwarning("Aucune sélection", "Veuillez sélectionner une note pour voir son contenu.")


    def save_note_to_file(self, title, content):
        # Sauvegarde la note dans le fichier texte
        with open(self.filename, "a") as file:
            file.write(f"{title}\n{content}\n---\n")

    def load_notes(self):
        # Charge les notes depuis le fichier texte
        try:
            with open(self.filename, "r") as file:
                lines = file.readlines()
                
                note = {}
                content_lines = []
                for line in lines:
                    line = line.strip()
                    if line == "---":
                        # Sauvegarde la note complétée
                        if note:
                            note["content"] = "\n".join(content_lines)
                            self.notes.append(note)
                            note = {}
                            content_lines = []
                    elif "title" not in note:
                        note["title"] = line
                    else:
                        content_lines.append(line)
        except FileNotFoundError:
            # Si le fichier n'existe pas, on le crée
            with open(self.filename, "w") as file:
                pass

    def update_notes_listbox(self):
        # Met à jour la Listbox avec les titres des notes chargées
        for note in self.notes:
            self.notes_listbox.insert(tk.END, note["title"])

# Création de la fenêtre principale
root = tk.Tk()
app = NotesApp(root)
root.mainloop()


# by itsantho