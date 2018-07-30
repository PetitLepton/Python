'''
The module provides the class Documentation to transform a
Markdown file into an HTML one.

It transforms the path to images into base64 inserts make
the HTML file standalone.'''
from pathlib import Path
import base64
import jinja2
import markdown
from bs4 import BeautifulSoup


TEMPLATE = '''
<html>
    <head>
    </head>
    <body>
        <div class="container">
        {{content}}
        </div>
    </body>
</html>'''


def extract_images_paths(html_doc, parent=None):
    '''This function extract the paths of images
    from an HTML document.

    Args:
        html_doc (str): the HTML document
        image_folder (Path, default: None): the parent path for the
            images if those are only relative

    Returns:
        list of paths (str)'''
    soup = BeautifulSoup(html_doc, 'lxml')
    images_paths = [image['src'] for image in soup.findAll('img')]
    images_full_paths = dict()
    if parent:
        for image_path in images_paths:
            if image_path.startswith('./'):
                image_full_path = str(parent / image_path)
            else:
                image_full_path = image_path
            images_full_paths[image_path] = image_full_path
    return images_full_paths


def to_base_64(file_path):
    '''This function transforms an image path into a base64 string
    of the pointed file.

    Args:
        file_path (str)

    Returns:
        string containg the HTML src tag in the base64 format'''
    path = Path(file_path)
    extension = path.suffix.replace('.', '')
    bytes_string = path.read_bytes()
    base64_string = 'data:image/{};base64, {}'.format(
        extension,
        base64.b64encode(bytes_string).decode('utf-8'))
    return base64_string


class Documentation:
    '''This class implements the conversion of Markdown files into their
    HTML counterparts as a standalone file, including images treating in
    the base64 format.'''

    def __init__(self, md_path, html_path=None):
        path = Path(md_path)
        self.md_path = path
        self.md_name = path.name
        self.folder = path.parent
        self.html_name = path.name.replace('.md', '.html')
        self.html_path = html_path if html_path else self.folder / self.html_name

    def to_html(self, template_path=None):
        '''This method transforms the Markdown text into
        an HTML one. If the text contains links to images,
        the function transforms the images into base64
        counterparts and include them in the document.

        Args:
            template_path (str, default: None): path to the Jinja2 template
                for the HTML file. I no path is given, the HTML file is bare
        '''
        md_content = self.md_path.read_text()
        html_content = markdown.markdown(
            text=md_content,
            extensions=['markdown.extensions.extra'],
            output_format='html5')

        template = Path(template_path).read_text() if template_path else TEMPLATE
        html_doc = jinja2.Template(template).render(content=html_content)

        images_full_paths = extract_images_paths(html_doc, self.folder)
        print(self.folder)
        for image_path, image_full_path in images_full_paths.items():
            base64_image = to_base_64(image_full_path)
            html_doc = html_doc.replace(image_path, base64_image)

        return html_doc
