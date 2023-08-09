from gui.todo_app.views.todo_view import TodoView


class TodoController:
    def __init__(self) -> None:
        self.todo_view = TodoView(self)

    def on_add_todo(self) -> None:
        print('on add todo')

    def on_update_todo(self) -> None:
        print('on update todo')

    def on_delete_todo(self) -> None:
        print('on delete todo')

    def on_complete_todo(self) -> None:
        print('on complete todo')
