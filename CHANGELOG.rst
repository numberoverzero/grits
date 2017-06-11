Change Log
~~~~~~~~~~

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
