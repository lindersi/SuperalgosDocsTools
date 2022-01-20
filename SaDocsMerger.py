# Merged deutsche Übersetzungen von veralteten Docs-Dateien in die aktuellen Dateien

import os
import json
import sys


project_path = "/home/simon/Superalgos/"
backup_path = "/home/simon/Superalgos-Backup/"
save_path = "/home/simon/Superalgos-Test/"  # z.B. "/home/simon/Superalgos-Test/". Mit save_path = project_path werden die Originaldateien überschrieben
old_files_list = "old_commits.txt"
fixed_files_list = "new_commits.txt"


# Dateiliste laden (old_commits.txt)
with open(old_files_list, 'r') as file:
    files = []
    for line in file:
        files.append(line.rstrip())
# print(files)

# Aktualisiertes Pendant öffnen und auf deutsche Übersetzungen prüfen
for file in files:
    if True:
    # try:
        new_path = project_path + file
        with open(new_path, 'r') as new_json:
            new_file = json.load(new_json)  # Objekt (dict) aus der aktuellen Datei erzeugen
        old_path = backup_path + file
        with open(old_path, 'r') as old_json:
            old_file = json.load(old_json)  # Objekt aus meiner alten Datei erzeugen

        # Prüfen, ob Deutsche Übersetzung in 'definitions' vorhanden
        if 'translations' in new_file['definition']:
            de = False
            new_transl = new_file['definition']['translations']
            for i in new_transl:
                if i['language'] == 'DE':
                    de = True
            # Falls nicht, Übersetzung aus meiner alten Datei einfügen
            if not de:
                old_transl = old_file['definition']['translations']
                for j in old_transl:
                    if j['language'] == 'DE':
                        old_de = j
                        new_transl.append(old_de)
        # Wenn noch gar keine Übersetzung vorhanden, 'translations' inkl. meinem Ersteintrag neu erstellen
        else:
            old_transl = old_file['definition']['translations']
            for k in old_transl:
                if k['language'] == 'DE':
                    old_de = k
                    new_def = new_file['definition']
                    new_def['translations'] = [old_de]

        # Prüfen, ob Deutsche Übersetzung in 'paragraphs' vorhanden
        p = 0
        for paragraph in new_file['paragraphs']:
            if 'translations' in paragraph:
                de = False
                new_transl = new_file['paragraphs'][p]['translations']
                for i in new_transl:
                    if i['language'] == 'DE':
                        de = True
                # Falls nicht, Übersetzung aus meiner alten Datei einfügen
                if not de:
                    # old_transl = old_file['paragraphs'][p]['translations']
                    # for j in old_transl:
                    #     if j['language'] == 'DE':
                    #         old_de = j
                    #         new_transl.append(old_de)
                    pass
            # Wenn noch gar keine Übersetzung vorhanden, 'translations' inkl. meinem Ersteintrag neu erstellen
            else:
                # old_paragr = old_file['paragraphs'][p]
                # old_transl = old_paragr['translations']
                # for k in old_transl:
                #     if k['language'] == 'DE':
                #         old_de = k
                #         new_def = new_file['paragraphs'][p]
                #         new_def['translations'] = [old_de]
                pass
            p += 1

        # Geänderte Datei im save_path speichern
        test_file = save_path + file
        test_path = os.path.dirname(test_file)
        if not os.path.exists(test_path):
            os.makedirs(test_path)
        with open(test_file, 'w') as test_json:
            json.dump(new_file, test_json, indent=4, ensure_ascii=False)

        new_json.close()
        old_json.close()
        test_json.close()

    # except:
        # print('Error processing ' + file + ': ' + str(sys.exc_info()))

# Geänderte Dateien in new_commits.txt auflisten