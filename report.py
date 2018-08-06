'''
The module provides the class Report to transform a
notebook into an HTML report. It is based on
http://nbconvert.readthedocs.io/en/latest/execute_api.html.

It contains methods for executing a notebook, transforming
the result into an HTML file and clean the file from
non-mandatory HTML elements.'''
from pathlib import Path
import codecs
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert import HTMLExporter
import jinja2
from bs4 import BeautifulSoup


class Report:
    '''The class handles the execution of notebooks and their
    transformation into HTML reports.

    Args:
        notebook_path (str): full path to the genuine notebook
        reports_folder (str): full path to the final report repository'''

    def __init__(self, notebook_path, report_folder):
        self.notebook_path = notebook_path
        path = Path(notebook_path)
        self.notebook_folder = str(path.parent)
        self.notebook = path.name
        self.temporary_notebook = Path('/tmp') / path.name
        self.report_path = Path(report_folder) / path.name.replace('ipynb', 'html')
        self.title = path.name.replace('.ipynb', '').replace('_', ' ')

    def execute_notebook(self, version=4, timeout=3600):
        '''The method executes the notebook.

        Args:
            version (int, default: 4): the version of the notebook
                (as_version parameter from nbformat.read)
            timeout (int, default: 3600): timeout for the cell execution'''
        try:
            notebook = nbformat.read(self.notebook_path, as_version=version)
        except FileNotFoundError as e:
            raise e

        kernel_name = notebook['metadata']['kernelspec']['name']
        ep = ExecutePreprocessor(timeout=timeout, kernel_name=kernel_name)
        ep.preprocess(notebook, dict(metadata=dict(path=self.notebook_folder)))

        nbformat.write(notebook, str(self.temporary_notebook))

    def notebook_to_report(self, version=4, template_path=None):
        '''The method transforms a notebook into a HTML file. By default,
        the title of the report is the name of the file without underscores.
        This can be modified by adding a custom key `title` to the metadata
        of the notebook.

        Args:
            version (int, default: 4): the version of the notebook
                (as_version parameter from nbformat.read)
            template_path (str, default: None): the full path to the
                template folder. By default, the template is the default
                one.'''
        html_exporter = HTMLExporter()

        if template_path:
            try:
                template_path = Path(template_path)
                loader = jinja2.FileSystemLoader(str(template_path.parent))
                html_exporter.extra_loaders = [loader]
                html_exporter.template_file = template_path.name
            except FileNotFoundError as e:
                raise e

        try:
            with self.temporary_notebook.open() as notebook_file:
                notebook = nbformat.read(notebook_file, as_version=version)
            if 'title' in notebook['metadata'].keys():
                title = notebook['metadata']['title']
            else:
                title = self.title
            resources = dict(metadata=dict(name=title))
            (body, _) = html_exporter.from_notebook_node(notebook, resources=resources)

            self.report_path.write_text(body)
            self.temporary_notebook.unlink()
        except FileNotFoundError as e:
            raise e

    def clean_html(self):
        '''The method removes most of the div elements coming
        from the notebook HTML. The structure is extracted from
        https://nbconvert.readthedocs.io/en/latest/customizing.html.

        The output_text and prompt elements are removed.'''
        with self.report_path.open() as bare_html:
            light_html = BeautifulSoup(bare_html, 'lxml')

        classes_to_remove = ['output_text', 'prompt']
        classes_to_replace = [
            'border-box-sizing', 'container',
            'cell', 'inner_cell', 'rendered_html',
            'output_prompt', 'output_wrapper', 'output', 'output_area']

        for class_to_remove in classes_to_remove:
            for div in light_html.findAll('div', {'class': class_to_remove}):
                div.decompose()

        for class_to_replace in classes_to_replace:
            for tag in light_html.findAll('div', {'class': class_to_replace}):
                tag.replaceWithChildren()

        # Remove the dataframe class from the tables
        for tag in light_html.findAll('table'):
            if 'id' not in tag.attrs.keys():
                tag.attrs = None

        # For highlight.js to work, one needs
        # the tag <pre><code></code></pre>
        for tag in light_html.findAll('pre'):
            content = ''.join(map(str, tag.content))
            content = '<code>{}</code>'.format(content)
            tag.contents = BeautifulSoup(content, 'lxml')

        # codecs is mandatory to avoid problem of encoding
        # on the different servers
        codecs.open(
            str(self.report_path),
            'w', encoding='utf-8').write(str(light_html))
