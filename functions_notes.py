from conn_sql import *
from os import system
from pathlib import Path
import os

rute = Path(os.path.expanduser("~/Desktop"))
rute_txt = Path(os.path.expanduser("~/Desktop/Personal_notes"))
#rute = Path(Path.home(), "workspace", "sqlalchemy")

#funcion del menu inicial del programa
def start():
    system("cls")
    print("*" * 38)
    print(" Welcome to our personal note system. ")
    print("*" * 38)

    opcion = "x"
    while not opcion.isnumeric() or int(opcion) not in range(1, 4):
        print("Please, choose a category from our selection menu")
        print('''
              [1] - Create Account
              [2] - Log In
              [3] - End Program
              ''')
        opcion = input("Choose a number between 1 and 3: ")
    return int(opcion)


#función para crear usuario y almacenar su información en la base de datos
def create_user():
    print("Please, follow the instructions to create an account.\n")
    while True:
        new_username = input("What is your User Name? ")
        if validate_user(new_username):
            break
        print("This User Name is already registred. Choose another one.")

    while True:
        print(""" The password must contain:
              At least one lower case.
              At least one upper case
              At least one number
              At least one symbol
              At least 6 character
              """)
        passwd = input("Enter your password: ")
        if validate_passwd(passwd):
            break
        print("Please, enter a validate password.\n")

    new_user = Person(username=new_username, password=passwd)
    session.add(new_user)
    session.commit()


#función para verificar que el User Name no exista en la base de datos
def validate_user(user):
    existing_user =  session.query(Person).filter_by(username=user).first()
    if existing_user:
        return False
    else:
        return True
    

#función para verificar 'manualmente' las caracteristicas que debe tener la contraseña
def validate_passwd(password):
    u_case = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    l_case = 'abcdefghijklmnopqrstuvwxyz'
    num = '0123456789'
    sym = "|°!#$%&/()=?¡*¨[_:;]^~@\~^,.-{+}¿'/"

    if not any(character in u_case for character in password):
        return False
    
    if not any(character in l_case for character in password):
        return False
    
    if not any(character in num for character in password):
        return False
    
    if not any(character in sym for character in password):
        return False

    if len(password) < 6:
        return False
    
    return True


#función para simular un inicio de sesión utilizando username y password
def login(username, passwd):
    user = session.query(Person).filter_by(username=username, password=passwd).first()
    if user:
        print(f'Welcome {user.username}')
        return user.person_id
    

#Función utilizada para mostrarle al usuario una vez que inicia sesión
#Posiblemente se le añada una función para poder eliminar usuario
def user_menu():
    exit_menu = 'x'
    while not exit_menu.isnumeric() or int(exit_menu) not in range(1, 4):
        print("Choose a category in the menu: ")
        print('''
            [1] - View Notes.
            [2] - Create Notes.
            [3] - Log Out.
            ''')
        exit_menu = input("Choose a number between 1 to 3 to proceed: ")
    return int(exit_menu)


#función utilizada para mostrarle al usuario las opciones de administración de notas
def user_note_menu():
    #view_notes(user_id)
    exit_menu = 'x'
    while not exit_menu.isnumeric() or int(exit_menu) not in range(1, 6):
        print("Choose a category in the menu: ")
        print('''
            [1] - Create Note.
            [2] - Edit Note.
            [3] - Delete Note
            [4] - Convert note to .txt file
            [5] - Exit.
            ''')
        exit_menu = input("Choose a number between 1 to 5 to proceed: ")
    return int(exit_menu)


#Esta función es utilizada en las demás funciones solamente para poder 
#ver las notas que ya estan creadas a través del titulo
def view_notes(user_id):
    user_notes = session.query(Notes).filter_by(owner=user_id).all()

    if not user_notes:
        print("No notes found")

    else:
        print("Your notes:\n")
        for note in user_notes:
            print(f"TITLE: {note.title}")
            print("-" * 20)

#función utilizada para leer las notas (titulo y descripción)
def read_notes(user_id):
    user_notes = session.query(Notes).filter_by(owner=user_id).all()

    if not user_notes:
        print("No notes found")

    else:
        print("Your notes:\n")
        for note in user_notes:
            print(f"TITLE:  {note.title}")
            print(f"DESCRIPTION:    {note.note}")
            print("-" * 20)


#función para crear notas nuevas y almacenarlas en la base de datos
#la base de datos almacena el DateTime Now en la base de datos
def create_note(user_id):
    view_notes(user_id)
    print("Creating a new note\n")

    while True:
        title_note = input("Enter a New Title: ")
        note_description = input("Enter a New Description: ")
        
        print(f"\nNEW TITLE.  {title_note}\nNEW DESCRIPTION.  {note_description}\n")
        confirmation = input("Are you sure you want to save new note? [Y] - [N]: ").upper()
        
        if confirmation == "Y":
                try:
                    new_note = Notes(owner=user_id, title=title_note, note=note_description)
                    session.add(new_note)
                    session.commit()
                    print("\n--NOTE SUCCESFULLY SAVED--")
                except Exception as Ex:
                    print(f"An error ocurred: {Ex}")
                break
        elif confirmation == "N":
            print("New note canceled")
            break
        else:
            print("Please enter the correct character to confirm")


#función para editar notas ya almacenadas enl a base de datos
def edit_note(user_id):
    view_notes(user_id)
    
    note_to_edit = input("Please, enter the title of the note you want to edit: ")
    note = session.query(Notes).filter_by(owner=user_id, title=note_to_edit).first()

    if note:
        print(f"Current Title:  {note.title}\n")
        new_title_note = input("Enter the new title (or press Enter to keep the current title): ")
        new_title_note = new_title_note if new_title_note else note.title

        print(f"Current Description:    {note.note}\n")
        new_description_note = input("Enter the new description (or press Enter to keep the current description): ")
        new_description_note = new_description_note if new_description_note else note.note

        print(f"\nNEW TITLE:  {new_title_note}")
        print(f"NEW DESCRIPTION:    {new_description_note}\n")

        confirmation = input("Are you sure you want to save the changes? [Y] - [N]: ").upper()

        if confirmation == "Y":
            try:
                note.title = new_title_note
                note.note = new_description_note
                session.commit()
                print("\n--NOTE SUCCESFULLY UPDATED--")
            except Exception as e:
                print(f"An error occurred: {e}")
        elif confirmation == "N":
            print("Editing canceled.")
        else:
            print("Invalid input. Please enter 'Y' to confirm or 'N' to cancel.")
    else:
        print("Note not found.")


#función para eliminar notas almacenadas en la base de datos
def delete_note(user_id):
    view_notes(user_id)
    note_to_delete = input("Please, enter the title of the note you want to delete: ")
    note = session.query(Notes).filter_by(owner=user_id, title=note_to_delete).first()

    if note:
        print(f"\nCurrent Title:    {note.title}")
        print(f"Current Description:    {note.note}\n")

        confirmation = input("Are you sure you want to delete the note? [Y] - [N]: ").upper()

        if confirmation == "Y":
            try:
                session.delete(note)
                session.commit()
                print("\n--NOTE SUCCESFULLY DELETED--")
            except Exception as e:
                print(f"An error occurred: {e}")
        elif confirmation == "N":
            print("Deletion canceled.")
        else:
            print("Invalid input. Please enter 'Y' to confirm or 'N' to cancel.")
    else:
        print("Note not found.")


#Con esta función puedes convertir las notas de la base de datos a archivo .txt
def convert_txt(user_id, rute):
    view_notes(user_id)

    note_to_convert = input("Please, enter the title of the note you want to convert: ")
    note = session.query(Notes).filter_by(owner=user_id, title=note_to_convert).first()

    if note:
        print(f"Title:  {note.title}")
        print(f"Description:    {note.note}")

        folder_name = "Personal_notes"
        folder_rute = Path(rute, folder_name)

        title_txt = note.title + ".txt"
        content_txt = note.note
        new_rute = Path(rute_txt, title_txt)

        try:
            if not os.path.exists(folder_rute):
                Path.mkdir(folder_rute)
                print("Your folder has been created succesfully.")
        except:
            pass

        try:
            if not new_rute.exists():
                new_rute.write_text(content_txt)
                print(f"Your file '{note.title}' has been converted to .txt")
            else:
                print("Sorry, this file already exists")
        except Exception as ex:
            print(f"An error occurred while converting to .txt: {ex}")
    else:
        print("Note not found.")


#función utilizada para volver al menú despues de una operación
def back_to_menu():
    choose_back = "s"

    while choose_back.lower() != "x":
        choose_back = input("\n Enter 'x' to go back: ")
