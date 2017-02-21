# Movable Type Export Entries to HTML

This is a quick-and-dirty python 3 script for exporting Entries from a
Movable Type blog's MySQL database to simple, static HTML pages, one per
Entry.

It's basic, and worked for my needs, but may need tweaking for yours.

When run it will save all Entries for your chosen Blog, and chosen status
(Draft or Published) into individual HTML files. It will also create an
`index.html` listing all the files.


## Installing

Check out the code.

It requires PyMySQL:

	pip install -r requirements.txt


## Configuring

In `export.py` set these variables at the top:

* `BLOG_ID`: The ID of your MT blog -- look in the URL while in MT Admin.
* `BLOG_TITLE`: The title of your blog. This will appear in the output HTML
	pages.
* `ENTRY_STATUS`: Select whether you want to export Draft (`1`) or Published
	(`2`) Entries.
* `DB_*`: Enter all the connection details for your MySQL database.
* `OUTPUT_DIR`: The path to the directory in which the HTML files should be
	saved.


## Using

Do:

	./export.py

The directory you specified in `OUTPUT_DIR` should contain one HTML file per
Entry plus an `index.html`.


## Caveats

* It will currently only handle posts that require no HTML formatting or that
	are set to 'Convert Line Breaks'. Any that use Markdown, Textile, etc will
	have nothing done to them. The script would need to be tweaked to render
	them to HTML (in `_make_entry_html()`).
* It doesn't output any Authors, Comments, Categories or Tags for the Entries.
* I've only used this on one Blog and it worked for that, but it hasn't been
	tested with anything else.

Phil Gyford -- phil@gyford.com

