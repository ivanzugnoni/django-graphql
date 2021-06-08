import uuid

import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene.utils.str_converters import to_snake_case

from library.models import Author, Book


# NOTE: This class is kind of a hack because Ordering AND Filtering
# were not working together. Probably this will be resolved in
# future versions of graphene framework
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


class CreateAuthorMutation(graphene.Mutation):
    class Arguments:
        id = graphene.UUID()
        name = graphene.String(required=True)

    author = graphene.Field(AuthorNode)

    @classmethod
    def mutate(cls, root, info, name):
        author = Author.objects.create(name=name)
        return CreateAuthorMutation(author=author)


class UpdateAuthorMutation(graphene.Mutation):
    class Arguments:
        id = graphene.UUID(required=True)
        name = graphene.String(required=True)

    author = graphene.Field(AuthorNode)

    @classmethod
    def mutate(cls, root, info, name, id):
        author = Author.objects.get(id=id)
        author.name = name
        author.save()
        return UpdateAuthorMutation(author=author)


class DeleteAuthorMutation(graphene.Mutation):
    class Arguments:
        id = graphene.UUID(required=True)

    author = graphene.Field(AuthorNode)

    @classmethod
    def mutate(cls, root, info, id):
        Author.objects.get(id=id).delete()
        return DeleteAuthorMutation()


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


class Mutation(graphene.ObjectType):
    create_author = CreateAuthorMutation.Field()
    update_author = UpdateAuthorMutation.Field()
    delete_author = DeleteAuthorMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
