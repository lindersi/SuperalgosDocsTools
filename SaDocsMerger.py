# Merged deutsche Übersetzungen von veralteten Docs-Dateien in die aktuellen Dateien

import os
import json
import sys


project_path = "/home/simon/Superalgos/"
backup_path = "/home/simon/Superalgos-Backup/"
save_path = "/home/simon/Superalgos-Test/"
files_list = "old_commits.txt"


# Dateiliste laden (old_commits.txt)
with open(files_list, 'r') as file:
    files = []
    for line in file:
        files.append(line.rstrip())

# print(files)

# Aktualisiertes Pendant öffnen und auf deutsche Übersetzungen prüfen
for file in files:
    try:
        new_path = project_path + file
        with open(new_path, 'r') as new_json:
            new_file = json.load(new_json)  # Objekt (dict) aus der ganzen aktuellen Datei erzeugen
        old_path = backup_path + file
        with open(old_path, 'r') as old_json:
            old_file = json.load(old_json)  # Objekt aus der alten Datei erzeugen

        if 'translations' in new_file['definition']:
            de = False
            new_transl = new_file['definition']['translations']
            for i in new_transl:
                if i['language'] == 'DE':
                    de = True
            if not de:
                old_transl = old_file['definition']['translations']
                for j in old_transl:
                    if j['language'] == 'DE':
                        old_de = j
                        new_file['definition']['translations'].append(old_de)
        else:
            old_transl = old_file['definition']['translations']
            for k in old_transl:
                if k['language'] == 'DE':
                    old_de = k
                    new_file['definition']['translations'][0] = old_de

        test_file = save_path + file
        test_path = os.path.dirname(test_file)
        if not os.path.exists(test_path):
            os.makedirs(test_path)
        with open(test_file, 'w') as test_json:
            json.dump(new_file, test_json, indent=4, ensure_ascii=False)

        new_json.close()
        old_json.close()
        test_json.close()

    except:
        print('Error processing ' + file + ': ' + str(sys.exc_info()))

# Wo keine Deutsche Übersetzung vorhanden, den entsprechenden Inhalt aus der alten Datei in die Neue einfügen


# Geänderte Dateien in new_commits.txt auflisten