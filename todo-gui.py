import functions
import PySimpleGUI as sg
import time
import os

if not os.path.exists("todos.txt"):
    with open("todos.txt", 'w') as file:
        pass

sg.theme('DarkGrey6')

clock = sg.Text("", key='clock')
label = sg.Text("Enter Your Task")
input_box = sg.InputText(tooltip="Enter Tasks", key='todo')
add_button = sg.Button("Add Task")
display_list = sg.Listbox(values=functions.get_todos(), key='todos',
                          enable_events=True, size=[44,10])
edit_button = sg.Button("Update")
complete_button = sg.Button('Complete')
exit_button = sg.Button('Exit')
label_ver = sg.Text("Version: 1.0.1", font=('Arial', 10))

window = sg.Window('ToDo App',
                   icon='favicon.ico',
                   resizable=False,
                   layout=[[label],
                           [input_box, add_button],
                           [display_list, edit_button, complete_button],
                           [exit_button, clock],
                           [label_ver]],
                   font=("Helvetica",14))

while True:
    event, values = window.read(timeout=1000)
    window['clock'].update(value=time.strftime("%d %B %Y, %I:%M %p"))
    match event:
        case 'Add Task':
            todos = functions.get_todos()
            new_todo = values['todo'] + '\n'
            if new_todo.strip() == "":
                sg.popup("Empty field. Add a task.", icon='favicon.ico')
            else:
                todos.append(new_todo)
                functions.write_todos(todos)
                window['todos'].update(todos)
                window['todo'].update(value='')

        case 'Update':
            try:
                todo_edit = values['todos'][0]
                new_todo = values['todo']
                todos = functions.get_todos()
                index = todos.index(todo_edit)
                todos[index] = new_todo
                functions.write_todos(todos)
                window['todos'].update(values=todos)
                window['todo'].update(value='')
            except IndexError:
                sg.popup("Select a task to update.", icon='favicon.ico')

        case 'Complete':
            try:
                to_complete = values['todos'][0]
                todos = functions.get_todos()
                todos.remove(to_complete)
                functions.write_todos(todos)
                window['todos'].update(values=todos)
                window['todo'].update(value='')
            except IndexError:
                sg.popup("Select a task to complete.", icon='favicon.ico')

        case 'todos':
            try:
                window['todo'].update(value=values['todos'][0])
            except:
                sg.popup("Add an item to update.", icon='favicon.ico')

        case 'Exit':
            break

        case sg.WIN_CLOSED:
            break

window.close()