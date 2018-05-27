NewsCollector: when and why async more is really worth
======================================================

Async code is less readeable and more difficult to debug, and requires the
understanding of new concepts like coroutines and event loops.

Being aware of that, I'm certainly not going to use async code just because
it's cool or fancy.

Nonetheless, a great effort has being devoted to provide Channels as
a framework suitable for both synchronous and asynchronous contexts, and
I have a sincere interest in understanding not just **how**, but rather **why**
it's worth it and **when** it can provide advantages.

Installation
------------

Manual installation
~~~~~~~~~~~~~~~~~~~

Make a new virtualenv for the project, and run::

    pip install -r requirements.txt

Then, you'll need Redis running locally; the settings are configured to
point to ``localhost``, port ``6379``, but you can change this in the
``CHANNEL_LAYERS`` setting in ``settings.py``.

Finally, run::

    python manage.py migrate
    python manage.py runserver


Usage
-----

No background models are required, and you won't need a superuser account.

The home page provides two buttons to let the user ask from the download of a
list of web pages; after data collection, the server sends back the results
packed in a JSON dictionary.

In **sync mode, downloads happen sequentially**, and the total time required to
complete the operation is at least the sum of the time required by each
individual download.

When demanting network operations are involved, there's a good chance to improve
overall performances significantly by applying an async approach.

In **async mode, pages are downloaded concurrently**, and the time required to
collect all results in greatly reduced.

.. image:: etc/screenshot.png


How It Works
------------

TODO: PROVIDE RELEVANT EXPLANATIONS HERE ...


Further Reading
---------------

- `Python & Async Simplified <https://www.aeracode.org/2018/02/19/python-async-simplified/>`_
- `Making 1 million requests with python-aiohttp <https://pawelmhm.github.io/asyncio/python/aiohttp/2016/04/22/asyncio-aiohttp.html>`_
