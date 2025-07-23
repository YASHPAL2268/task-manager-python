import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import json
import os

DATA_FILE = "inventory.json"

class GroceryManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Grocery Inventory Manager")
        self.items = []
        self.load_items()

        self.create_widgets()
        self.refresh_listbox()

    def create_widgets(self):
        self.listbox = tk.Listbox(self.root, width=60)
        self.listbox.pack(pady=10)

        frame = tk.Frame(self.root)
        frame.pack()

        tk.Button(frame, text="Add Item", command=self.add_item).grid(row=0, column=0, padx=5)
        tk.Button(frame, text="Edit Item", command=self.edit_item).grid(row=0, column=1, padx=5)
        tk.Button(frame, text="Delete Item", command=self.delete_item).grid(row=0, column=2, padx=5)
        tk.Button(frame, text="Purchase", command=self.purchase_item).grid(row=0, column=3, padx=5)
        tk.Button(frame, text="Restock", command=self.restock_item).grid(row=0, column=4, padx=5)
        tk.Button(frame, text="Export Report", command=self.export_report).grid(row=0, column=5, padx=5)

        tk.Button(self.root, text="Inventory Summary", command=self.show_summary).pack(pady=5)

    def load_items(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as file:
                self.items = json.load(file)

    def save_items(self):
        with open(DATA_FILE, "w") as file:
            json.dump(self.items, file, indent=4)

    def refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for item in self.items:
            self.listbox.insert(tk.END, f"{item['name']} - ₹{item['price']} - Qty: {item['quantity']}")

    def get_selected_index(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "No item selected.")
            return None
        return selected[0]

    def add_item(self):
        name = simpledialog.askstring("Item Name", "Enter item name:")
        if not name:
            return
        try:
            quantity = int(simpledialog.askstring("Quantity", "Enter quantity:"))
            price = int(simpledialog.askstring("Price", "Enter price (₹):"))
        except:
            messagebox.showerror("Invalid Input", "Please enter valid numbers.")
            return

        self.items.append({"name": name, "quantity": quantity, "price": price})
        self.save_items()
        self.refresh_listbox()

    def edit_item(self):
        idx = self.get_selected_index()
        if idx is None:
            return

        item = self.items[idx]
        name = simpledialog.askstring("Edit Name", "Enter new name:", initialvalue=item['name'])
        try:
            quantity = int(simpledialog.askstring("Edit Qty", "Enter new quantity:", initialvalue=item['quantity']))
            price = int(simpledialog.askstring("Edit Price", "Enter new price (₹):", initialvalue=item['price']))
        except:
            messagebox.showerror("Invalid Input", "Please enter valid numbers.")
            return

        self.items[idx] = {"name": name, "quantity": quantity, "price": price}
        self.save_items()
        self.refresh_listbox()

    def delete_item(self):
        idx = self.get_selected_index()
        if idx is None:
            return
        del self.items[idx]
        self.save_items()
        self.refresh_listbox()

    def restock_item(self):
        idx = self.get_selected_index()
        if idx is None:
            return
        try:
            add_qty = int(simpledialog.askstring("Restock", "Enter quantity to add:"))
        except:
            messagebox.showerror("Invalid Input", "Please enter a number.")
            return
        self.items[idx]["quantity"] += add_qty
        self.save_items()
        self.refresh_listbox()

    def purchase_item(self):
        idx = self.get_selected_index()
        if idx is None:
            return
        if self.items[idx]["quantity"] > 0:
            self.items[idx]["quantity"] -= 1
        else:
            messagebox.showinfo("Out of Stock", "This item is out of stock.")
        self.save_items()
        self.refresh_listbox()

    def export_report(self):
        with open("inventory_report.txt", "w") as file:
            for item in self.items:
                file.write(f"{item['name']} - ₹{item['price']} - Qty: {item['quantity']}\n")
        messagebox.showinfo("Report", "Inventory report saved to inventory_report.txt")

    def show_summary(self):
        total_items = len(self.items)
        total_qty = sum(i['quantity'] for i in self.items)
        total_value = sum(i['quantity'] * i['price'] for i in self.items)
        messagebox.showinfo("Summary", f"Total Items: {total_items}\nTotal Quantity: {total_qty}\nTotal Value: ₹{total_value}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GroceryManagerApp(root)
    root.mainloop()
