import os
from typing import Optional

class EnvUtils:
    @staticmethod
    def get_env_variable(var_name: str, default: Optional[str] = None) -> str:
        try:
            return os.environ[var_name]
        except KeyError:
            if default is not None:
                return default
            else:
                error_msg = "The environment variable {} was missing, abort...".format(
                    var_name
                )
                raise OSError(error_msg)