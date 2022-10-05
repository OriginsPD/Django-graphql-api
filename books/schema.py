import graphene
from graphene_django import DjangoObjectType
from books.models import Book


class BookType(DjangoObjectType):
    class Meta:
        model = Book
        fields = "__all__"

# Queries


class Query(graphene.ObjectType):
    all_books = graphene.List(BookType)
    book = graphene.Field(BookType, id=graphene.Int())
    book_by_title = graphene.List(
        BookType, title=graphene.String(required=True))

    def resolve_all_books(self, info, **kwargs):
        return Book.objects.all()

    def resolve_book(self, info, id):
        return Book.objects.get(pk=id)

    def resolve_book_by_title(self, info, title):
        try:
            return Book.objects.filter(title=title)
        except Book.DoesNotExist:
            return None


class BookInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String()
    author = graphene.String()
    year_published = graphene.String()
    review = graphene.Int()

# Mutations


class CreateBook(graphene.Mutation):
    class Arguments:
        data = BookInput(required=True)

    book = graphene.Field(BookType)

    @staticmethod
    def mutate(root, info, data=None):
        book_instance = Book(
            title=data.title,
            author=data.author,
            year_published=data.year_published,
            review=data.review
        )
        book_instance.save()
        return CreateBook(book=book_instance)


class UpdateBook(graphene.Mutation):
    class Arguments:
        data = BookInput(required=True)

    book = graphene.Field(BookType)

    @staticmethod
    def mutate(root, info, data=None):

        book_instance = Book.objects.get(pk=data.id)

        if book_instance:
            book_instance.title = data.title
            book_instance.author = data.author
            book_instance.year_published = data.year_published
            book_instance.review = data.review
            book_instance.save()

            return UpdateBook(book=book_instance)
        return UpdateBook(book=None)


class DeleteBook(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    book = graphene.Field(BookType)

    @staticmethod
    def mutate(root, info, id):
        book_instance = Book.objects.get(pk=id)
        book_instance.delete()

        return None


# Registering The Methods Created
class Mutation(graphene.ObjectType):
    create_book = CreateBook.Field()
    update_book = UpdateBook.Field()
    delete_book = DeleteBook.Field()


# Schema
schema = graphene.Schema(query=Query, mutation=Mutation)
