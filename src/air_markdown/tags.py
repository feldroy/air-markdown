"""Main module."""

import air
import mistletoe
# import pygments


# default_style = "colorful"
# formatter = pygments.HtmlFormatter(style=default_style, cssclass=default_style)
# default_style_definition = formatter.get_style_defs(f".{default_style}")


# class HighlightStyle(air.Tag):
#     def __init__(self, *args, **kwargs):
#         """Display the CSS needed for a tag.

#         Args:
#             *args: A style argument that matches what Pygments provides
#             **kwargs: Ignored (for consistency with Tag interface)
#         """
#         if len(args) == 0:
#             self.style_definition = default_style_definition
#         elif len(args) == 1:
#             self.style_definition = formatter.get_style_defs(f".{args[1]}")
#         else:
#             raise ValueError("HighlightStyle tag accepts only one string argument")
#         super().__init__('')    

#     def render(self) -> str:
#         """Render the string with the Markdown library."""
#         return air.Style(self.style_definition)
    


class Markdown(air.Tag):
    def __init__(self, *args, **kwargs):
        """Convert a Markdown string to HTML using mistletoe

        Args:
            *args: Should be exactly one string argument
            **kwargs: Ignored (for consistency with Tag interface)
        """
        if len(args) > 1:
            raise ValueError("Markdown tag accepts only one string argument")

        raw_string = args[0] if args else ""

        if not isinstance(raw_string, str):
            raise TypeError("Markdown tag only accepts string content")

        super().__init__(raw_string)

    def render(self) -> str:
        """Render the string with the Markdown library."""
        content = self._children[0] if self._children else ""
        return mistletoe.markdown(content, mistletoe.HtmlRenderer)
