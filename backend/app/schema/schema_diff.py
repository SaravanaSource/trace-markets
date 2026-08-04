class SchemaDiff:

    @staticmethod
    def compare(old_schema:dict, new_schema:dict):

        added = []
        removed = []
        changed =[]

        for field in new_schema:
            if field not in old_schema:
                added.append(field)

            elif old_schema[field] != new_schema[field] :
                changed.append(field)

        for field in old_schema:
            if field not in new_schema:
                removed.append(field)

        return {
            "added":added,
            "removed": removed,
            "changed": changed
        }