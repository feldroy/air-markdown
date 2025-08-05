"""Main module."""

import ast
import html

import air
import mistletoe
from mistletoe import block_token
from mistletoe.html_renderer import HtmlRenderer


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

    @property
    def html_renderer(self) -> type[mistletoe.HtmlRenderer]:
        """Override this to change the HTML renderer.

        Example:
            import mistletoe
            from air_markdown import Markdown

            class MyCustomRenderer(mistletoe.HtmlRenderer):
                # My customizations here

            Markdown.html_renderer = MyCustomRenderer

            Markdown('# Important title Here')
        """
        return mistletoe.HtmlRenderer

    def wrapper(self, content) -> str:
        """Override this method to handle cases where CSS needs it.

        Example:
            from air_markdown import Markdown

            class TailwindTypographyMarkdown(Markdown):
                def wrapper(self):
                    return f'<article class="prose">{content}</article>'


            Markdown('# Important title Here')
        """
        return content

    def render(self) -> str:
        """Render the string with the Markdown library."""
        content = self._children[0] if self._children else ""
        return self.wrapper(mistletoe.markdown(content, self.html_renderer))


class TailwindTypographyMarkdown(Markdown):
    def wrapper(self, content) -> str:
        return f'<article class="prose">{content}</article>'


class AirHTMLRenderer(HtmlRenderer):
    def render_block_code(self, token: block_token.BlockCode) -> str:
        """Render air-live code blocks as the executed output
        of calling the Air Tag's .render() method.

        For example:
        ```air-live
        air.H1("Title")
        air.P("Paragraph")
        ```
        will render as `<h1>Title</h1>\n<p>Paragraph</p>`
        """
        template = "<pre><code{attr}>{inner}</code></pre>"
        if token.language == "air-live":
            code = token.content.strip()
            if not code:
                return ""

            try:
                module = ast.parse(code)
                rendered_parts = []
                local_scope = {}  # Initialize local_scope here

                for node in module.body:
                    statement_module = ast.Module(body=[node], type_ignores=[])
                    if isinstance(node, ast.Expr):
                        # Evaluate expression and render if it's an Air Tag
                        expr_obj = compile(ast.Expression(body=node.value), "<string>", "eval")
                        # Ensure local_scope is passed to eval
                        result = eval(expr_obj, globals(), local_scope)
                        if isinstance(result, air.Tag):
                            rendered_parts.append(result.render())
                    else:
                        # Execute other statements (imports, assignments, etc.)
                        code_obj = compile(statement_module, "<string>", "exec")
                        # Ensure local_scope is passed to exec
                        exec(code_obj, globals(), local_scope)

                return "\n".join(rendered_parts)

            except Exception as e:
                error_message = f"Error rendering air-live block: {e}"
                inner = self.escape_html_text(f"{code}\n\n{error_message}")
                attr = ' class="language-air-live-error"'
                return template.format(attr=attr, inner=inner)

        elif token.language:
            attr = ' class="{}"'.format(f"language-{html.escape(token.language)}")
        else:
            attr = ""
        inner = self.escape_html_text(token.content)
        return template.format(attr=attr, inner=inner)


class AirMarkdown(Markdown):
    html_renderer = AirHTMLRenderer

    def wrapper(self, content) -> str:
        return f'<article class="prose">{content}</article>'
