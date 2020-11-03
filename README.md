# Asana for Conky

## Description

fetch asana tasks and write them to a (conky config) file

## Install

1. Copy `configuration.template.yaml` and rename it to `configuration.yaml`
2. Fill out the configuration based on the comments within
3. Add the start and end tags to your conky conf file
4. `pip install asana==0.10.3`
5. run the program  
  a. `python fetch_tagged_tasks.py`   
  b. `python fetch_todays_tasks.py`
6. Install sytemd files  
  a. Move files in `./systemd` to your system's `systemd` folder  
  b. Edit the variables (eg. paths, timer interval) in the sytemd files  
  c. Enable and start them  

## Miscellaneous

This is a hobby project.  
There will be bugs.  
Use this project at your own risk.  
I do not take any responsible for any data loss or other damages.  
Should something be unclear or you find bugs - open an issue on [GitHub](https://github.com/TomLouisKeller/asana_conky)
