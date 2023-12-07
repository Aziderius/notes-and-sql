"""
An online note simulation program
"""
from functions_notes import *

#Programa principal 
finish_program = False

while not finish_program:
    menu = start()
    if menu == 1:
        my_user = create_user()
        back_to_menu()
    if menu == 2:
        user = input("Enter your User Name: ")
        passw = input("Enter your Password: ")
        user_login = login(user, passw)
        if user_login:

            exit = False
            while not exit:
                person_menu = user_menu()
                if person_menu == 1:
                    read_notes(user_login)

                    exit_note_menu = False
                    while not exit_note_menu:
                        note_person_menu = user_note_menu()
                        if note_person_menu == 1:
                            create_note(user_login)
                            back_to_menu()
                        elif note_person_menu == 2:
                            edit_note(user_login)
                            back_to_menu()
                        elif note_person_menu == 3:
                            delete_note(user_login)
                            back_to_menu()
                        elif note_person_menu == 4:
                            convert_txt(user_login, rute)
                            back_to_menu()
                        elif note_person_menu == 5:
                            exit_note_menu = True

                elif person_menu == 2:
                    create_note(user_login)
                    back_to_menu()
                elif person_menu == 3:
                    exit = True
        
    if menu == 3:
        print("Thanks for yous support using our system.")
        print("Come back later")
        finish_program = True
