# Writing Docs files info and wordcount to .csv file

import os
import json
import csv
import datetime

project_path = "/home/simon/Superalgos/Projects"  # Startpoint - must be the ".../Superalgos/Projects" directory. Doesn't work with (Windows) backslashes.
stop = -1  # Number of files to process (-1 = all).
csv_filename = 'Superalgos_Docs_list.csv'  # Filename for the output csv file. Date/Time (%y%m%d-%h%m) will be added before.
head = ['Project', 'Category', 'type', 'wordcount', 'Path', 'File', 'topic', 'tutorial', 'pageNumber', 'language']  # Column headers (and order of columns) for the csv file.
# Available are: 'Project', 'Category', 'type' (title), 'wordcount', 'Path', 'File', 'topic', 'tutorial', 'pageNumber', 'language' (if available)
cli_print = False  # Print document structures on cli. Generates several thousand lines for all Superalgos files!


# Extract info and wordcount out of a json file
def read_json(file_path, cli_print):
    output = {'type': 'none', 'wordcount': 0, 'topic': 'none', 'tutorial': 'none', 'pageNumber': 'none', 'language': 'none'}
    lang = ''
    with open(file_path, 'r') as file:
        obj = json.load(file)
    for key_1 in obj:
        val_1 = obj[key_1]
        if isinstance(val_1, dict):  # e.g. definition
            for key_2 in val_1:
                val_2 = val_1[key_2]
                if isinstance(val_2, dict):  # not used in Docs json structure?
                    if cli_print:
                        print(f'2: {key_1}: {key_2} (dict)')
                        for key_3 in val_2:
                            val_3 = val_2[key_3]
                            if isinstance(val_3, dict):
                                print(f'3: {key_1}: {key_2}: {key_3} (dict)')
                            elif isinstance(val_2, list):
                                print(f'3: {key_1}: {key_2}: {key_3} (list)')
                            else:
                                print(f'3: {key_1}: {key_2}: {key_3}: {val_3}')
                elif isinstance(val_2, list):  # e.g. definition translations
                    lang = ''
                    for val_3 in val_2:
                        if isinstance(val_3, dict):
                            if 'language' in val_3:
                                lang += val_3['language'] + ' '
                                if val_3['language'] == 'DE':
                                    text_de = f'3: {key_1}: {key_2}: text ({val_3["language"]}): {str(val_3["text"])[0:50]}...'
                                    if cli_print:
                                        print(text_de)
                            else:
                                if cli_print:
                                    print(f'3: {key_1}: {key_2}: (val_3, dict)')
                                pass
                        elif isinstance(val_3, list):
                            if cli_print:
                                print(f'3: {key_1}: {key_2}: (val_3, list)')
                            pass
                        else:
                            if cli_print:
                                print(f'3: {key_1}: {key_2}: {val_3}')
                            pass
                    if cli_print:
                        print(f'3: {key_1}: {key_2}: language: {lang}')
                else:
                    if key_2 == 'text':
                        output['wordcount'] += words(val_2)
                        if len(val_2) > 53:
                            val_2 = val_2[0:50] + '...'
                    if cli_print:
                        print(f'2: {key_1}: {key_2}: {val_2}')
            # print(f'1: {key_1} (dict)')
        elif isinstance(val_1, list):  # e.g. paragraphs
            i = 0
            for val_2 in val_1:
                i += 1
                if isinstance(val_2, dict):
                    for key_3 in val_2:
                        val_3 = val_2[key_3]
                        if isinstance(val_3, dict):
                            if cli_print:
                                print(f'3: {key_1}: {i}: {key_3} (dict)')
                        elif isinstance(val_3, list):  # e.g. paragraphs translations
                            lang = ''
                            for val_4 in val_3:
                                if isinstance(val_4, dict):
                                    if 'language' in val_4:
                                        lang += val_4['language'] + ' '
                                        if val_4['language'] == 'DE':
                                            text_de = f'4: {key_1}: {i}: {key_3}: text ({val_4["language"]}): {str(val_4["text"])[0:50]}...'
                                            if cli_print:
                                                print(text_de)
                                    else:
                                        if cli_print:
                                            print(f'3: {key_1}: {i}: (val_3, dict)')
                                        pass
                                elif isinstance(val_3, list):
                                    if cli_print:
                                        print(f'3: {key_1}: {i}: (val_3, list)')
                                    pass
                                else:
                                    if cli_print:
                                        print(f'3: {key_1}: {i}: {key_3}: {val_3}')
                                    pass
                            if cli_print:
                                print(f'3: {key_1}: {i}: language: {lang}')
                        else:
                            if key_3 == 'text':
                                output['wordcount'] += words(val_3)
                                if len(val_3) > 53:
                                    val_3 = val_3[0:50] + '...'
                            if cli_print:
                                print(f'3: {key_1}: {i}: {key_3}: {val_3}')
                elif isinstance(val_2, list):
                    if cli_print:
                        print(f'2: {key_1}: {i}: (list)')
                    pass
                else:
                    if cli_print:
                        print(f'2: {key_1}: {i}: {val_2}')
                    pass
        else:
            if cli_print:
                print(f'1: {key_1}: {val_1}')
            output[key_1] = val_1
    if cli_print:
        print(output)
    output['language'] = lang
    return output

# Count words in a string
def words(text):
    words = len(str(text).split(' ')) - 1
    nowords = str(text).count(' + ') * 2 - 1  # Don't count keyboard shortcuts (e.g. "Ctrl + Shift + Alt + Key-S")
    nowords += str(text).count(' - ')  # Don't count this, too.
    nowords += str(text).count(' > ')
    return words - nowords

# Extract info out of file path
def info_line(file_path):
    path = str(file_path).replace('\\', '/')  # Replace backslashes in case of Windows paths
    path_parts = path.split('/')
    proj_parts = path_parts[path_parts.index('Projects') + 1]
    cat_part = path_parts[path_parts.index('Schemas') + 1]
    line = {'Project': proj_parts, 'Category': cat_part, 'File': path_parts[-1], 'Path': path.split('Superalgos/')[1]}
    return line

# Search and process all Docs files
def filelist(project_path):
    i = 0
    file_list = []

    for (root, dirs, files) in os.walk(project_path):
        for f in files:
            # if True:
            try:
                path = root+'/'+f
                if "Schemas/Docs-" in root:
                    if i == stop:  # stopper (for testing)
                        break
                    line = info_line(path)  # get info from file path
                    add = read_json(path, cli_print)  # get info out of the json file
                    for key in add:
                        line[key] = add[key]  # add json info to the path info dictionary
                    # print(f"{line['Wordcount']} {line['Project']} > {line['Category']} > {line['Title']}")
                    # print(line['File'])
                    file_list.append(line)
                    i += 1
            except:
                print('Error processing ' + f + '. Check JSON structure and keys.')  # Add str(sys.exc_info()) for error details
        if i == stop:  # stopper (for testing)
            break
    return file_list
    print(f'Processed {i} Docs files in {project_path}.')
    print(f'List stored in {os.getcwd()}/{output_file}.')

def save_csv(file_list, csv_filename):
    date = datetime.datetime.now()
    csv_filename = (date.strftime('%y%m%d-%H%M')) + '_' + csv_filename
    with open(csv_filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        line = file_list[0]
        head = []
        for name in line:
            head.append(name)  # generate comma separated line from dictionary
        csvwriter.writerow(head)
        for line in file_list:
            row = []
            for name in line:
                row.append(line[name])  # generate comma separated line from dictionary
            csvwriter.writerow(row)

file_list = filelist(project_path)
# for i in file_list:
#     print(i)
save_csv(file_list, csv_filename)
