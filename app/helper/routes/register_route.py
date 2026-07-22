import pkgutil
import importlib
from fastapi import FastAPI
import app.routes as routes

def register_route(app: FastAPI):
    for _, module_name, _ in pkgutil.iter_modules(routes.__path__):
        module = importlib.import_module(f"app.routes.{module_name}")

        if hasattr(module, "router"):
            app.include_router(module.router)