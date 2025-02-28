from maxihelp.decorators import check_params
from datetime import datetime


@check_params()
def some_func(x: datetime) -> None:
    print(x.strftime("%d:%m:%Y"))


some_func("")
