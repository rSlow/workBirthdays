from collections import defaultdict
from dataclasses import dataclass
from typing import Sequence

from dishka.dependency_source.factory import Factory
from dishka.entities.key import DependencyKey
from dishka.entities.scope import BaseScope, Scope
from dishka.registry import Registry


@dataclass
class DependencyClass:
    name: str
    provide: DependencyKey

    def __str__(self):
        return f"{self.name} ({self.provide.type_hint})"


@dataclass
class Component:
    provide: DependencyClass
    scope: BaseScope
    dependencies: Sequence[DependencyClass]


def dep_key_to_render_dependency(provide: DependencyKey):
    hint = provide.type_hint
    name = getattr(hint, "__name__", str(hint))
    return DependencyClass(name=name, provide=provide)


def factory_to_component(factory: Factory):
    return Component(
        provide=dep_key_to_render_dependency(factory.provides),
        scope=factory.scope,
        dependencies=[dep_key_to_render_dependency(dep) for dep in factory.dependencies]
    )


def render_dependency(dep: DependencyClass):
    return f"     | -> {dep}\n"


def render_component(component: Component):
    res = f"    {component.provide}\n"
    for dep in component.dependencies:
        res += render_dependency(dep)
    return res


def render_scope(scope: Scope, components: list[Component]):
    return (
            f"  Scope <{scope.value.name}>:\n" +
            "".join(render_component(component) for component in components) +
            "\n"
    )


def render(registries: list[Registry]):
    res = "DependencyDiagram\n"
    scopes = defaultdict(list[Component])

    for registry in registries:
        for factory in registry.factories.values():
            component = factory_to_component(factory)
            scopes[factory.scope].append(component)

    for scope, components in scopes.items():
        if components:
            res += render_scope(scope, components)

    return res.strip() + "\n"
