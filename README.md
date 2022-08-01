# pizzabox
> Always check to make sure the box is really empty. :pizza:

`pizzabox` is a CLI tool that allows you to inspect a GitHub workflow's [HTRVX](https://github.com/HTR-United/htrvx) log according to your own [SegmOnto](https://segmonto.github.io/) transcription's specifications.

This is useful because the HTRVX log, while verbose, can sometimes falsely flag a zone as problematic. With its configuration file, the `pizzabox` CLI allows the user to specify which text boxes can be empty. The CLI then generates an easy-to-read CSV file that points the user to the problematic zones, those which should not be empty, as well as any other problems with the data that the HTRVX workflow noticed.

## Output
`./output.csv`
| issue | tag | element | file |
| --- | --- | --- | --- |
| Zone missing a tag. | NA | eSc_dummyblock_ | \<file path> |
| Line missing a tag. | NA | line_65 | \<file path> |
| Zone should not be empty. | RunningTitleZone | eSc_textblock_d62ca85a | \<file path> |


## How does it work?
When set with the options `--check-empty` and `--segmonto`, a GitHub action's HTRVX log will run two tests. 

1. The `Segmonto test` checks to see that all the SegmOnto zones and lines have tags.
    ```
    × Segmonto test for <file path>: Invalid (0 wrongly tagged zones, 1 wrongly tagged lines)
        → *Empty* tag for lines is forbidden (1 annotations): #line_65
    ```
    The results of this first test are always important because an ALTO XML element should never be without a tag. The `pizzabox` CLI alerts the user to these problematic zones and lines in the output CSV.

2. The `check-emtpy` test checks to see that all the `<TextBlock>` elements have descending `<TextLine>` elements, and that all the `<TextLine>` elements have descending `<String>` elements, which should contain text.

    ```
    × Detection of empty lines or region in <file path>: Empty elements founds (2)
        → 2 empty zone(s) found: #eSc_textblock_d62ca85a, #eSc_textblock_34f1c416
        → 0 empty line(s) found: 
    ```
    This test is useful because many of the zones in the SegmOnto guidelines should have descendants. However, there is a significant number of zones that should, in fact, be empty. A list of these zones can be edited in the CLI's configuration file.

    `./package/config.py`
    ```python
    names_of_unproblematic_emtpy_zones = [
        "DamageZone", 
        "DropCapitalZone", 
        "GraphicZone", 
        "MusicZone", 
        "SealZone", 
        "StampZone", 
        "TableZone"
    ]
    ```
## How do you use the CLI?
### Requirements:
- Python v. 3.7
- git
- a GitHub project that follows the [Gallic(orpor)a](https://github.com/Gallicorpora) template
### Installation
1. From the terminal, download this GitHub repository and then change to that directory.
```shell
$ git clone https://github.com/kat-kel/pizzabox.git
$ cd pizzabox
```
2. Create a virtual environment, activate it, and install the CLI tool in that environment.
```shell
$ python 3.7 -m venv pizza-cli
$ source pizza-cli/bin/activate
$ pip install -e .
```
### Data
3. To use the CLI tool, you'll need to have downloaded a HTRVX log from a GitHub repository where you've been using the HTRVX workflow (with the `--verbose`, `--check-empty`, and `--segmonto` options). Download this log from GitHub onto your machine.
4. You'll also need to have recently pulled that same GitHub repository on your machine, so you have access to the data that the HTRVX workflow analysed.

### Execution
With the virtual environment on, in which you installed the CLI tool, call the `pizzabox` application with the following two options: (1) the relative path to HTRVX log you download on your local machine, and (2) the relative path to your project's cloned git repository on your local machine. 

To demonstrate the command, imagine you have the following file structure on your computer:
```
.
|---Dropbox/
|   |-------GitHub_Project/
|   |       |-------------.github
|   |       |             |----workflows/
|   |       |                  |---------HTRVX.yml
|   |       |-------------data/
|   |       |             |----document1/
|   |       |             |    |---------alto1.xml
|   |       |             |    |---------alto2.xml
|   |       |             ...
|   |       ...
|   ...
|---Downloads/
|   |-------logs_23/
|   |       ...
|   |       |-------------HTRVX/
|   |       |             ...
|   |       |             |----5_Run HTRVX.txt/
...
```
From, for example, the direcoty `./Dropbox`, and with the virtual environment `pizza-cli` activate, you would call the following comamnd:
```shell
(pizza-cli) $ pizzabox ../../Downloads/logs_23/HTRVX/5_Run\ HTRVX.txt ./GitHub_Project/
```