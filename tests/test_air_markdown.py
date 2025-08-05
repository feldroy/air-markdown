"""Tests for `air_markdown` package."""

import mistletoe


from air_markdown import Markdown, TailwindTypographyMarkdown
from air_markdown.tags import AirMarkdown


def test_markdown_tag_h1():
    html = Markdown("# Hello, world").render()
    assert html == '<h1>Hello, world</h1>\n'


def test_markdown_h1_and_p():
    html = Markdown("""
# Hello, world

This is a paragraph.    
""").render()
    assert html == '<h1>Hello, world</h1>\n<p>This is a paragraph.</p>\n'


def test_code_example():
    html = Markdown("""
# Code Example

```python
for i in range(5):
    print(i)
```
""").render()
    assert html == '<h1>Code Example</h1>\n<pre><code class="language-python">for i in range(5):\n    print(i)\n</code></pre>\n'

def test_custom_html_renderer():

    from air_markdown import Markdown as LocalMarkdown

    class CustomRenderer(mistletoe.HtmlRenderer):
        def render_strong(self, token: mistletoe.span_token.Strong) -> str:
            template = '<strong class="superman">{}</strong>'
            return template.format(self.render_inner(token))  

    LocalMarkdown.html_renderer = CustomRenderer

    assert LocalMarkdown('**Hello, World**').render() == '<p><strong class="superman">Hello, World</strong></p>\n'

def test_custom_wrapper_dynamic_assignment():
    Markdown.wrapper = lambda self, x: f'<section>{x}</section>'   

    assert Markdown('# Big').render() == '<section><h1>Big</h1>\n</section>'

def test_TailwindTypographyMarkdown():
    html = TailwindTypographyMarkdown('# Tailwind support').render()
    assert html == '<article class="prose"><h1>Tailwind support</h1>\n</article>'

def test_air_markdown():
    html = AirMarkdown("""# Heading into markdown""").render()
    assert html == '<section><h1>Heading into markdown</h1>\n</section>'

def test_air_markdown_airtag():
    html = AirMarkdown("""# Heading into airtag_rendered

```airtag_rendered
print(air.H2("Test").render())
```
""").render()
    assert html == '<section><h1>Heading into airtag_rendered</h1>\n<h2>Test</h2>\n\n</section>'

def test_air_markdown_airtag_with_import():
    html = AirMarkdown("""# Heading into airtag_rendered

```airtag_rendered
import math
print(air.H2(f"Test {math.ceil(42.1)}").render())
```
""").render()
    assert html == '<section><h1>Heading into airtag_rendered</h1>\n<h2>Test 43</h2>\n\n</section>'
