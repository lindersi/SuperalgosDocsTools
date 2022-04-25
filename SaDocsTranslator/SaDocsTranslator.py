# Insert translations from DeepL

import os
import json
import shutil
import sys
import time
import deepl
import secrets


project_path = "/home/simon/Superalgos/"  # The local Superalgos folder - update Superalgos before processing!
backup_path = "/home/simon/Superalgos-bkp/"  # Backup path for original files before processing. Is created if needed.
save_path = "/home/simon/Superalgos-DE/"  # Path for translated files (save_path = project_path to overwrite originals)
files_list = "files-to-translate.txt"  # Contains the paths ("Projects/.../...json") of the files to process
lang = "DE"  # Language code of the language to add
ignore = ['Block', 'Gif', 'Include', 'Hierarchy']  # Paragraph types (style=) not to translate

processed = []
ignored = []
errors = []
transl = {}

# Create a Translator object providing your DeepL API authentication key.
translator = deepl.Translator(secrets.deepl_api_key)

# Glossaries allow you to customize your translations
glossary_superalgos = translator.create_glossary(
    "Superalgos",
    source_lang="EN",
    target_lang=lang,
    entries={
        "node": "Node",
        "nodes": "Nodes",
        "space": "Space",
        "workspace": "Workspace"
    },
)

def translate(text):
    transl['language'] = lang
    transl['text'] = str(translator.translate_text_with_glossary(text, glossary_superalgos)) + '\n<i>Original: ' + text + '</i>'
    transl['updated'] = round(time.time() * 1000)
    return transl

# Load list with files to process
with open(files_list, 'r') as file:
    files = []
    for line in file:
        if len(line.rstrip()) > 0:  # ignore empty lines
            files.append(line.rstrip())

# Backup original Superalgos files
for file in files:
    os.makedirs(os.path.dirname(backup_path + file), exist_ok=True)
    shutil.copy(project_path + file, backup_path + file)

# Open source files and check for translations
for file in files:
    try:
        new_path = project_path + file
        with open(new_path, 'r') as new_json:
            new_file = json.load(new_json)

        processed_flag = False
        if 'translations' in new_file['definition']:
            # Check if translation already exists (prevent overwriting)
            lang_check = False
            new_transl = new_file['definition']['translations']
            for i in new_transl:
                if i['language'] == lang:
                    lang_check = True
            if not lang_check:
                # Translate text
                orig_text = new_file['definition']['text']
                transl = translate(orig_text)
                new_transl.append(transl)
                processed_flag = True
        else:
            # If no translation exists, create new "translations" entry
            orig_text = new_file['definition']['text']
            new_file['definition']['translations'] = [translate(orig_text)]
            processed_flag = True

        # Same game for every paragraph
        p = 0
        for paragraph in new_file['paragraphs']:
            if paragraph['style'] not in ignore:
                if 'translations' in paragraph:
                    lang_check = False
                    new_transl = new_file['paragraphs'][p]['translations']
                    for i in new_transl:
                        if i['language'] == lang:
                            lang_check = True
                    if not lang_check:
                        # Translate text
                        orig_text = new_file['paragraphs'][p]['text']
                        transl = translate(orig_text)
                        new_transl.append(transl)
                        processed_flag = True
                else:
                    orig_text = new_file['paragraphs'][p]['text']
                    new_file['paragraphs'][p]['translations'] = [translate(orig_text)]
                    processed_flag = True
                p += 1

        # Write merged file to save_path
        if processed_flag:
            save_file = save_path + file
            test_path = os.path.dirname(save_file)
            if not os.path.exists(test_path):
                os.makedirs(test_path)
            with open(save_file, 'w') as save_json:
                    json.dump(new_file, save_json, indent=4, ensure_ascii=False)
                    processed.append(file)
            save_json.close()
        else:
            ignored.append(file)

    except:
        errors.append(file + ': ' + str(sys.exc_info()))
        print('Error processing ' + file + ': ' + str(sys.exc_info()))

    new_json.close()

with open('processed_files.txt', 'w') as proc_files:
    proc_files.write('Processed:\n')
    for line in processed:
        proc_files.write(line + '\n')
    proc_files.write('\nIgnored (already translated):\n')
    for line in ignored:
        proc_files.write(line + '\n')
    proc_files.write('\nErrors:\n')
    for line in errors:
        proc_files.write(line + '\n')
    proc_files.close()

print(f'Successfully translated {len(processed)} and ignored {len(ignored)} of {len(files)} files with {len(errors)} errors.')
