# keyword-grabber
Similar to grep, it searches directories and sub-directories for keywords

# Examples:
1. Search for `# TODO:` and `# NOTE:` keywords in current and all subdirectories to current directory, and save them to a file `todo.csv` in csv format:
   ```
   python3 todo.py -d '.' -e '.py' -k '# TODO:' '# NOTE:' -f csv -o todo.csv
   ```
2. Search for `# TODO:` and print to screen, but exclude folder 'venv' and file `todo.py`:
   ```
   python3 todo.py -s 'venv' 'todo.py'
   ```
3. Find `# TODO:` keywords in todo.py:
   ```
   python3 todo.py -f markdown | grep todo.py
   ```
4. Similar grep command for searching for `# TODO:` keyword:
   ```
   grep -rnw './' -e '# TODO:'
   ```
