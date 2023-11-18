# Advanced Usage

## Exceptions

The library raises several exceptions, the main ones being: [`AnimeNotAvailable`](../../api-reference/exceptions/#animeworld.exceptions.AnimeNotAvailable), [`Error404`](../../api-reference/exceptions/#animeworld.exceptions.Error404), and [`DeprecatedLibrary`](../../api-reference/exceptions/#animeworld.exceptions.DeprecatedLibrary).<br>For more information, consult the [documentation](../../api-reference/exceptions).

### DeprecatedLibrary

The [`DeprecatedLibrary`](../../api-reference/exceptions/#animeworld.exceptions.DeprecatedLibrary) exception is raised when a change on the [AnimeWorld](https://www.animeworld.so/) site is detected that is no longer supported by the library.

This exception can be raised practically by any method of the library, so it is recommended to handle it globally.

```py linenums="1" hl_lines="9"
try:
    res = aw.find("...")
    anime = aw.Anime("https://www.animeworld.so/play/...")
    episodes = anime.getEpisodes()

    for x in episodes:
        x.download()
        
except aw.DeprecatedLibrary as e:
    # Exception handling
    print("Open an issue on GitHub :(")
```

### Error404

The [`Error404`](../../api-reference/exceptions/#animeworld.exceptions.Error404) exception is raised when the URL passed during the creation of the Anime object points to a [404](https://www.animeworld.so/404) page.

Since this exception is only raised by the [`Anime`](../../api-reference/developer-interface/#animeworld.Anime) class, it is recommended to handle it only if you are indeed instantiating an object of that class.

```py linenums="1" hl_lines="7"
try:
    res = aw.find("...")

    try:
        anime = aw.Anime("https://www.animeworld.so/play/...")

    except aw.Error404 as e:
        # Exception handling
        print("Anime not found :(")

    else:
        episodes = anime.getEpisodes()
        for x in episodes:
            x.download()
        
except aw.DeprecatedLibrary as e:
    # Exception handling
    print("Open an issue on GitHub :(")
```

### AnimeNotAvailable

The [`AnimeNotAvailable`](../../api-reference/exceptions/#animeworld.exceptions.AnimeNotAvailable) exception is raised when the anime page exists, but the episodes are not yet available. This happens, for example, when a new season starts.

The exception occurs only when calling the [`getEpisodes`](../../api-reference/developer-interface/#animeworld.anime.Anime.getEpisodes) method.

```py linenums="1" hl_lines="15"
try:
    res = aw.find("...")

    try:
        anime = aw.Anime("https://www.animeworld.so/play/...")

    except aw.Error404 as e:
        # Exception handling
        print("Anime not found :(")

    else:
        try:
            episodes = anime.getEpisodes()

        except aw.AnimeNotAvailable as e:
            # Exception handling
            print("Anime not yet available :(")

        else:
            for x in episodes:
                x.download()
        
except aw.DeprecatedLibrary as e:
    # Exception handling
    print("Open an issue on GitHub :(")
```

## Server

To download an episode, you can manually select the server from which to download the video. To do this, first obtain the list of servers using the [`Episode.links`](../../api-reference/developer-interface/#animeworld.episode.Episode.links) attribute and then choose one of the supported ones.

!!! Warning
    I do not recommend using this method to download an episode; it is much simpler and safer to use the [`Episode.download`](../../api-reference/developer-interface/#animeworld.episode.Episode.download) method because:

    1. The fastest server is always chosen at the beginning.
    2. If an unsupported server is chosen, the [ServerNotSupported](../../api-reference/exceptions/#animeworld.exceptions.ServerNotSupported) exception will be raised.

```py linenums="1"
anime = aw.Anime("...")

# Choose the first episode
episode = anime.getEpisodes()[0]

# Get the list of servers
servers = episode.links

# Choose the AnimeWorld_Server server, for example
server = [x for x in servers if isinstance(x.name, AnimeWorld_Server)][0]

# Download the video
server.download()
```

### Supported Servers

The supported servers are listed below; if you want to contribute to add others, you can take a look at the [Contributing](../../community/contributing/) section.

--8<-- "static/server.txt"

## Download

!!! Warning inline end
    If there are any disallowed characters in the file name (`#%&{}<>*?/$!'":@+\``|=`), they will be automatically removed. To obtain the actual file name written to disk, you can get it from the return of the [`Episode.download`](../../api-reference/developer-interface/#animeworld.episode.Episode.download) method.

To obtain an episode, i recommend using the [`Episode.download`](../../api-reference/developer-interface/#animeworld.episodio.Episodio.download) method, which retrieves the video using the fastest available server at the time of the download.

You can set the file name using the `title` parameter and the destination folder using the `folder` parameter.

### hook

The `hook` parameter is more interesting; this is a reference to a function that will be called every time a video chunk is downloaded (~524 KB). This is useful for displaying the download progress on the screen. The function must have a single parameter of type `Dict[str, Any]`.

```py
def my_hook(data):
	print(data)

episodi = anime.getEpisodes()
for x in episodi:
	x.download(hook=my_hook)
```

An example of a possible dictionary passed to the hook function is as follows:

```py
{
    "total_bytes": 234127340,  # Total size of the video in bytes
    "downloaded_bytes": 524288,  # Downloaded size in bytes
    "percentage": 0.0022393283928310126,  # Downloaded percentage [0, 1]
    "speed": 3048288.673006227,  # Download speed in bytes/s
    "elapsed": 0.17199420928955078,  # Elapsed time in seconds
    "filename": "1 - AnimeWorld Server.mp4",  # File name
    "eta": 76.63416331551707,  # Estimated remaining time in seconds
    "status": "downloading",  # Download status ('downloading' | 'finished' | 'aborted')
}
```

### opt

It is also possible to forcefully stop the download using the `opt` parameter. This parameter is a list of strings, each string representing an option. Currently, the only possible option is `abort`, which stops the download.

If the string `abort` appears in opt during the download, the download is stopped, and the partially downloaded file is deleted.

An example of using the `opt` parameter is as follows:

```py linenums="1"
import animeworld as aw
import time
from threading import Thread

anime = aw.Anime("...")
episode = anime.getEpisodes()[0]

# Define the function for the thread
def handle_download(options_list):
    time.sleep(5)
    options_list.append("abort")


opt = []  # Array for dynamic options
t = Thread(target=handle_download, args=(opt,))  # Create the thread

t.start()  # Start the thread

episode.download(opt=opt)  # Start the download
```

In this example, the download is stopped after 5 seconds.

### I/O Buffer

You can download an episode using a file descriptor directly instead of a string for the directory. Just pass an [IOBase](https://docs.python.org/3/library/io.html#i-o-base-classes) type to the `folder` parameter.

```py linenums="1"
import animeworld as aw
import io

anime = aw.Anime("...")
episode = anime.getEpisodes()[0]

buffer = io.BytesIO()  # Allocate an in-memory buffer

episode.download(folder=buffer)  # Start the download
```

In this example, the downloaded episode is written to memory without being saved as a file. 

---

## Complete Example

```py title="example.py" linenums="1"
--8<-- "static/example.py"
```