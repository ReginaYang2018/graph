__author__ = 'Mengyao Yang'
import unittest
import main

# unit test frame provided by python unittest
class TestStringMethods(unittest.TestCase):
    testA = main.Entity(1, 'testA', 'this is A')
    testB = main.Entity(2, 'testB', 'this is B', [testA])
    testA.goes_to = [testB]

    id_map = {1: testA, 2: testB}
    links = [main.Link(1, 2), main.Link(2, 1)]

    # use the symmetric property to test in and out parse
    def test_parser(self):

        test_data = main.output_parser(self.id_map, self.links)
        re_map, re_list = main.input_parser(test_data)

        self.assertEqual(len(re_map), len(self.id_map))
        self.assertEqual(len(re_list), len(self.links))
        self.assertEqual(max(re_map.keys()), max(self.id_map.keys()))
        self.assertEqual(min(re_map.keys()), min(self.id_map.keys()))

    # test the clone function
    def test_clone(self):
        cloned_map, cloned_list = main.clone(self.id_map, self.links, 1)
        self.assertTrue(len(cloned_map) == 4)
        self.assertTrue(len(cloned_list) == 5)
        self.assertTrue(max(cloned_map.keys()) == 10002)
        pass


if __name__ == '__main__':
    unittest.main()