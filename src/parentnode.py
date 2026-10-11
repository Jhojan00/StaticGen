from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(
        self, tag: str, children: list[HTMLNode], props: dict[str, str] | None = None
    ):
        super().__init__(tag, children=children, props=props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("ParentNode cannot have a None tag.")

        if self.children is None:
            raise ValueError("ParentNode must have children.")

        props = self.props_to_html()
        children_html = [child.to_html() for child in self.children]

        result = f"<{self.tag}{props}>{''.join(children_html)}</{self.tag}>"

        return result
