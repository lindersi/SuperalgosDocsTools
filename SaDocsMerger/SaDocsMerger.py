# Merges translations from outdated Docs files into current files

import os
import json
import shutil
import sys


project_path = "/home/simon/Superalgos/"  # The local Superalgos folder - update Superalgos before processing!
backup_path = "/home/simon/Superalgos-bkp/"  # Backup path for original files before processing. Is created if needed.
source_path = "/home/simon/Superalgos-DE/"  # Superalgos-Structure with the translations to merge
save_path = "/home/simon/Superalgos-Test/"  # Path for merged files (save_path = project_path to overwrite originals)
files_list = "files-to-process.txt"  # Contains the paths ("Projects/.../...json") of the files to process
lang = "DE"  # Language code of the language to add

processed = []
ignored = []
errors = []

# Load list with files to process
with open(files_list, 'r') as file:
    files = []
    for line in file:
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
        src_path = source_path + file
        with open(src_path, 'r') as src_json:
            src_file = json.load(src_json)

        processed_flag = False
        if 'translations' in new_file['definition']:
            # Check if translation already exists (prevent overwriting)
            lang_check = False
            new_transl = new_file['definition']['translations']
            for i in new_transl:
                if i['language'] == lang:
                    lang_check = True
            if not lang_check:
                # Insert translation from source file
                src_transl = src_file['definition']['translations']
                for j in src_transl:
                    if j['language'] == lang:
                        src_lang = j
                        new_transl.append(src_lang)
                        processed_flag = True
        else:
            # If no translation exists, create new "translations" entry
            src_transl = src_file['definition']['translations']
            for k in src_transl:
                if k['language'] == lang:
                    src_lang = k
                    new_def = new_file['definition']
                    new_def['translations'] = [src_lang]
                    processed_flag = True

        # Same game for every paragraph
        p = 0
        for paragraph in new_file['paragraphs']:
            if 'translations' in paragraph:
                lang_check = False
                new_transl = new_file['paragraphs'][p]['translations']
                for i in new_transl:
                    if i['language'] == lang:
                        lang_check = True
                if not lang_check:
                    src_transl = src_file['paragraphs'][p]
                    if 'translations' in src_transl:
                        for j in src_transl['translations']:
                            if j['language'] == lang:
                                src_lang = j
                                new_transl.append(src_lang)
                                processed_flag = True
            else:
                src_paragr = src_file['paragraphs'][p]
                if 'translations' in src_paragr:
                    for k in src_paragr['translations']:
                        if k['language'] == lang:
                            src_lang = k
                            new_def = new_file['paragraphs'][p]
                            new_def['translations'] = [src_lang]
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
    src_json.close()

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

print(f'Successfully merged {len(processed)} and ignored {len(ignored)} of {len(files)} files with {len(errors)} errors.')
