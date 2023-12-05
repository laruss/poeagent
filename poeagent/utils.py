import importlib.resources as pkg_resources


def get_resource(resource) -> str:
    with pkg_resources.open_text("main", resource) as f:
        return f.read()
