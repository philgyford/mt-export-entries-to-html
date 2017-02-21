#!/usr/bin/env python
# coding: utf-8
import pymysql.cursors
import re


BLOG_ID = 1

# Will be used in the output HTML:
BLOG_TITLE = 'My Blog'

# 1 Draft; 2 Published.
ENTRY_STATUS = 2


DB_USER = ''
DB_PASSWORD = ''
DB_NAME = ''
DB_HOST = '127.0.0.1'
DB_PORT = 3306

# Must end in a slash:
OUTPUT_DIR = './posts/'


class MTEntryExporter(object):

    def __init__(self):
        pass

    def start(self):
        
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     db=DB_NAME,
                                     port=DB_PORT,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                sql = ("SELECT * FROM `mt_entry` "
                        "WHERE `entry_blog_id` = %s "
                        "AND `entry_status` = %s "
                        "ORDER BY `entry_authored_on` ASC")
                cursor.execute(sql, (BLOG_ID, ENTRY_STATUS))

                filenames = []

                for entry in cursor:

                    # eg '2017-02-21_my_basename_here.html':
                    filename = '{}_{}.html'.format(
                                entry['entry_created_on'].strftime("%Y-%m-%d"),
                                entry['entry_basename']
                            )

                    filenames.append(filename)

                    filepath = '{}{}'.format(OUTPUT_DIR, filename)

                    f = open(filepath, 'w')

                    f.write( self._make_entry_html(entry) )

                    f.close()
        finally:
            connection.close()

        self._write_index(filenames)

    def _make_entry_html(self, entry):
        "Given an entry dict, returns the HTML for a page containing that entry."

        STATUSES = {
            '1': 'Draft',
            '2': 'Published',
        }

        # 0 None
        # 1 Convert Line breaks
        # __default__ Convert Line breaks

        text = entry['entry_text']
        if entry['entry_text_more']:
            text = '{}\n\n{}'.format(text, entry['entry_text_more'])

        if entry['entry_convert_breaks'] in [1, '__default__']:
            text = self._convert_linebreaks(text)
        
        # We don't currently handle Markdown etc, but we'd do it here if we did.
        # 'markdown'
        # 'markdown_with_smartypants'
        # 'richtext'
        # 'textile_2'
        # 0 - No formatting.

        html = """{html_start}
            <h1>{title}</h1>
            <p><a href="index.html" title="List of entries">{blog_title}</a></p>

            <hr>

            <dl>
                <dt>Created on</dt>
                <dd>{created_on}</dd>
                <dt>Modified on</dt>
                <dd>{modified_on}</dd>
                <dt>Status</dt>
                <dd>{status}</dd>
            </dl>

            <hr>

            {text}

            <hr>
{html_end}""".format(
                html_start = self._html_header(entry['entry_title']),
                title=entry['entry_title'],
                blog_title=BLOG_TITLE,
                created_on=entry['entry_created_on'],
                modified_on=entry['entry_modified_on'],
                status=STATUSES[ str(entry['entry_status']) ],
                text=text,
                html_end = self._html_footer()
            )

        return html

    def _html_header(self, title):
        """Returns HTML for the start of a page.
        title is the text for the <title> tag.
        """

        html = """<!doctype html>
<html lang="en-gb">
    <head>
        <meta charset="utf-8">
        <title>{title}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style type="text/css">
            .container {{
                font-family: sans-serif;
                max-width: 40em;
                margin: 0 auto;
            }}
        </style>
    </head>
    <body>
        <div class="container">
""".format(title=title)

        return html

    def _html_footer(self):
        "Returns HTML for the end of a page."
        html = """
        </div>
    </body>
</html>
"""
        return html

    def _convert_linebreaks(self, text):
        "Add <br> and <p> tags instead of linebreaks."

        # Replace all linebreaks with <br>:
        text = re.sub(
                    r"\r\n?|\n",
                    "<br>\n",
                    text
                )

        # Replace double linebreaks with close/open <p>s:
        text = re.sub(
                    r"<br>\s*<br>",
                    "</p>\n\n<p>",
                    text
                )

        text = "<p>{}</p>".format(text)

        return text

    def _write_index(self, filenames):
        """Writes the index.html
        filenames is a list of filenames to, er, list.
        """

        file_list = ''
        for filename in filenames:
            file_list += '<li><a href="{}">{}</a></li>'.format(filename, filename)

        html = """{html_start}
            <h1>{blog_title}</h1>
            <ul>
            {file_list}
            </ul>
{html_end}""".format(
            html_start=self._html_header('Index'),
            blog_title=BLOG_TITLE,
            file_list=file_list,
            html_end=self._html_footer()
        )

        f = open("{}index.html".format(OUTPUT_DIR), 'w')

        f.write(html)

        f.close()


def main():
    exporter = MTEntryExporter()

    exporter.start()


if __name__ == "__main__":
    main()

