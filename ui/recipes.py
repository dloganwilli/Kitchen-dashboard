# ui/recipes.py

import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
import os
from ui.styles import COLORS, FONTS, WIDGET_STYLE

DB_PATH = os.path.join("data", "recipes.db")

class RecipeWidget:
    def __init__(self, parent):
        self.parent = parent
        self.setup_ui()
        self.load_recipes()

    def setup_ui(self):
        self.left_frame = tk.Frame(self.parent, bg=COLORS["bg"], width=200)
        self.left_frame.pack(side="left", fill="y")

        self.right_frame = tk.Frame(self.parent, bg=COLORS["bg"])
        self.right_frame.pack(side="right", expand=True, fill="both")

        self.recipe_listbox = tk.Listbox(
            self.left_frame,
            font=FONTS["body"],
            bg=COLORS["entry_bg"],
            fg=COLORS["fg"],
            selectbackground=COLORS["highlight"]
        )
        self.recipe_listbox.pack(padx=10, pady=10, fill="both", expand=True)
        self.recipe_listbox.bind("<<ListboxSelect>>", self.show_recipe)

        add_btn = tk.Button(self.left_frame, text="Add Recipe", command=self.add_recipe,
                            font=FONTS["button"], bg=COLORS["button"], fg=COLORS["fg"], **WIDGET_STYLE["button"])
        add_btn.pack(pady=5)

        self.edit_btn = tk.Button(self.left_frame, text="Edit Recipe", command=self.edit_recipe,
                                  state="disabled", font=FONTS["button"], bg=COLORS["button"], fg=COLORS["fg"], **WIDGET_STYLE["button"])
        self.edit_btn.pack(pady=5)

        self.delete_btn = tk.Button(self.left_frame, text="Delete Recipe", command=self.delete_recipe,
                                    state="disabled", font=FONTS["button"], bg=COLORS["button"], fg=COLORS["fg"], **WIDGET_STYLE["button"])
        self.delete_btn.pack(pady=5)

        self.recipe_display = tk.Text(self.right_frame, font=FONTS["body"], wrap="word",
                                      bg=COLORS["entry_bg"], fg=COLORS["fg"], insertbackground=COLORS["fg"])
        self.recipe_display.pack(padx=10, pady=10, fill="both", expand=True)

    def load_recipes(self):
        self.recipe_listbox.delete(0, tk.END)
        self.recipes = []

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, title FROM recipes ORDER BY title ASC")
        self.recipes = cursor.fetchall()
        conn.close()

        for _, title in self.recipes:
            self.recipe_listbox.insert(tk.END, title)

        self.edit_btn.config(state="disabled")
        self.delete_btn.config(state="disabled")

    def show_recipe(self, event):
        selected = self.recipe_listbox.curselection()
        if not selected:
            self.edit_btn.config(state="disabled")
            self.delete_btn.config(state="disabled")
            return

        self.edit_btn.config(state="normal")
        self.delete_btn.config(state="normal")

        index = selected[0]
        recipe_id = self.recipes[index][0]

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT title, ingredients, instructions FROM recipes WHERE id = ?", (recipe_id,))
        row = cursor.fetchone()
        conn.close()

        self.recipe_display.delete("1.0", tk.END)
        if row:
            title, ingredients, instructions = row
            content = f"📌 {title}\n\n🧂 Ingredients:\n{ingredients}\n\n📋 Instructions:\n{instructions}"
            self.recipe_display.insert(tk.END, content)

    def add_recipe(self):
        title = simpledialog.askstring("Recipe Title", "Enter the recipe title:")
        if not title:
            return

        ingredients = simpledialog.askstring("Ingredients", "Enter ingredients:")
        if ingredients is None:
            return

        instructions = simpledialog.askstring("Instructions", "Enter instructions:")
        if instructions is None:
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO recipes (title, ingredients, instructions) VALUES (?, ?, ?)",
                       (title, ingredients, instructions))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", f"Recipe '{title}' added!")
        self.load_recipes()

    def edit_recipe(self):
        selected = self.recipe_listbox.curselection()
        if not selected:
            return

        index = selected[0]
        recipe_id = self.recipes[index][0]

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT title, ingredients, instructions FROM recipes WHERE id = ?", (recipe_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            messagebox.showerror("Error", "Could not find recipe.")
            return

        title, ingredients, instructions = row

        modal = tk.Toplevel(self.parent)
        modal.title("Edit Recipe")
        modal.geometry("500x500")
        modal.configure(bg=COLORS["bg"])
        modal.grab_set()

        title_var = tk.StringVar(value=title)
        ingredients_text = tk.Text(modal, height=8, wrap="word", bg=COLORS["entry_bg"], fg=COLORS["entry_fg"])
        instructions_text = tk.Text(modal, height=10, wrap="word", bg=COLORS["entry_bg"], fg=COLORS["entry_fg"])

        ingredients_text.insert("1.0", ingredients)
        instructions_text.insert("1.0", instructions)

        tk.Label(modal, text="Title:", bg=COLORS["bg"], fg=COLORS["fg"], font=FONTS["body"]).pack(anchor="w", padx=10, pady=(10, 0))
        tk.Entry(modal, textvariable=title_var, font=FONTS["body"], bg=COLORS["entry_bg"], fg=COLORS["entry_fg"]).pack(fill="x", padx=10)

        tk.Label(modal, text="Ingredients:", bg=COLORS["bg"], fg=COLORS["fg"], font=FONTS["body"]).pack(anchor="w", padx=10, pady=(10, 0))
        ingredients_text.pack(fill="both", expand=True, padx=10)

        tk.Label(modal, text="Instructions:", bg=COLORS["bg"], fg=COLORS["fg"], font=FONTS["body"]).pack(anchor="w", padx=10, pady=(10, 0))
        instructions_text.pack(fill="both", expand=True, padx=10)

        def save_changes():
            new_title = title_var.get().strip()
            new_ingredients = ingredients_text.get("1.0", "end-1c").strip()
            new_instructions = instructions_text.get("1.0", "end-1c").strip()

            if not new_title:
                messagebox.showerror("Error", "Title cannot be empty.")
                return

            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE recipes SET title = ?, ingredients = ?, instructions = ? WHERE id = ?",
                (new_title, new_ingredients, new_instructions, recipe_id)
            )
            conn.commit()
            conn.close()

            modal.destroy()
            self.load_recipes()
            self.recipe_display.delete("1.0", tk.END)
            messagebox.showinfo("Updated", f"'{new_title}' was updated.")

        save_btn = tk.Button(modal, text="Save", command=save_changes,
                             font=FONTS["button"], bg=COLORS["button"], fg=COLORS["fg"], **WIDGET_STYLE["button"])
        save_btn.pack(side="left", padx=20, pady=10)

        cancel_btn = tk.Button(modal, text="Cancel", command=modal.destroy,
                               font=FONTS["button"], bg=COLORS["button"], fg=COLORS["fg"], **WIDGET_STYLE["button"])
        cancel_btn.pack(side="right", padx=20, pady=10)

    def delete_recipe(self):
        selected = self.recipe_listbox.curselection()
        if not selected:
            return

        index = selected[0]
        recipe_id, title = self.recipes[index][0], self.recipes[index][1]

        confirm = messagebox.askyesno("Delete Recipe", f"Are you sure you want to delete '{title}'?")
        if not confirm:
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
        conn.commit()
        conn.close()

        self.recipe_display.delete("1.0", tk.END)
        self.load_recipes()
        self.delete_btn.config(state="disabled")
        self.edit_btn.config(state="disabled")
        messagebox.showinfo("Deleted", f"'{title}' has been deleted.")
