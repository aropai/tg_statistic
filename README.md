# Telegram statistics
Here you can find a program that somehow analyze your
Telegram conversations. Right now for each chat member **it
can**:
* count his messages
* count the symbols he's written
* count his average message length
* determine who replied him the most and to whom did he
replied the most
* determine and count his most often used meessages

## Installation
### Requirements:
* Python 3
* All from [requirements.txt](https://github.com/nnrpi/tg_statistic/blob/master/requirements.txt)
file

### How to download this project:
Just create a new directory for the project and clone it there
by using
`git clone https://github.com/nnrpi/tg_statistic.git`

## Usage
1. **Export** the Telegram chat you want to analyze:
    * Open this chat
    * Click on 3 dots in the right up corner ![](Pictures/1337chat.jpg)
    * Click on "Export chat history" ![](Pictures/1337export_chat.jpg)
    * Make all like in the picture below and click on the "Export"
    button ![](Pictures/1337exporting.jpg)
    * After this your chat exporting will start. Wait till it ends
    * You will see a directory called like 'ChatExport_<today_date>'.
    There could be several files, the one you need is called "result.json"
2. **Run** the program:
    * Open Terminal, go to the project's directory and run
    the program by using `./main.py ~/path/to/the/result.json`.
    *Congratulations*, you did it!!! You should see the output like:
    ![](Pictures/1337output1.jpg)
    ![](Pictures/1337output2.jpg)