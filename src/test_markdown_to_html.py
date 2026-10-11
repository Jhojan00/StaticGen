import unittest

from markdown_to_html import markdown_to_html_node


class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_heading(self):
        md = """
# This is a H1

## This is a H2

### This is a H3

#### This is a H4

##### This is a H5

###### This is a H6

####### This is a p:(
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a H1</h1><h2>This is a H2</h2><h3>This is a H3</h3><h4>This is a H4</h4><h5>This is a H5</h5><h6>This is a H6</h6><p>####### This is a p:(</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_blockquote(self):
        md = """
> _Ladies_ and **gentlemen**
> I hope everybody is 
> having a `great` time
> - somebody
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote><i>Ladies</i> and <b>gentlemen</b> I hope everybody is having a <code>great</code> time - somebody</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- Tomatoes.
- Potatos.
- Beans.  
-   Rice.
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Tomatoes.</li><li>Potatos.</li><li>Beans.</li><li>Rice.</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. Tomatoes.
2. Potatos.
3. Beans.  
4.   Rice.
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Tomatoes.</li><li>Potatos.</li><li>Beans.</li><li>Rice.</li></ol></div>",
        )

    def test_empty_markdown(self):
        md = """



"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div></div>")

    def test_all_blocks(self):
        md = """
# Python is _cool_

Python... ![actual python](https://real_python.png)
Not that one, this one [python](https://www.python.org).

A `Python` example would be:

```
print("Hello, world")
raise Exception("An error, already?")
```

## Features

This **language** supports:

- Funcional programming.
- OOP.
- Procedural programming.

## Writing a script

1. Download Python for your OS (Linux is just **better**).
2. Create file ending with the .py extention.
3. Write `raise Exception("Hello world")`.
4. Run the script with `python your_script.py`.
5. Enjoy.


> Thank you.
> The tester.
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div>"
            "<h1>Python is <i>cool</i></h1>"
            '<p>Python... <img src="https://real_python.png" alt="actual python"></img> '
            'Not that one, this one <a href="https://www.python.org">python</a>.</p>'
            "<p>A <code>Python</code> example would be:</p>"
            '<pre><code>print("Hello, world")\n'
            'raise Exception("An error, already?")\n'
            "</code></pre>"
            "<h2>Features</h2>"
            "<p>This <b>language</b> supports:</p>"
            "<ul>"
            "<li>Funcional programming.</li>"
            "<li>OOP.</li>"
            "<li>Procedural programming.</li>"
            "</ul>"
            "<h2>Writing a script</h2>"
            "<ol>"
            "<li>Download Python for your OS (Linux is just <b>better</b>).</li>"
            "<li>Create file ending with the .py extention.</li>"
            '<li>Write <code>raise Exception("Hello world")</code>.</li>'
            "<li>Run the script with <code>python your_script.py</code>.</li>"
            "<li>Enjoy.</li>"
            "</ol>"
            "<blockquote>Thank you. The tester.</blockquote>"
            "</div>",
        )
