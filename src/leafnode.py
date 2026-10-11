from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        value: str,
        props: dict[str, str] | None = None,
    ):
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("A leaf node cannot be None.")

        if self.tag is None:
            return self.value

        props = self.props_to_html()

        result = f"<{self.tag}{props}>{self.value}</{self.tag}>"

        return result

    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
