# Ultra specific Python scripts
I have a bunch of ultra-specific and weird python scripts laying around. I'm gonna start putting them here to share and have a repository of them.
Maybe someone will have a less specific use of them, maybe some of them are actually useful.

A list of them are:
- resize.py: I'm using this to resize all the memes in my meme folder to 491px height, as I find it good enough to be displayed on my desktop
- export.py: A script that I cobble together to use pandoc with obsidian links and convert them to citation using the Pandoc Reference List plugin for Obsidian. Yes it is a complete mess, why I do this to myself, I don't know. It gets as arguments the .md file to parse and the .docx file to output. Easily modifiable, ultra-specific to set up
- fetchData.py, runScripts.py, createExcels.py, unifyComp.py, unifyEco.py: maybe these ones are actually useful. These are scripts that I use in my ICH Atlas visualisations to manage and download the files from .csv file that I host in the web. To make them work you need the libraries `panda` and `xlsxwriter`. They basically works like this:
  - runScripts.py calls all the other scripts
  - fetchData.py will check a .csv file called "links.csv" and download the associated databases
  - createExcels.py will then call unifyComp.py and unifyEco.py
  - These last two scripts will get two specific datasets as .csv and then transform them in .xlsx file with more sheets inside.
- convert-to-webp.py : This script check if a folder called "png" and one called "webp" exists: if no it creates them, if yes it checks all the files inside the png folder (and the directories) -> convert the files to `.webp` and it copy them inside the same folder structure in the webp folder
- csv-to-md.py: Another conversion script. This one it's one of the most complicated but also versatile, I think. I'm using Obsidian (with the plugin Quadro) to make QDA analysis with tagging and coding. As I was working with posts from social media, I needed to separate all the different files individually. Obsidian is able to work with 20000+ file, so I decided to split each posts in singular files. Right now I worked with 400+ posts and it parse it and convert it in seconds. So no issue at all. I think it could be repurposed also to get data from sheets to work better with AIs (it seems they prefer markdown? I don't know). Nevertheless, it works like this: 
  - From the CLI you need to specify an url for a webhosted `.csv` table (I usually work with Google Sheet, so it's easier for me), then you need to define the output folder in which you want your `.md` files. Then you can specify two arguments, both required: `--content-col` with the name of the column in which you need your content exctrated and `--title-prefix` that is used to give a title to each of the `.md` files (it would be like: `000-title.md`). The script will then extract all the text and by row divide it in different files. As I use it with Obsidian, I think one further development would be also the option to add data from other columns in the YAML of the singular `.md` file. This can easily be set up in the line 99-100. 

  ---

  ### ALL OF THESE SCRIPTS ARE FREE-TO-USE AND FREE-TO-MISUSE. IF YOU FIND A WAY TO USE THEM THAT IS NOT ULTRA-SPECIFIC, PLEASE LET ME KNOW I'M CURIOUS. You can use it for whatever purpose you like, except evil.
