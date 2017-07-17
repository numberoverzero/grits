Change Log
~~~~~~~~~~

====================
[0.5.1] - 2017.07.16
====================

``prettify_html`` is a noop for now, since ``BeautifulSoup.prettify`` was
inserting significant whitespace into elements.

==================
[0.5] - 2017.06.14
==================

Rewrote the content splitting mechanism.  Each source html file can have the following format:
* at most one <head> section
* exactly one <main> section (with any number of inner scripts)
* any number of top-level <script> sections.

``grits-build`` takes ``--src``, ``--dst``, and ``--tpl``.  Use ``--tpl`` to provide your own templates for eg.
``__full.html`` or ``__partial.html``.

Source scripts are broken up and the pieces stored in the rendering context as ``"head"``, ``"main"``,
and ``"scripts"``.  These are each strings.

The simplest way to use ``render.Renderer`` is through ``Renderer.process()`` which runs through the source folder
and generates the necessary mapp-specific components like ``_dynamicRoutes.json``.  If you manually generate files,
make sure to call ``Renderer.render_scaffolding()`` to produce those files.

-----
Added
-----

* Split src_dir from templates_dir
* contents of src_dir are always rendered to output while templates_dir are only used to find extra templates

==================
[0.4] - 2017.06.11
==================

-----
Added
-----

* ``Renderer.render`` handles binary files, uses ``context["is_binary"]``
  function to decide if file should be copied directly.
  Defaults to ``grits.render.default_is_binary``.
* Properly copy ``templates/static`` for rendering.

=================
[0.2] - 2017.1.30
=================

-----
Added
-----

* ``grits.build``
* scripts ``grits-build`` and ``grits-serve``

==========================
[0.1] - 2017.1.29 [YANKED]
==========================

-----
Added
-----

Initial commit
