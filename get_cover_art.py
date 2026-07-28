import requests
from pathlib import Path
from frontmatter_helper import iterate_through_all_files_of_notetype, unwrap_obsidian_link
from config import VAULT_PATH, COVERS_PATH, SOURCES_PATH


def get_cover(artist, album):
    """
    Searches a database for cover art for a certain album and artist.
    returns the art in bytes

    :param artist:
    :param album:
    :return: image in bytes
    """
    # Search MusicBrainz for the release
    search = requests.get(
        "https://musicbrainz.org/ws/2/release",
        params={"query": f"artist:{artist} release:{album}", "fmt": "json"}
    )
    releases = search.json()["releases"][0]["id"]
    if not releases:
        raise ValueError(f"No MusicBrainz release found for {artist} - {album}")

    # Fetch cover from Cover Art Archive
    cover = requests.get(f"https://coverartarchive.org/release/{releases}/front")
    return cover.content  # raw image bytes

def save_cover(artist, album):
    """
    creates a directory (if it doesnt exist) for covers in the obsidian sources dictionary.
    then creates the image path name based on artist and album title.
    then gets the coer art in bytes and writes it to the image path.
    then returns the obsidian markdown link to the newly created image file.

    :param artist:
    :param album:
    :return: obsidian markdown link to newly created cover art
    """
    img_dir = Path(SOURCES_PATH) / "covers"
    img_dir.mkdir(parents=True, exist_ok=True)

    artist2 = unwrap_obsidian_link(artist)
    print(artist2)

    #img_path = img_dir / f"{artist} - {album}.jpg"
    #img_path.write_bytes(get_cover(artist, album))

    return f"[[covers/{artist} - {album}.jpg]]"

def add_cover_image(file, filename):
    """
    for a file, first gets the artist and album information (returns if not available)
    then adds a cover image file to the meta information

    :param file:
    :param filepath:
    :return: -
    """
    print(dict(file))
    artist = file.get("artist")
    album = filename.replace(".md", "")

    if not artist or not album:
        print(f"  Skipping {filename}: missing artist or album field")
        return

    if file.get("cover"):  # don't overwrite if already set
        return

    link = save_cover(artist, album)
    file["cover"] = link
    print(f"  Added cover: {link}")

def match_cover_to_album(file, filename):
    """
    for an album-type file, looks if a cover image with a filename of artist_album exists and sets
    it to the files cover attribute

    :param file:
    :param filename:
    :return:
    """
    artist = unwrap_obsidian_link(file.get("artist"))
    album = filename.replace(".md", "")

    if not artist or not album:
        return

    # build the expected filename the same way clean_filename would
    expected = f"{artist}_{album}.jpg".replace(" ", "")

    cover_path = Path(COVERS_PATH) / expected
    if cover_path.exists():
        file["cover"] = f"[[covers/{expected}]]"
        print(f"  Matched cover: {expected}")
    else:
        print(f"  No cover found for: {expected}")

iterate_through_all_files_of_notetype("album", action=match_cover_to_album)

