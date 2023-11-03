# About
Simple sync/async client for REST API over JSON

PyPI: https://pypi.org/project/RESTModels/

# Usage
- install package
```shell
pip install RESTModels
```

- Create models
```python
from RESTModels import ResourceModel, SyncClient, get, post


class Model(ResourceModel):
    @get("/todos/{count}")
    def get_todos(self, count: int) -> list[str]:
        ...

    @post("/todo", body=("todo",))
    def make_todo(self, todo: str) -> None:
        ...
```

- Create instance and use it
```python
client = SyncClient("http://localhost:8000")
model = Model(client)
print(model.make_todo("Info"))
print(model.get_todos(1))
```

# More usage
## Custom type alias parsers
Create any object that implement protocol:
```python
class TypeParserProtocol(Protocol):
    def __call__(
            self,
            value: Any,
            alias: GenericAlias,
            alias_parser: "TypeAliasParser",
    ) -> Any:

        raise NotImplementedError
```

And register it as type alias parser for TypeAliasParser:

```python
from RESTModels import register_general_type_parser


@register_general_type_parser  # For all TypeAliasParser objects
def str_alias_parser(value: Any, alias: GenericAlias, alias_parser: TypeAliasParser) -> str:
    return str(value)

```

- value: response body as json.loads(request.body)
- alias: GenericAlias that describes expected result type
- alias_parser: TypeAliasParser object that called your type parser. Use it for parse nested types as showed lower.

You can parse generic types like that:
```python
@TypeAliasParser.register_general_type_parser
def list_alias_parser(value: Any, alias: GenericAlias, alias_parser: TypeAliasParser) -> list[Any]:
    if hasattr(alias, "__args__"):
        origin_type_alias = alias.__args__[0]
        return [alias_parser(elem, origin_type_alias) for elem in value]

    return list(value)
```
If your return type is generic, annotate it like Generic[Any] for static type checkers, as showed above

Type of value that type parser returns determined by return type annotation

If you register more than one parser for one type only last will be used

Make sure that return type annotation does not turn into the type you do not expect. Example:
```python
>>> Union[Any]
typing.Any
>>> Any | Any
typing.Any
```
