import inspect
from typing import no_type_check

from aiogram.fsm.state import StatesGroup, StatesGroupMeta

from .field import InputFormField


class InputFormMeta(StatesGroupMeta):
    __states__: tuple[InputFormField, ...]

    @no_type_check
    def __new__(mcs, name, bases, namespace, **kwargs):
        cls = super(InputFormMeta, mcs).__new__(mcs, name, bases, namespace)

        states = []
        childs = []

        base: mcs = bases[0]
        for base_state in base:
            if isinstance(base_state, InputFormField):
                state_name = base_state.field_name
                state_copy = base_state.copy()
                state_copy.set_parent(cls)
                namespace[state_name] = state_copy

        for name, arg in namespace.items():
            if isinstance(arg, InputFormField):
                states.append(arg)
            elif inspect.isclass(arg) and issubclass(arg, InputForm):
                childs.append(arg)
                arg.__parent__ = cls

        cls.__parent__ = None
        cls.__childs__ = tuple(childs)
        cls.__states__ = tuple(states)
        cls.__state_names__ = tuple(state.state for state in states)

        cls.__all_childs__ = cls._get_all_childs()
        cls.__all_states__ = cls._get_all_states()

        return cls


class InputForm(StatesGroup, metaclass=InputFormMeta):
    @classmethod
    def first(cls) -> InputFormField:
        return cls.__states__[0]

    @classmethod
    def last(cls) -> InputFormField:
        return cls.__states__[-1]

    @classmethod
    def get_fields(cls):
        return cls.__states__

    def __len__(self):
        return len(self.get_fields())
