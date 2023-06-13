from invoke.context import Context
from invoke.tasks import task


@task
def send_information(ctx: Context) -> None:
    ctx.run("poetry run python bot/telegram/send_information.py")


@task
def build_ubuntu(ctx: Context) -> None:
    ctx.run(
        """
        cd bot/telegram
        poetry run pyinstaller --onefile --clean --paths ~/workspace/python_bot send_information.py
        """
    )


@task
def build_windows(ctx: Context) -> None:
    ctx.run(
        "poetry run pyinstaller --onefile --clean --noconsole "
        "bot\\telegram\\send_information.py && "
        "rmdir /s /q build && del /f send_information.spec"
    )
