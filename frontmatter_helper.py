import os
import frontmatter
from pathlib import Path

from config import VAULT_PATH, NOTE_TYPE, ITEMS_FOLDER

def replace_and_delete_frontmatter(old_yaml, new_yaml):
    """
    Replaces attribute name for all files. Preserves the value and deletes the old attribute.

    :param old_yaml: the old attribute name
    :param new_yaml: the new attribute name.
    :return:
    """
    for root, dirs, files in os.walk(VAULT_PATH):
        for filename in files:
            if filename.endswith(".md"):
                filepath = os.path.join(root, filename)
                try:
                    file = frontmatter.load(filepath)
                    value = file.get(old_yaml)
                    file[new_yaml] = value

                    del file[old_yaml]

                    with open(filepath, "w") as f:
                        f.write(frontmatter.dumps(file))

                    print(f"Updated: {filename}")
                except Exception as e:
                    print(f"Skipped {filename}: {e}")

def delete_note_typ_attribut():
    """
        :param old_yaml: the old attribute name
        :param new_yaml: the new attribute name.
        :return:
        """
    for root, dirs, files in os.walk(os.path.join(VAULT_PATH, ITEMS_FOLDER)):
        for filename in files:
            if filename.endswith(".md"):
                filepath = os.path.join(root, filename)
                try:
                    file = frontmatter.load(filepath)
                    del file["note-typ"]

                    if file.get("note-typ"):
                        del file["note-typ"]

                        with open(filepath, "w") as f:
                            f.write(frontmatter.dumps(file))

                        print(f"Updated: {filename}")
                except Exception as e:
                    print(f"Skipped {filename}: {e}")


def change_note_type_to_item_type(old_note_type):
    """
    :param old_yaml: the old attribute name
    :param new_yaml: the new attribute name.
    :return:
    """
    for root, dirs, files in os.walk(os.path.join(VAULT_PATH, ITEMS_FOLDER)):
        for filename in files:
            if filename.endswith(".md"):
                filepath = os.path.join(root, filename)
                try:
                    file = frontmatter.load(filepath)

                    if file.get("note_type") == old_note_type:
                        file["item_type"] = old_note_type
                        file["note_type"] = "item"
                        #del file["note-typ"]

                        with open(filepath, "w") as f:
                            f.write(frontmatter.dumps(file))

                        print(f"Updated: {filename}")
                except Exception as e:
                    print(f"Skipped {filename}: {e}")

def replace_and_delete_frontmatter_with_value(old_yaml, new_yaml, attribute_value):
    """
    Searches and replaces frontmatter for all the files in the obsidian vault.
    If the attribute with the name of "old_yaml" has the value of "attribute value",
    it creates a new attribute with the name "new_yaml" and assigns it the "attribute_value".
    It also deletes the old attribute

    :param old_yaml: the old attribute
    :param new_yaml: the new attribute to be createe
    :param attribute_value: replacement will be executed for all files where old_yaml = attribute_value
    :return:
    """
    for root, dirs, files in os.walk(VAULT_PATH):
        for filename in files:
            if filename.endswith(".md"):
                filepath = os.path.join(root, filename)
                try:
                    raw = Path(filepath).read_text(encoding="utf-8")
                    if "{{" in raw:
                        continue

                    file = frontmatter.load(filepath)
                    if file.get(old_yaml) == attribute_value:
                        file[new_yaml] = attribute_value # set new property
                        del file[old_yaml]  # delete old property

                        with open(filepath, "w") as f:
                            f.write(frontmatter.dumps(file))

                        print(f"Updated: {filename}")
                except Exception as e:
                    print(f"Skipped {filename}: {e}")

def iterate_through_all_files_of_notetype(note_type, action=None):
    """
    iterates through all files of a certain note_type, performs a given action for them

    :param note_type: the note type, for example "journal-note"
    :param action: an action that can be executed for each file for a certain note type
    :return:
    """
    for root, dirs, files in os.walk(VAULT_PATH):
        for filename in files:
            if filename.endswith(".md"):
                filepath = os.path.join(root, filename)
                try:
                    # some stuff or else it errors
                    raw = Path(filepath).read_text(encoding="utf-8")
                    if "{{" in raw:
                        continue

                    file = frontmatter.load(filepath)
                    if file.get(NOTE_TYPE) == note_type:
                        #if action:
                        #    action(file, filename)
                        new_path = os.path.join(VAULT_PATH, ITEMS_FOLDER, filename)
                        os.replace(filepath, new_path)
                        #with open(filepath, "w") as f:
                            #f.write(frontmatter.dumps(file))

                        print(f"Updated: {filename}")
                except Exception as e:
                    print(f"Skipped {filename}: {e}")

def iterate_through_all_files_in_path(path, action=None):
    """goes through all files in a certain directory and performs an action"""
    for root, dirs, files in os.walk(path):
        for filename in files:
            filepath = os.path.join(root, filename)
            try:
                if action:
                    action(filepath)
                    print(f"Updated: {filename}")
            except Exception as e:
                print(f"Skipped {filename}: {e}")


def clean_filename(filepath):
    """given a path, replaces the name based on a set pattern"""
    directory = os.path.dirname(filepath)
    filename = os.path.basename(filepath)

    # remove [[ ]], spaces, dashes, and extension
    new_name = filename.replace("[[", "").replace("]]", "")
    new_name = new_name.replace(" - ", "_").replace(" ", "")

    new_filepath = os.path.join(directory, new_name)
    os.rename(filepath, new_filepath)
    print(f"Renamed: {filename} → {new_name}")


#iterate_through_all_files_in_path(COVERS_PATH, action=clean_filename)

def rename_attribute_value(attribute, pattern_old_name, pattern_new_name):
    pass


def unwrap_obsidian_link(link):
    return link.strip("[]")

def copy_all_item_notes_into_item_folder(file, filename):
    print(filename)


delete_note_typ_attribut()