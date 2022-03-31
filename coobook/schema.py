import graphene
from graphene_django import DjangoObjectType
from ingredients.models import Category, Ingredient


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name", "ingredients")


class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "notes", "category")


class Query(graphene.ObjectType):
    all_ingredients = graphene.List(IngredientType)
    category_by_name = graphene.Field(CategoryType, name=graphene.String(required=True))

    def resolve_all_ingredients(root, info):
        return Ingredient.objects.select_related("category").all()

    def resolve_category_by_name(root, info, name):
        try:
            return Category.objects.get(name=name)
        except Category.DoesNoExist:
            return None


class MyAwesomeMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        notes= graphene.String(required=True)
        category = graphene.Int()

    ingredient = graphene.Field(IngredientType)
    @classmethod
    def mutate(cls, root, info, name, notes, category):
        ingredient = Ingredient.objects.create(
            name=name,
            notes=notes,
            category_id=category
        )
        return MyAwesomeMutation(ingredient=ingredient)

class Mutation(graphene.ObjectType):
    create_ingredient = MyAwesomeMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)