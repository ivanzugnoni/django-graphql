import graphene
from graphene import relay

from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene.utils.str_converters import to_snake_case

from library.models import Author, Book


class OrderedDjangoFilterConnectionField(DjangoFilterConnectionField):
    @classmethod
    def resolve_queryset(
        cls, connection, iterable, info, args, filtering_args, filterset_class
    ):
        qs = super(DjangoFilterConnectionField, cls).resolve_queryset(
            connection, iterable, info, args
        )
        filter_kwargs = {k: v for k, v in args.items() if k in filtering_args}
        qs = filterset_class(data=filter_kwargs, queryset=qs, request=info.context).qs

        order = args.get("orderBy", None)
        if order:
            if type(order) is str:
                snake_order = to_snake_case(order)
            else:
                snake_order = [to_snake_case(o) for o in order]
            qs = qs.order_by(*snake_order)
        return qs


class AuthorNode(DjangoObjectType):
    number_of_books = graphene.Int()

    class Meta:
        model = Author
        interfaces = (relay.Node,)
        fields = "__all__"
        filter_fields = {
            "id": ["exact", "icontains", "istartswith"],
            "name": ["exact", "icontains", "istartswith"],
        }


class BookNode(DjangoObjectType):
    class Meta:
        model = Book
        interfaces = (relay.Node,)
        filter_fields = {
            "id": ["exact", "icontains", "istartswith"],
            "name": ["exact", "icontains", "istartswith"],
        }


class Query(graphene.ObjectType):
    author = relay.Node.Field(AuthorNode)
    authors = OrderedDjangoFilterConnectionField(
        AuthorNode, orderBy=graphene.List(of_type=graphene.String)
    )
    book = relay.Node.Field(BookNode)
    books = OrderedDjangoFilterConnectionField(
        BookNode, orderBy=graphene.List(of_type=graphene.String)
    )


schema = graphene.Schema(query=Query)
