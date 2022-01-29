from pprint import pprint


class SymbolTable:
    class_identifiers = ["STATIC", "FIELD"]
    subroutine_identifiers = ["ARG", "VAR"]

    """Creates a new symbol table"""
    def __init__(self):
        self.class_table = {identifier: {} for identifier in self.class_identifiers}
        self.subroutine_table = {identifier: {} for identifier in self.subroutine_identifiers}

    """Starts (resets) the subroutine hash_table"""
    def start_subroutine(self):
        for key in self.subroutine_table:
            self.subroutine_table[key].clear()

    """defines a new identifier of the given name, type, kind and assigns it a running index"""
    def define(self, name, symbol_type, kind):
        kind = kind.upper()
        if kind in self.class_identifiers:  # STATIC and FIELD identifiers have a class scope
            self.class_table[kind][name] = (symbol_type, self.var_count(kind))
        else:  # ARG and VAR identifiers have a subroutine scope
            self.subroutine_table[kind][name] = (symbol_type, self.var_count(kind))

    """Returns the number of variables of a given kind already defined in the current scope"""
    def var_count(self, kind):
        kind = kind.upper()
        return len(self.class_table[kind]) \
            if kind in self.class_identifiers \
            else len(self.subroutine_table[kind])

    """Looks up the named identifier and returns an the requested attribute"""
    def look_up_named_id_attribute(self, name, attribute):
        for table in [self.class_table, self.subroutine_table]:
            for kind, named_ids in table.items():
                if named_ids.get(name):
                    attributes = {
                        "kind": kind,
                        "type": named_ids.get(name)[0],
                        "index": named_ids.get(name)[1]
                    }
                    return attributes[attribute]
        return None

    """Returns the kind of the named identifier in the current scope.
    If the identifier is unknown in the current scope, return None
    """
    def kind_of(self, name):
        return self.look_up_named_id_attribute(name, 'kind')

    """Returns the type of the named identifier in the current scope."""
    def type_of(self, name):
        return self.look_up_named_id_attribute(name, 'type')

    """Returns the index assigned to the named identifier"""
    def index_of(self, name):
        return self.look_up_named_id_attribute(name, 'index')


if __name__ == "__main__":
    symbol_table = SymbolTable()
    test_symbols = [
        ('x', 'int', 'FIELD'),
        ('y', 'int', 'FIELD'),
        ('pointCount', 'int', 'STATIC'),
        ('this', 'Point', 'ARG'),
        ('other', 'Point', 'ARG'),
        ('dx', 'int', 'VAR'),
        ('dy', 'int', 'VAR')
    ]
    for name, symbol_type, kind in test_symbols:
        symbol_table.define(name, symbol_type, kind)

    pprint(symbol_table.class_table)
    pprint(symbol_table.subroutine_table)
