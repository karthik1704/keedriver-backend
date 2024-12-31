# schema.py
from drf_spectacular.generators import SchemaGenerator


class CustomSchemaGenerator(SchemaGenerator):
    def get_endpoints(self, request=None):
        endpoints = super().get_endpoints(request)
        # Modify endpoint data here, adding tags as needed
        for path, path_data in endpoints.items():
            if "login" in path:
                for method in path_data["methods"].values():
                    method["tags"] = ["Auth"]
        return endpoints
