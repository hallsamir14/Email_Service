import markdown2
from pathlib import Path


class TemplateEngine:
    def __init__(self):
        # Resolve working directory
        working_dir = Path(__file__).resolve().parent

        # Resolve full path for email templates directory
        self.email_template_dir = working_dir / "email_templates"

    def __read_template(self, filename: str) -> str:
        """Private method to read template content."""
        template_path = self.email_template_dir / filename
        with open(template_path, "r", encoding="utf-8") as file:
            return file.read()

    def __apply_styles(self, html: str) -> str:
        """Apply advanced CSS styles inline for email compatibility with excellent typography."""
        styles: dict[str, str] = {
            "body": "font-family: Arial, sans-serif; font-size: 16px; color: #333333; background-color: #ffffff; line-height: 1.5;",
            "h1": "font-size: 24px; color: #333333; font-weight: bold; margin-top: 20px; margin-bottom: 10px;",
            "p": "font-size: 16px; color: #666666; margin: 10px 0; line-height: 1.6;",
            "a": "color: #0056b3; text-decoration: none; font-weight: bold;",
            "footer": "font-size: 12px; color: #777777; padding: 20px 0;",
            "ul": "list-style-type: none; padding: 0;",
            "li": "margin-bottom: 10px;",
        }

        # Wrap entire HTML content in <div> with body style
        styled_html = f'<div style="{styles["body"]}">{html}</div>'

        # Apply styles to each HTML element, except body
        for tag, style in styles.items():
            # Skip the body style since it's already applied to the <div>
            if tag != "body":
                styled_html = styled_html.replace(
                    f"<{tag}>", f'<{tag} style="{style}">'
                )
        return styled_html

    def render_template(self, template_name: str, **context) -> str:
        """Render a markdown template with given context, applying advanced email styles."""
        header = self.__read_template("header.md")
        footer = self.__read_template("footer.md")

        # Read main template and format it with provided context
        main_template = self.__read_template(f"{template_name}.md")
        main_content = main_template.format(**context)

        full_markdown = f"{header}\n{main_content}\n{footer}"
        html_content = markdown2.markdown(full_markdown)

        return self.__apply_styles(html_content)
