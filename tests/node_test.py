import unittest
import json

from delta_trace_db.query.nodes.comparison_node import FieldEquals, FieldNotEquals, FieldGreaterThan, \
    FieldGreaterThanOrEqual, FieldLessThan, FieldLessThanOrEqual
from delta_trace_db.query.nodes.logical_node import AndNode, OrNode, NotNode
from delta_trace_db.query.nodes.query_node import QueryNode


class TestComparisonNodes(unittest.TestCase):

    def test_field_equals(self):
        node = FieldEquals('name', 'Alice')
        self.assertTrue(node.evaluate({'name': 'Alice'}))
        self.assertFalse(node.evaluate({'name': 'Bob'}))

    def test_field_not_equals(self):
        node = FieldNotEquals('age', 30)
        self.assertTrue(node.evaluate({'age': 25}))
        self.assertFalse(node.evaluate({'age': 30}))

    def test_field_greater_than(self):
        node = FieldGreaterThan('score', 80)
        self.assertTrue(node.evaluate({'score': 90}))
        self.assertFalse(node.evaluate({'score': 70}))

    def test_field_greater_than_or_equal(self):
        node = FieldGreaterThanOrEqual('score', 80)
        self.assertTrue(node.evaluate({'score': 80}))
        self.assertFalse(node.evaluate({'score': 79}))

    def test_field_less_than(self):
        node = FieldLessThan('score', 80)
        self.assertTrue(node.evaluate({'score': 70}))
        self.assertFalse(node.evaluate({'score': 90}))

    def test_field_less_than_or_equal(self):
        node = FieldLessThanOrEqual('score', 80)
        self.assertTrue(node.evaluate({'score': 80}))
        self.assertFalse(node.evaluate({'score': 81}))


class TestLogicalNodes(unittest.TestCase):

    def test_and_node(self):
        node = AndNode([FieldEquals('x', 1), FieldEquals('y', 2)])
        self.assertTrue(node.evaluate({'x': 1, 'y': 2}))
        self.assertFalse(node.evaluate({'x': 1, 'y': 3}))

    def test_or_node(self):
        node = OrNode([FieldEquals('x', 1), FieldEquals('y', 2)])
        self.assertTrue(node.evaluate({'x': 0, 'y': 2}))
        self.assertFalse(node.evaluate({'x': 0, 'y': 0}))

    def test_not_node(self):
        node = NotNode(FieldEquals('z', 5))
        self.assertFalse(node.evaluate({'z': 5}))
        self.assertTrue(node.evaluate({'z': 4}))


class TestQueryNode(unittest.TestCase):

    def test_query_node_mixed(self):
        query = AndNode([
            FieldEquals('type', 'user'),
            OrNode([FieldGreaterThan('age', 18), FieldEquals('role', 'admin')]),
        ])
        self.assertTrue(query.evaluate({'type': 'user', 'age': 20}))
        self.assertTrue(query.evaluate({'type': 'user', 'role': 'admin'}))
        self.assertFalse(query.evaluate({'type': 'user', 'age': 10}))
        self.assertFalse(query.evaluate({'type': 'bot', 'age': 30}))

    def test_nested_logical(self):
        query = NotNode(
            AndNode([FieldEquals('active', True), FieldLessThan('count', 5)])
        )
        self.assertFalse(query.evaluate({'active': True, 'count': 3}))
        self.assertTrue(query.evaluate({'active': False, 'count': 3}))
        self.assertTrue(query.evaluate({'active': True, 'count': 6}))

    def test_serialization_field_equals(self):
        node = FieldEquals('name', 'Alice')
        json_str = json.dumps(node.to_dict())
        restored = FieldEquals.from_dict(json.loads(json_str))
        self.assertTrue(restored.evaluate({'name': 'Alice'}))
        self.assertFalse(restored.evaluate({'name': 'Bob'}))

    def test_serialization_field_greater_than_or_equal(self):
        node = FieldGreaterThanOrEqual('score', 50)
        json_str = json.dumps(node.to_dict())
        restored = FieldGreaterThanOrEqual.from_dict(json.loads(json_str))
        self.assertTrue(restored.evaluate({'score': 60}))
        self.assertFalse(restored.evaluate({'score': 40}))

    def test_serialization_and_node(self):
        node = AndNode([FieldEquals('type', 'user'), FieldGreaterThan('age', 18)])
        json_str = json.dumps(node.to_dict())
        restored = AndNode.from_dict(json.loads(json_str))
        self.assertTrue(restored.evaluate({'type': 'user', 'age': 20}))
        self.assertFalse(restored.evaluate({'type': 'user', 'age': 10}))

    def test_serialization_not_or_node(self):
        node = NotNode(OrNode([FieldEquals('x', 1), FieldEquals('y', 2)]))
        json_str = json.dumps(node.to_dict())
        restored = NotNode.from_dict(json.loads(json_str))
        self.assertTrue(restored.evaluate({'x': 0, 'y': 0}))
        self.assertFalse(restored.evaluate({'x': 1, 'y': 0}))

    def test_serialization_complex_query_node(self):
        original = AndNode([
            FieldEquals('role', 'admin'),
            OrNode([FieldLessThan('logins', 5), FieldGreaterThan('age', 40)]),
        ])
        json_str = json.dumps(original.to_dict())
        decoded = json.loads(json_str)
        restored = AndNode.from_dict(decoded)
        self.assertTrue(restored.evaluate({'role': 'admin', 'logins': 2}))
        self.assertTrue(restored.evaluate({'role': 'admin', 'age': 45}))
        self.assertFalse(restored.evaluate({'role': 'admin', 'logins': 10, 'age': 30}))
        self.assertFalse(restored.evaluate({'role': 'user', 'logins': 2}))

    def test_from_dict_field_equals(self):
        original = FieldEquals('foo', 'bar')
        json_str = json.dumps(original.to_dict())
        restored = QueryNode.from_dict(json.loads(json_str))
        self.assertIsInstance(restored, FieldEquals)
        self.assertTrue(restored.evaluate({'foo': 'bar'}))

    def test_from_dict_nested_and_node(self):
        original = AndNode([FieldEquals('a', 1), FieldGreaterThan('b', 10)])
        json_str = json.dumps(original.to_dict())
        restored = QueryNode.from_dict(json.loads(json_str))
        self.assertIsInstance(restored, AndNode)
        self.assertTrue(restored.evaluate({'a': 1, 'b': 11}))
        self.assertFalse(restored.evaluate({'a': 1, 'b': 5}))

    def test_from_dict_complex_not_or_node(self):
        original = NotNode(OrNode([FieldEquals('x', True), FieldLessThan('y', 5)]))
        json_str = json.dumps(original.to_dict())
        restored = QueryNode.from_dict(json.loads(json_str))
        self.assertIsInstance(restored, NotNode)
        self.assertTrue(restored.evaluate({'x': False, 'y': 10}))  # NOT(FALSE OR FALSE) = TRUE
        self.assertFalse(restored.evaluate({'x': True, 'y': 10}))  # NOT(TRUE OR FALSE) = FALSE


if __name__ == '__main__':
    unittest.main()
