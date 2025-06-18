from aiogram.fsm.state import StatesGroup, State

from workBirthdays.bot.utils.states_factory import FSMSingleFactory

AdminMainSG = FSMSingleFactory("AdminMainSG")


class RoleManagerStartSG(StatesGroup):
    main = State()
    list = State()


class RoleCreateSG(StatesGroup):
    alias = State()
    name = State()


class RoleSG(StatesGroup):
    main = State()
    delete = State()
    add_user = State()
    users = State()
    accept_delete_user = State()


class AddUserToRoleSG(StatesGroup):
    input = State()
    accept = State()
