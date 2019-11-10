import functools
import time


def print_runtime(func):
    """
    定义装饰器，输出函数运行时间。
    支持关键字参数，修正了__name__和__doc__属性的覆盖。
    :param func: func，被装饰的函数
    :return: func，替换的新函数
    """

    @functools.wraps(func)
    def clocked(*args, **kwargs):
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        epsilon = time.perf_counter() - t0
        name = func.__name__
        arg_list = []
        if args:
            arg_list.append(', '.join(repr(arg) for arg in args))
        if kwargs:
            pairs = [f"{k}={v}" for (k, v) in sorted(kwargs.items())]
            arg_list.append(', '.join(pairs))
        arg_str = ', '.join(arg_list)
        print(f"{epsilon:.8f} {name}({arg_str}) -> {result!r}")
        return result

    return clocked
