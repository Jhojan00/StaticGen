import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_several_children(self):
        child_node_1 = LeafNode("b", "child 1")
        child_node_2 = LeafNode("i", "child 2")
        child_node_3 = LeafNode(None, "child 3")

        parent_node = ParentNode("div", [child_node_1, child_node_2, child_node_3])

        self.assertEqual(
            parent_node.to_html(), "<div><b>child 1</b><i>child 2</i>child 3</div>"
        )

    def test_to_html_with_several_grandchildren(self):
        grandchild_node_1 = LeafNode("b", "grandchild 1")
        granchild_node_2 = LeafNode("i", "grandchild 2")

        grandchild_node_3 = LeafNode(None, "grandchild 3")
        grandchild_node_4 = LeafNode("span", "grandchild 4")

        child_node_1 = ParentNode("foo", [grandchild_node_1, granchild_node_2])
        child_node_2 = ParentNode("bar", [grandchild_node_3, grandchild_node_4])

        parent_node = ParentNode("div", [child_node_1, child_node_2])

        self.assertEqual(
            parent_node.to_html(),
            "<div><foo><b>grandchild 1</b><i>grandchild 2</i></foo>"
            "<bar>grandchild 3<span>grandchild 4</span></bar></div>",
        )

    def test_to_html_with_no_children(self):
        parent_node = ParentNode("p", None)
        self.assertRaises(ValueError, parent_node.to_html)

    def test_to_html_with_no_tag(self):
        child_node = LeafNode("p", "child")
        parent_node = ParentNode(None, [child_node])
        self.assertRaises(ValueError, parent_node.to_html)

    def test_to_html_with_props(self):
        child_node = LeafNode("b", "child")
        parent_node = ParentNode("span", [child_node], {"class": "material-icon-48"})

        self.assertEqual(
            parent_node.to_html(), '<span class="material-icon-48"><b>child</b></span>'
        )

    def test_to_html_with_children_props(self):
        child_node = LeafNode("a", "child", props={"href": "https://hello.world"})
        parent_node = ParentNode("span", [child_node], {"class": "material-icon-48"})

        self.assertEqual(
            parent_node.to_html(),
            '<span class="material-icon-48"><a href="https://hello.world">child</a></span>',
        )

    def test_to_html_with_several_grandchildren_props(self):
        grandchild_node_1 = LeafNode("b", "grandchild 1", {"grand": "true"})
        granchild_node_2 = LeafNode("i", "grandchild 2", {"grand": "true"})

        grandchild_node_3 = LeafNode(
            None, "grandchild 3", {"grand": "true"}
        )  # Props ignored by the leafnode.
        grandchild_node_4 = LeafNode("span", "grandchild 4", {"grand": "true"})

        child_node_1 = ParentNode(
            "foo", [grandchild_node_1, granchild_node_2], {"children": "true"}
        )
        child_node_2 = ParentNode(
            "bar", [grandchild_node_3, grandchild_node_4], {"children": "true"}
        )

        parent_node = ParentNode(
            "div", [child_node_1, child_node_2], {"parent": "true"}
        )

        self.assertEqual(
            parent_node.to_html(),
            '<div parent="true"><foo children="true"><b grand="true">grandchild 1</b><i grand="true">grandchild 2</i></foo>'
            '<bar children="true">grandchild 3<span grand="true">grandchild 4</span></bar></div>',
        )
