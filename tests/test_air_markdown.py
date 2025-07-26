#!/usr/bin/env python
import pytest

"""Tests for `air_markdown` package."""


from air_markdown import Markdown


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
