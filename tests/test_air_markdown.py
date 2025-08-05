"""Tests for `air_markdown` package."""

import mistletoe

from air_markdown import Markdown, TailwindTypographyMarkdown
from air_markdown.tags import AirMarkdown


def test_markdown_tag_h1():
    html = Markdown("# Hello, world").render()
    assert html == "<h1>Hello, world</h1>\n"


def test_markdown_h1_and_p():
    html = Markdown(
        """
# Hello, world

This is a paragraph.
"""
    ).render()
    assert html == "<h1>Hello, world</h1>\n<p>This is a paragraph.</p>\n"


def test_code_example():
    html = Markdown(
        """
# Code Example

```python
for i in range(5):
    print(i)
```
"""
    ).render()
    assert (
        html
        == '<h1>Code Example</h1>\n<pre><code class="language-python">for i in range(5):\n    print(i)\n</code></pre>\n'
    )


def test_custom_html_renderer():
    from air_markdown import Markdown as LocalMarkdown

    class CustomRenderer(mistletoe.HtmlRenderer):
        def render_strong(self, token: mistletoe.span_token.Strong) -> str:  # type: ignore
            template = '<strong class="superman">{}</strong>'
            return template.format(self.render_inner(token))

    LocalMarkdown.html_renderer = CustomRenderer  # type: ignore

    assert LocalMarkdown("**Hello, World**").render() == '<p><strong class="superman">Hello, World</strong></p>\n'


def test_custom_wrapper_dynamic_assignment():
    Markdown.wrapper = lambda self, x: f"<section>{x}</section>"  # type: ignore

    assert Markdown("# Big").render() == "<section><h1>Big</h1>\n</section>"


def test_TailwindTypographyMarkdown():
    html = TailwindTypographyMarkdown("# Tailwind support").render()
    assert html == '<article class="prose"><h1>Tailwind support</h1>\n</article>'


def test_air_markdown():
    html = AirMarkdown("# Heading into markdown").render()
    assert html == '<article class="prose"><h1>Heading into markdown</h1>\n</article>'


def test_air_markdown_airtag():
    html = AirMarkdown(
        """# Heading into air-live

```air-live
air.H2("Test")
```
"""
    ).render()
    assert html == '<article class="prose"><h1>Heading into air-live</h1>\n<h2>Test</h2>\n</article>'


def test_air_markdown_airtag_with_import():
    html = AirMarkdown(
        """# Heading into air-live

```air-live
import math
air.H2(f"Test {math.ceil(42.1)}")
```
"""
    ).render()
    assert html == '<article class="prose"><h1>Heading into air-live</h1>\n<h2>Test 43</h2>\n</article>'


def test_air_markdown_airtag_error():
    html = AirMarkdown(
        """# Heading into air-live

```air-live
air.H2("Test"
```
"""
    ).render()
    assert "Error rendering air-live block" in html


def test_air_markdown_airtag_empty():
    html = AirMarkdown(
        """# Heading into air-live

```air-live
```
"""
    ).render()
    assert html == '<article class="prose"><h1>Heading into air-live</h1>\n\n</article>'


def test_air_markdown_airtag_no_expression():
    html = AirMarkdown(
        """# Heading into air-live

```air-live
x = 1
```
"""
    ).render()
    assert html == '<article class="prose"><h1>Heading into air-live</h1>\n\n</article>'


def test_air_markdown_airtag_multiple_statements():
    html = AirMarkdown(
        """# Heading into air-live

```air-live
x = \"Hello\"
y = \"World\"
air.P(f"{x}, {y}!")
```
"""
    ).render()
    assert html == '<article class="prose"><h1>Heading into air-live</h1>\n<p>Hello, World!</p>\n</article>'


def test_air_markdown_airtag_not_air_tag():
    html = AirMarkdown(
        """# Heading into air-live

```air-live
"string"
```
"""
    ).render()
    assert html == '<article class="prose"><h1>Heading into air-live</h1>\n\n</article>'


def test_air_markdown_airtag_multiple_tags():
    markdown_content = """
# Multiple Tags
```air-live
air.H1(\"Title\")
air.P(\"This is a paragraph.\")
```
"""
    html = AirMarkdown(markdown_content).render()
    expected_html = (
        '<article class="prose"><h1>Multiple Tags</h1>\n<h1>Title</h1>\n<p>This is a paragraph.</p>\n</article>'
    )
    assert html == expected_html


def test_air_markdown_airtag_multiple_tags_with_logic():
    markdown_content = """
# Multiple Tags with Logic
```air-live
title = \"My Title\"
air.H1(title)
content = \"Some content.\"
air.P(content)
```
"""
    html = AirMarkdown(markdown_content).render()
    expected_html = (
        '<article class="prose"><h1>Multiple Tags with Logic</h1>\n<h1>My Title</h1>\n<p>Some content.</p>\n</article>'
    )
    assert html == expected_html
