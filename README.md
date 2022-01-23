# SuperalgosDocsTools

*SaDocsList/SaDocsListWordcount.py*

Lists and extract info (incl. wordcount) out of all Superalgos Docs files into csv format.

Output example (yymmdd-hhmm_Superalgos_Docs_list.csv):
![image](https://user-images.githubusercontent.com/76875781/149655552-1d0a688f-1bd2-4338-b700-0483b4673934.png)



*SaDocsMerger.py*

Appends german translations from separate files to the original repo files. Processes all files that are listed in files_list.txt.
See comments for usage and details.

My personal workflow:
- Move/copy outdated (or conflicting) files with translations in a separate Superalgos file structure (source_path, e.g. /home/user/Superalgos-DE) 
- List according file paths in files_list.txt (paths have to start at "Projects/..." and can be copied from the PR on github in case of conflicts after committing)
- Update Superalgos (project_path, e.g. /home/user/Superalgos) 
   -- or hard reset if necessary (https://stackoverflow.com/questions/9646167/clean-up-a-fork-and-restart-it-from-the-upstream)
- Set up and run SaDocsMerger.py 
   - original files are backed up (backup_path) and merged files are written to a different folder (save_path)
- Compare files with Meld
- Copy approved files into the Superalgos structure

Why?
I'm new to github, commited several files and as they didn't get merged due to a conflict for over 10 days, almost all my files got outdated. 



*SaDocsTranslator.py*

Helper for Translations. Under construction...
