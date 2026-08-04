class SchemaUtils:

    @staticmethod
    def infer_schema(data: dict):
        """
        Infer a simple schema from a dictionary.
        """

        schema = {}
        for key, value in data.items():
            schema[key] = type(value).__name__
            
        return schema