from modernrpc.core import rpc_method


@rpc_method
def test():
    return "Works"
