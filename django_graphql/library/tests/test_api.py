import json

from django.core.management import call_command
from graphene_django.utils.testing import GraphQLTestCase

from library.models import Author, Book


class AuthorsTestCase(GraphQLTestCase):
    def setUp(self):
        call_command("loaddata", "initial_data.json")
        super().setUp()

    def test_authors_list(self):
        """Should return the list of all authors"""
        # preconditions
        self.assertEqual(Author.objects.count(), 2)

        response = self.query(
            """
            query {
                authors {
                    edges {
                        node {
                            id
                            name
                            slug
                            created
                            modified
                            numberOfBooks
                        }
                    }
                }
            }
            """
        )
        content = json.loads(response.content)

        # postconditions
        self.assertResponseNoErrors(response)
        self.assertEqual(len(content["data"]["authors"]["edges"]), 2)

    def test_authors_filter(self):
        """Should return the author with given name"""
        response = self.query(
            """
            query authors($name: String!){
                authors(name: $name) {
                    edges {
                        node {
                            id
                            name
                            slug
                            created
                            modified
                            numberOfBooks
                        }
                    }
                }
            }
            """,
            variables={"name": "J. K. Rowling"},
        )
        content = json.loads(response.content)

        # postconditions
        self.assertResponseNoErrors(response)
        self.assertEqual(len(content["data"]["authors"]), 1)
        self.assertEqual(
            content["data"]["authors"]["edges"][0]["node"]["name"], "J. K. Rowling"
        )
