from modernrpc.core import rpc_method


@rpc_method
def echo(text):
    """
    Echoes the sent in string. For testing purpose.
    :param text: string containing text.
    :return: the sent in string.
    """

    return text
