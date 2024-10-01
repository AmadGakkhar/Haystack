import json
import os


def store_dict_as_json(dictionary, filename):
    """
    Stores a dictionary as a JSON file on disk.

    Args:
        dictionary (dict): The dictionary to store.
        filename (str): The filename to use for the JSON file.
    """
    # Ensure the directory exists

    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump(
                {
                    "store_path": "",
                    "document_store": "",
                    "converter": "",
                    "embedder": "",
                    "cleaner": "",
                    "splitter": "",
                },
                f,
            )
    state_dict = {}
    with open(filename, "r") as f:
        state_dict = json.load(f)
        state_dict.update(dictionary)
    # Open the file in write mode
    with open(filename, "w") as f:
        # Use json.dump to serialize the dictionary to JSON
        json.dump(state_dict, f)


def load_json_as_dict(filename):
    """
    Loads a JSON file from disk into a dictionary.

    Args:
        filename (str): The filename of the JSON file.

    Returns:
        dict: The loaded dictionary.
    """
    try:
        # Open the file in read mode
        with open(filename, "r") as f:
            # Use json.load to deserialize the JSON into a dictionary
            return json.load(f)
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return None
