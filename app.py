from tkinter import *
from tkinter import ttk,messagebox
from PIL import Image, ImageTk
import json
class ContactBook(Tk):
    def __init__(self):
        super().__init__()
        self.title("My Contacts")
        self.config(background="white", padx=20)
        self.minsize(width=1000, height=700)

        # Create canvas
        self.canvas = Canvas(self, width=100, height=100, highlightthickness=0)
        self.canvas.place(x=300, y=0)

        # Load and resize image
        self.image = Image.open("3.png")
        self.resized_image = self.image.resize((100, 100))

        # Convert to Tkinter image
        self.photo = ImageTk.PhotoImage(self.resized_image)

        # Set icon (must use PhotoImage)
        self.iconphoto(False, self.photo)

        # Place image on canvas
        self.canvas.create_image(50, 50, image=self.photo)

    def on_focus_in(self, event, entry, placeholder, underline):
        """When the entry box gets focus"""
        if entry.get() == placeholder:
            entry.delete(0, END)
            entry.config(fg="#2196F3")  # Change text color to blue
        underline.config(bg="#2196F3")  # Underline color to blue

    def on_focus_out(self, event, entry, placeholder, underline):
        """When the entry box loses focus"""
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(fg="grey")  # Set text color to grey
        underline.config(bg="grey")# Underline color back to grey


    def add_contact(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()

        # Only proceed if neither field is the placeholder
        if name != self.placeholder_name and phone != self.placeholder_phone:
            new_data = {name.lower():{
                "name":name, 
                "phone":phone}
            }

            # Try loading existing contacts, or start fresh
            if len(phone)!=10:
                messagebox.showerror("Invalid number","Please Enter a valid length number")                
            else:
                try:
                    with open("contacts.json", "r") as file:
                        data = json.load(file)
                        if not isinstance(data, dict):
                            data = {} # Reset if structure is wrong
                except (FileNotFoundError,json.JSONDecodeError):
                    data = {}

                # Update and save back to the same file
                data.update(new_data)
                with open("contacts.json", "w") as file:
                    json.dump(data, file, indent=4)

                messagebox.showinfo("Success", f"Contact '{name}' saved!")
        
        else:
            messagebox.showerror("Input Error", "None of the fields must be empty")
        self.load_contacts()
        self.name_entry.delete(0,END)
        self.phone_entry.delete(0,END)
        self.name_entry.insert(0,self.placeholder_name)
        self.phone_entry.insert(0,self.placeholder_phone)
    def delete_contact(self):
        selected_contact = self.contact_tree.selection()
        if not selected_contact:
            messagebox.showerror("No contact selected", "Select a contact to delete")
            return

        # Get selected item info
        item = self.contact_tree.item(selected_contact)
        name = item["values"][1]  # Assuming 2nd column is Name (key in your JSON)

        try:
            with open("contacts.json", "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            messagebox.showerror("Error", "No contact data found.")
            return

        if name in data:
            del data[name]  # Remove the contact by name
            with open("contacts.json", "w") as file:
                json.dump(data, file, indent=4)

            self.contact_tree.delete(selected_contact)
            messagebox.showinfo("Deleted", "Contact deleted successfully.")
        else:
            messagebox.showerror("Error", "Selected contact not found in file.")

    def load_contacts(self):
        """ Read contacts.json and populate the Treeview. """
        # 1) Clear existing rows
        for row in self.contact_tree.get_children():
            self.contact_tree.delete(row)

        # 2) Read from JSON
        try:
            with open("contacts.json", "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        # 3) Insert into Treeview
        for idx, (name, info) in enumerate(data.items(), start=1):
            name = info.get("name", "")
            phone = info.get("phone", "")
            self.contact_tree.insert(
                "",        # parent
                "end",     # position
                values=(idx, name, phone)
            )
          
    def search_contact(self):
        contact_name = self.search_entry_box.get().lower()
        phone_num = self.search_entry_box.get()
        if self.search_entry_box.get()!=self.placeholder_search:
            try:
                
                with open("contacts.json","r") as file:
                    data = json.load(file)
                    if contact_name in data:
                        phone = data[contact_name]["phone"]
                        messagebox.showinfo("contact found",f"Name:{contact_name}\nPhone{phone}")
        
                    else:
                        messagebox.showerror("Contact not found","No such contacts exist.")
            except FileNotFoundError:
                messagebox.showerror("Error!","File not found")
        else:
            messagebox.showerror("No input","Search a contact by Name")

    def setup_ui(self):
        self.my_contact_label = Label(text="My contacts", font=("Old Serif", 50, "bold"), fg="black", bg="white")
        self.my_contact_label.place(x=420, y=0)

        # Placeholder for search box (fixing incomplete line)
        self.placeholder_search = "Search a Contact"
        self.search_entry_box = Entry(self, bd=0, font=("Arial", 14), fg="grey", bg="white", insertbackground="#333")
        self.search_entry_box.place(x=10, y=150, height=25, width=450)
        self.search_entry_box.insert(0, self.placeholder_search)

        # Underline frame
        self.search_entry_box_underline = Frame(self, height=2, width=450, bg="grey")
        self.search_entry_box_underline.place(x=10, y=175)

        # Bind focus events to change the color
        self.search_entry_box.bind("<FocusIn>", lambda e: self.on_focus_in(e, self.search_entry_box, self.placeholder_search, self.search_entry_box_underline))
        self.search_entry_box.bind("<FocusOut>", lambda e: self.on_focus_out(e, self.search_entry_box, self.placeholder_search, self.search_entry_box_underline))

        # Search button
        self.search_button = ttk.Button(self, text="Search",command=self.search_contact)
        self.search_button.place(x=470, y=150)
        self.style = ttk.Style()
        self.style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
        self.style.configure("Treeview", font=("Arial", 11), rowheight=30)
        
        self.contact_tree = ttk.Treeview(self,columns=("Id","Name","Phone Number"),show="headings",height=500)
        self.contact_tree.heading("Id",text="Id")
        self.contact_tree.heading("Name",text="Name")
        self.contact_tree.heading("Phone Number",text="Phone Number")
        self.contact_tree.column("Id",width= 50,minwidth=50)
        self.contact_tree.column("Name",width=200,minwidth=200)
        self.contact_tree.column("Phone Number",width=300,minwidth=300)
        self.contact_tree.place(x=10,y=180)
        scrollbar = ttk.Scrollbar(self, orient=VERTICAL, command=self.contact_tree.yview)
        self.contact_tree.configure(yscrollcommand=scrollbar.set) 
        scrollbar.pack(side=RIGHT, fill=Y)

        self.save_button = ttk.Button(self, text="Save",width=50,command=self.add_contact)
        self.save_button.place(x=570, y=300)
        self.delete_button = ttk.Button(self, text="Delete",width=50,command=self.delete_contact)
        self.delete_button.place(x=570, y=330)
        
        # entry for writing the name of the contact 
        self.placeholder_name = "Enter a name"
        self.name_entry = Entry(self,font=("Arial",14),bd=0,fg="grey", bg="white", insertbackground="#333")
        self.name_entry.insert(0,self.placeholder_name)
        self.name_entry.place(x=570,y=180,width=300)
        self.name_entry_underline = Frame(self,height=2,width=300,bg="grey")
        self.name_entry_underline.place(x=570,y=205)
        self.name_entry.bind("<FocusIn>", lambda e: self.on_focus_in(e, self.name_entry, self.placeholder_name, self.name_entry_underline))
        self.name_entry.bind("<FocusOut>", lambda e: self.on_focus_out(e, self.name_entry, self.placeholder_name, self.name_entry_underline))


        # phone number entry box
        self.placeholder_phone = "Enter Number"
        self.phone_entry = Entry(self,font=("Arial",14),bd=0,fg="grey", bg="white", insertbackground="#333")
        self.phone_entry.insert(0,self.placeholder_phone)
        self.phone_entry.place(x=570,y=230,width=300)
        self.phone_entry_underline = Frame(self,height=2,width=300,bg="grey")
        self.phone_entry_underline.place(x=570,y=255)
        self.phone_entry.bind("<FocusIn>", lambda e: self.on_focus_in(e, self.phone_entry, self.placeholder_phone, self.phone_entry_underline))
        self.phone_entry.bind("<FocusOut>", lambda e: self.on_focus_out(e, self.phone_entry, self.placeholder_phone, self.phone_entry_underline))

    

# # Run the app
app = ContactBook()
app.setup_ui()
app.load_contacts()
app.mainloop()
