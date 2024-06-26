#!/usr/bin/env python

"""
    Utility script for processing system instruction from MD (Markdown) format to the HTML.
    See additional tech info here:
        - https://alberand.com/markdown-custom-tags.html

    Created:  Dmitrii Gusev, 08.05.2023
    Modified: Dmitrii Gusev, 24.07.2023
"""

# todo: make this script complete cmd line utility (use clock library)
# todo: add cmd line parameters for input/output and process mgmt...
# todo: add parameters to turn on/off and configure our own extensions/processors

import re
import markdown
import xml.etree.ElementTree as etree

from loguru import logger as log
from markdown.extensions import Extension
from markdown.inlinepatterns import LinkInlineProcessor
from markdown.postprocessors import Postprocessor

# -- some script defaults
ENCODING = "utf-8"

# -- docs to convert
DOCS = {
    ".instruction/instruction.md": ".instruction/instruction.html",
    ".instruction/faq.md":         ".instruction/faq.html",
}

# -- defaults for markdown and extensions
IMAGE_LINK_RE = r'\!\['  # this is from the markdown source


class ImageInlineProcessor(LinkInlineProcessor):  # our new markdown image processor
    """ Return a img element from the given match. """

    def handleMatch(self, m, data):
        text, index, handled = self.getText(data, m.end(0))
        if not handled:
            return None, None, None

        src, title, index, handled = self.getLink(data, index)
        if not handled:
            return None, None, None

        # - put image into a <div> container - not needed now
        # div = etree.Element("div")
        # div.set("class", "image-container")
        # a = etree.SubElement(div, "a")
        # a.set("href", src)
        # img = etree.SubElement(a, "img")

        # create HTML element <img /> with necessary properties
        img = etree.Element("img")
        img.set("src", "{% static 'docs/" + src + "' %}")
        if title is not None:
            img.set("title", title)
        img.set('alt', self.unescape(text))

        return img, m.start(0), index


class AddTableCSSClassesPostprocesor(Postprocessor):  # new postprocessor
    """ Add bootstrap CSS classes to tables (add it to each <table> tag). """

    def run(self, text):
        return re.sub('<table>',
                      '<table class="table-striped table-condensed table-hover table-bordered">',
                      text)


class MyTagsExtension(Extension):  # our own markdown extension class

    def extendMarkdown(self, md):
        # deregister default image processor and replace it with our custom one
        md.inlinePatterns.deregister('image_link')
        md.inlinePatterns.register(ImageInlineProcessor(IMAGE_LINK_RE, md), 'image_link', 150)

        # register our own (additional) postprocessor
        md.postprocessors.register(AddTableCSSClassesPostprocesor(), 'add_css_to_table_tag', 250)


# MARKDOWN_CONFIG = {  # todo: do we need this config?
#   'extensions': [MyTagsExtension()],
#   'extension_configs': {
#     'markdown.extensions.extra': {},
#     'markdown.extensions.meta': {},
#   },
#   'output_format': 'html5',
# }


def convert():
    log.info("Starting conversion MD to HTML.")

    for key in DOCS:
        # starting convertion MD to HTML
        log.info(f"Converting markdown [{key}] to html [{DOCS[key]}].")

        # open input MD file, read it and convert to HTML
        with open(key, "r", encoding=ENCODING) as input_file:
            text = input_file.read()
        html = markdown.markdown(text, extensions=['sane_lists', 'toc', 'tables', 'attr_list',
                                                   MyTagsExtension()])

        # open output HTML file and there the converted from MD text
        with open(DOCS[key], "w", encoding=ENCODING, errors="xmlcharrefreplace") as output_file:
            output_file.write("{% load static %}\n")
            output_file.write(html)

        # conversion is done - final msg
        log.info(f"Done converting to file [{DOCS[key]}].")


if __name__ == "__main__":
    convert()
