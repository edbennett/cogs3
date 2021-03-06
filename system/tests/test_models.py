from django.test import TestCase

from system.models import System


class SystemTests(TestCase):

    @classmethod
    def create_system(cls, name, description, number_of_cores):
        """
        Create a System instance.

        Args:
            name (str): Name of the system.
            description (str): A short description of the system.
            number_of_cores (int): The number of cores available on the system.
        """
        return System.objects.create(
            name=name,
            description=description,
            number_of_cores=number_of_cores,
        )

    def test_system_creation(self):
        """
        Ensure we can create a System instance.
        """
        name = 'Nemesis'
        description = 'Bangor University Cluster'
        number_of_cores = 10000
        system = self.create_system(
            name=name,
            description=description,
            number_of_cores=number_of_cores,
        )
        self.assertTrue(isinstance(system, System))
        self.assertEqual(system.__str__(), system.name)
        self.assertEqual(system.name, name)
        self.assertEqual(system.description, description)
        self.assertEqual(system.number_of_cores, number_of_cores)
