from typing import Optional

from PyQt5.QtWidgets import QDialog

from gui.todo_app.models.todo import Todo
from gui.todo_app.views.todo_form import TodoForm
from gui.todo_app.views.todo_list_view import TodoListView


class TodoController:
    def __init__(self, todo_list_view: TodoListView) -> None:
        self.todo_list_view = todo_list_view

    def add_todo_button_clicked(self) -> None:
        self.show_todo_form()

    def update_todo_button_clicked(self) -> None:
        index = self.todo_list_view.todo_table.currentIndex().row()
        if index >= 0:
            todo = Todo(
                self.todo_list_view.model.item(index, 0).text(),
                self.todo_list_view.model.item(index, 1).text(),
                self.todo_list_view.model.item(index, 2).text(),
                self.todo_list_view.model.item(index, 3).text() == "Yes",
            )
            self.show_todo_form(todo)

    def delete_todo_button_clicked(self) -> None:
        index = self.todo_list_view.todo_table.currentIndex().row()
        if index >= 0:
            todo_id = self.todo_list_view.model.item(index, 0).text()
            Todo.delete(todo_id)
            self.todo_list_view.remove_todo_from_view(index)

    def complete_todo_button_clicked(self) -> None:
        index = self.todo_list_view.todo_table.currentIndex().row()
        if index >= 0:
            todo_id = self.todo_list_view.model.item(index, 0).text()
            todo = Todo.update(todo_id)
            updated_todo = Todo.objects(todo.id)
            updated_todo.title = self.todo_list_view.model.item(index, 1).text()
            updated_todo.description = self.todo_list_view.model.item(index, 2).text()
            updated_todo.completed = True
            self.todo_list_view.update_todo_in_view(index, todo)

    def show_todo_form(self, todo: Optional[Todo] = None) -> None:
        todo_form = TodoForm(self, todo.title if todo else "", todo.description if todo else "")

        result = todo_form.exec()

        if result == QDialog.Accepted:
            title, description = todo_form.get_inputs()
            if todo is None:
                todo = Todo(title, description).save()
                self.todo_list_view.add_todo_to_view(todo)
            else:
                updated_todo = Todo.objects(todo.id)
                updated_todo.title = title
                updated_todo.description = description
                updated_todo.completed = todo.completed
                index = self.todo_list_view.todo_table.currentIndex().row()
                self.todo_list_view.update_todo_in_view(index, todo)

    def load_todos_from_database(self) -> None:
        for todo in Todo.objects:
            self.todo_list_view.add_todo_to_view(todo)
