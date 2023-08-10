from PyQt5.QtWidgets import QDialog

from gui.todo_app.models.todo import Todo
from gui.todo_app.views.add_todo_view import AddTodoView
from gui.todo_app.views.edit_todo_view import EditTodoView
from gui.todo_app.views.todo_list_view import TodoListView
from gui.todo_app.views.todo_view import TodoView


class TodoController:
    def __init__(self, todo_view: TodoView, todo_list_view: TodoListView) -> None:
        self.todo_view = todo_view
        self.todo_list_view = todo_list_view

    def on_add_todo(self) -> None:
        add_todo_view = AddTodoView()
        result = add_todo_view.exec()
        if result == QDialog.Accepted:
            title, description = add_todo_view.get_inputs()
            todo = Todo(
                title=title,
                description=description
            )
            todo.save()
            self.todo_list_view.add_todo_to_view(todo)

    def on_update_todo(self) -> None:
        index = self.todo_list_view.todo_table.currentIndex().row()
        if index >= 0:
            todo_id = self.todo_list_view.model.item(index, 0).text()
            title = self.todo_list_view.model.item(index, 1).text()
            description = self.todo_list_view.model.item(index, 2).text()

            edit_todo_view = EditTodoView(title, description)
            result = edit_todo_view.exec()
            if result == QDialog.Accepted:
                new_title, new_description = edit_todo_view.get_inputs()
                todo = Todo.objects.get(id=todo_id)
                todo.title = new_title
                todo.description = new_description
                todo.save()
                self.todo_list_view.update_todo_in_view(index, todo)

    def on_delete_todo(self) -> None:
        index = self.todo_list_view.todo_table.currentIndex().row()
        if index >= 0:
            todo_view = self.todo_list_view.model.takeRow(index)
            Todo.objects.get(id=todo_view[0].text())

    def on_complete_todo(self) -> None:
        index = self.todo_list_view.todo_table.currentIndex().row()
        if index >= 0:
            todo_id = self.todo_list_view.model.item(index, 0).text()
            todo = Todo.objects.get(id=todo_id)
            todo.completed = not todo.completed
            todo.save()
            self.todo_list_view.model.item(index, 3).setText("Yes" if todo.completed else "No")
