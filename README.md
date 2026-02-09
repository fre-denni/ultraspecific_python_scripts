# Ultra specific Python scripts
I have a bunch of ultra-specific and weird python scripts laying around. I'm gonna start putting them here to share and have a repository of them.
Maybe someone will have a less specific use of them, maybe some of them are actually useful.

A list of them are:
- resize.py: I'm using this to resize all the memes in my meme folder to 491px height, as I find it good enough to be displayed on my desktop
- export.py: A script that I cobble together to use pandoc with obsidian links and convert them to citation using the Pandoc Reference List plugin for Obsidian. Yes it is a complete mess, why I do this to myself, I don't know. It gets as arguments the .md file to parse and the .docx file to output. Easily modifiable, ultra-specific to set up
- fetchData.py, runScripts.py, createExcels.py, unifyComp.py, unifyEco.py: maybe these ones are actually useful. These are scripts that I use in my ICH Atlas visualisations to manage and download the files from .csv file that I host in the web. To make them work you need panda and xlsxwriter. They basically works like this:
  - runScripts.py calls all the other scripts
  - fetchData.py will check a .csv file called "links.csv" and download the associated databases
  - createExcels.py will then call unifyComp.py and unifyEco.py
  - These last two scripts will get two specific datasets as .csv and then transform them in .xlsx file with more sheets inside.


  ---

  ### ALL OF THESE SCRIPTS ARE FREE-TO-USE AND FREE-TO-MISUSE. IF YOU FIND A WAY TO USE THEM THAT IS NOT ULTRA-SPECIFIC, PLEASE LET ME KNOW I'M CURIOUS. You can use it for whatever purpose you like, except evil.
