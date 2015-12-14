Result
======

A simple Result type `inspired by Rust <https://doc.rust-lang.org/std/result/>`__.

The idea is that a ``Result`` value can be either ``Ok(value)`` or ``Err(error)``,
with a way to differentiate between the two. It will change code like this:

.. sourcecode:: python

    def get_user_by_email(email):
        """
        Return the user instance or an error message.
        """
        if not user_exists(email):
            return None, 'User does not exist'
        if not user_active(email):
            return None, 'User is inactive'
        user = get_user(email)
        return user, None

    user, reason = get_user_by_email('ueli@example.com')
    if user is None:
        raise RuntimeError('Could not fetch user: %s' % reason)
    else:
        do_something(user)

To something like this:

.. sourcecode:: python

    from result import Ok, Err

    def get_user_by_email(email):
        """
        Return the user instance or an error message.
        """
        if not user_exists(email):
            return Err('User does not exist')
        if not user_active(email):
            return Err('User is inactive')
        user = get_user(email)
        return Ok(user)

    user_result = get_user_by_email(email)
    if user_result.is_ok():
        do_something(user_result.value)
    else: 
        raise RuntimeError('Could not fetch user: %s' user_result.value)

As this is Python and not Rust, you will lose some of the advantages that it
brings, like elegant combinations with the ``match`` statement. On the other
side, you don't have to return semantically unclear tuples anymore.

Not all methods (https://doc.rust-lang.org/std/result/enum.Result.html) have
been implemented, only the ones that make sense in the Python context. You still
don't get any type safety, but some easier handling of types that can be OK or
not, without resorting to custom exceptions.
