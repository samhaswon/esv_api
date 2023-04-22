########################################################################
# An example of usage of the esv_api package. This example assumes you
# have placed your API key in api-key.txt. For generating an API key,
# please see the README.
#
# File name: example.py
# Author: Samuel Howard
# Version: 4-22-2023
########################################################################
import esv_api

if __name__ == '__main__':
    with open("api-key.txt", "r") as api_key_in:
        api_key: str = api_key_in.read()

    # Example search
    search = esv_api.Search(api_key)
    print("Search example: ")
    print(search.search("Jesus wept"))
    print("=" * 30)

    # Example text retrieval
    text = esv_api.Text(api_key)
    print("Text example: ")
    print("More open, get_passage method:")
    print(text.get_passage("John 11:35")[1])
    print("-" * 30)
    print("More filtered, get_chapter_json method")
    print(text.get_chapter_json("Psalm", 117))
    print("=" * 30)

    # Example HTML retrieval
    html = esv_api.HTML(api_key)
    print("HTML example:")
    print("More open, get_passage method:")
    print(html.get_passage("John 11:35"))
    print("-" * 30)
    print("More basic, get_passage_basic method:")
    print(html.get_passage_basic("John 11:35"))
    print("=" * 30)

    # Example audio link retrieval
    audio = esv_api.Audio(api_key)
    print("Audio example:")
    print("The get_passage method would return a link such as: ", audio.get_passage("John", 11, 35))
