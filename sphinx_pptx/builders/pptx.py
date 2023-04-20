"""Plain-text Sphinx builder."""

from __future__ import annotations

from os import path
from typing import Any, Iterator

from docutils.io import StringOutput
from docutils.nodes import Node

from sphinx.application import Sphinx
from sphinx.builders import Builder
from sphinx.locale import __
from sphinx.util import logging
from sphinx.util.osutil import ensuredir, os_path

from pptx import Presentation

from ..writers.pptx import PptxTranslator, PptxWriter

logger = logging.getLogger(__name__)


class PptxBuilder(Builder):
    name = 'pptx'
    format = 'pptx'
    epilog = __('The text files are in %(outdir)s.')

    out_suffix = '.txt'
    allow_parallel = True
    default_translator_class = PptxTranslator

    current_docname: str | None = None

    def init(self) -> None:
        # section numbers for headings in the currently visited document
        self.secnumbers: dict[str, tuple[int, ...]] = {}

    def get_outdated_docs(self) -> Iterator[str]:
        for docname in self.env.found_docs:
            if docname not in self.env.all_docs:
                yield docname
                continue
            targetname = path.join(self.outdir, docname + self.out_suffix)
            try:
                targetmtime = path.getmtime(targetname)
            except Exception:
                targetmtime = 0
            try:
                srcmtime = path.getmtime(self.env.doc2path(docname))
                if srcmtime > targetmtime:
                    yield docname
            except OSError:
                # source doesn't exist anymore
                pass

    def get_target_uri(self, docname: str, typ: str | None = None) -> str:
        return ''

    def prepare_writing(self, docnames: set[str]) -> None:
        self.writer = PptxWriter(self)

    def write_doc(self, docname: str, doctree: Node) -> None:
        self.current_docname = docname
        self.secnumbers = self.env.toc_secnumbers.get(docname, {})
        destination = StringOutput(encoding='utf-8')
        self.writer.write(doctree, destination)
        outfilename = path.join(self.outdir, os_path(docname) + self.out_suffix)
        ensuredir(path.dirname(outfilename))
        # output = self.writer.output
        # try:
        #     with open(outfilename, 'w', encoding='utf-8') as f:
        #         f.write(output)
        # except OSError as err:
        #     logger.warning(__("error writing file %s: %s"), outfilename, err)
        self.writer.prs.save(outfilename + '.pptx')

    def finish(self) -> None:
        pass


def setup(app: Sphinx) -> dict[str, Any]:
    app.add_builder(PptxBuilder)

    # app.add_config_value('text_sectionchars', '*=-~"+`', 'env')
    # app.add_config_value('text_newlines', 'unix', 'env')
    # app.add_config_value('text_add_secnumbers', True, 'env')
    # app.add_config_value('text_secnumber_suffix', '. ', 'env')

    return {
        'version': 'builtin',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }