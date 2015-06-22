
.. code:: python

    cd

.. parsed-literal::

    /home/guojiaro


.. code:: python

    !wget -O dropbox.tar.gz "http://www.dropbox.com/download/?plat=lnx.x86_64"
.. code:: python

    !tar -xzf dropbox.tar.gz
.. code:: python

    !~/.dropbox-dist/dropboxd
Now, once you see the message "This client is not linked to any
account...", visit the link in another tab & log in to Dropbox.

THEN, go up to 'Kernel', and select 'Interrupt'.

.. code:: python

    # finally: reboot!
    !/sbin/shutdown -r now
When the machine restarts, you will have a directory /root/Dropbox that
is linked to your dropbox account.
