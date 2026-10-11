class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str] | None = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def props_to_html(self) -> str:
        if not self.props:
            return ""
        result = ""
        for k, v in self.props.items():
            result += f' {k}="{v}"'

        return result

    def to_html(self) -> str:
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
