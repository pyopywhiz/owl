from gui.todo_app.models.todo import Todo
from gui.todo_app.views.todo_list_view import TodoListView


class TodoListController:
    def __init__(self, todo_list_view: TodoListView):
        self.todo_list_view = todo_list_view

    def load_todos(self):
        self.todo_list_view.load_todos(Todo.objects)

    def on_data_changed(self, coordinate) -> None:
        row = coordinate.row()

        todo_id = self.todo_list_view.model.item(row, 0).text()
        todo = Todo.objects.get(id=todo_id)

        todo.title = self.todo_list_view.model.item(row, 1).text()
        todo.description = self.todo_list_view.model.item(row, 2).text()
        todo.completed = self.todo_list_view.model.item(row, 3).text() == "Yes"
        todo.save()

        self.todo_list_view.update_todo_in_view(row, todo)
