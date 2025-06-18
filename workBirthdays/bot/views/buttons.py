from aiogram_dialog import StartMode
from aiogram_dialog.widgets.kbd import Start, Cancel, Back, Next
from aiogram_dialog.widgets.text import Const

from workBirthdays.bot.states.start import MainMenuSG

__all__ = [
    "MAIN_MENU",
    "CANCEL",
    "BACK",
    "NEXT"
]

MAIN_MENU = Start(
    text=Const("Главное меню ☰"),
    id="__main__",
    state=MainMenuSG.state,
    mode=StartMode.RESET_STACK
)

CANCEL = Cancel(
    text=Const("Назад ◀")
)

BACK = Back(
    text=Const("Назад ◀")
)
NEXT = Next(
    text=Const("Вперед ▶")
)
