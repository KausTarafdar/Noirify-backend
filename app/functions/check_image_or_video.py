import mimetypes
from typing import Union

def check_file_type(file_path: str)-> Union[str | None]:
    """
    Checks file types for input file_name
        Returns : "video" or "image" if exists
        Else : None
    """
    file_type, err = mimetypes.guess_type(file_path)
    if not err:
        file_type = file_type.split('/')[0]
        return file_type
    else:
        return None

