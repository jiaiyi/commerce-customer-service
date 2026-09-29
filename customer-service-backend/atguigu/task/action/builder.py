import importlib
import inspect
import pkgutil

from atguigu.task.action.base import Action
from atguigu.task.action.builtin.action_listen import ActionListen
from atguigu.task.action.builtin.action_response import ActionResponse
from atguigu.task.action.registry import ActionRegistry
from atguigu.task.action.runner import ActionRunner


def register_custom_action(registry:ActionRegistry):
    # 定义自定义action类的注册
    # 1.导入atguigu.task.action.custom包
    package = importlib.import_module("atguigu.task.action.custom")
    # 2.遍历包中的所有模块
    for __,name,is_pkg in pkgutil.iter_modules(package.__path__,prefix=f"{package.__name__}."):
        # 如果时包就跳过
        if is_pkg:
            continue
        module = importlib.import_module(name)
        # 3.获取模块中的所有类,只要父类时Action的类，且排除Action本身
        for __,obj in inspect.getmembers(module,inspect.isclass):
            if issubclass(obj,Action) and obj is not Action:
                registry.register(obj())

def register_builtin_actions(registry:ActionRegistry):
    registry.register(ActionResponse())
    registry.register(ActionListen())

def build_action_runner() ->ActionRunner:
    registry = ActionRegistry()
    # 注册内置Action（静态注册）
    register_builtin_actions(registry)
    # 注册自定义Action（通过扫包完成自定义Action的动态注册）
    register_custom_action(registry)
    return ActionRunner(registry)