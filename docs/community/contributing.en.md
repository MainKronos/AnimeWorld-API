# Contributing

## Server

This section explains how to add the ability to download an episode from another unsupported server.

--8<-- "static/server.txt"

To add a new server, follow these steps:

1. Create a .py file with the server's name and place it in the [servers](https://github.com/MainKronos/AnimeWorld-API/tree/master/animeworld/servers) folder (e.g., `NewServer.py`).

1. Use this template for the class of the new server:
```py title="NewServer.py" linenums="1"
from .Server import *

class NewServer(Server):
    def fileLink(self):  # Mandatory
        """
        Retrieves the direct link for downloading the episode file.

        Returns:
          Direct link.

        Example:
          ```py
          return str  # File link
          ```
        """
        pass  # TODO: to be completed

    def fileInfo(self) -> Dict[str, str]:  # Optional
        """
        Retrieves information about the episode file.

        Returns:
          Episode file information.

        Example:
          ```py
          return {
            "content_type": str,  # File type, e.g., video/mp4
            "total_bytes": int,  # Total file bytes
            "last_modified": datetime,  # Date and time of the last update to the episode on the server
            "server_name": str,  # Server name
            "server_id": int,  # Server ID
            "url": str  # Episode URL
          }
          ```
        """
        pass  # TODO: to be completed

    def download(self, title: Optional[str] = None, folder: str = '', *, hook: Callable[[Dict], None] = lambda *args: None, opt: List[str] = []) -> Optional[str]:  # Mandatory
        """
        Downloads the episode.

        Args:
          title: Name to be given to the downloaded file.
          folder: Location where the downloaded file will be moved.

        Other parameters:
          hook: Function called multiple times during the download; the function receives a dictionary with the following keys:\n
            - `total_bytes`: Total bytes to download.
            - `downloaded_bytes`: Currently downloaded bytes.
            - `percentage`: Download progress percentage.
            - `speed`: Download speed (bytes/s).
            - `elapsed`: Time elapsed since the start of the download.
            - `eta`: Estimated remaining time for the download to finish.
            - `status`: 'downloading' | 'finished' | 'aborted'
            - `filename`: Downloaded file name.

          opt: List for additional options.\n
            - `'abort'`: Forcefully stops the download.

        Returns:
          Downloaded file name.

        Raises:
          HardStoppedDownload: The downloading file has been forcibly interrupted.

        Example:
          ```py
          return str  # Downloaded file
          ```
        """
        if title is None:
            title = self._defTitle
        else:
            title = self._sanitize(title)

        pass

        # TODO: to be completed, select one of the 2 methods:
        # #NOTE: to be used if the file can be downloaded simply with httpx:
        # return self._downloadIn(title,folder,hook=hook,opt=opt)
        #
        # #NOTE: to be used if the file must be downloaded using the youtube_dl library
        # return self._dowloadEx(title,folder,hook=hook,opt=opt)
```

1. Complete the various functions (those marked as `Optional` can also be left incomplete), also taking inspiration from the various servers loaded in the folder.

1. Add the line `from .NewServer import NewServer` to the file [servers/__init__.py](https://github.com/MainKronos/AnimeWorld-API/tree/master/animeworld/servers/__init__.py).

1. Modify the file [episodio.py](https://github.com/MainKronos/AnimeWorld-API/tree/master/animeworld/episodio.py) by adding the server's name among the imports ([Line 12](https://github.com/MainKronos/AnimeWorld-API/blob/master/animeworld/episodio.py#L12)) and modifying the function [__setServer](https://github.com/MainKronos/AnimeWorld-API/blob/master/animeworld/episodio.py).

If everything works correctly, open a [pull request](https://github.com/MainKronos/AnimeWorld-API/pulls).