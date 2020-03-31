# ArxivScraper
## What is ArxivScraper?
This program is to get arxiv information from terminal.


## Usage
### 3: move to home foleder
```
cd ~
```

### 2: clone files
```
git clone https://github.com/DOALA0155/ArxivScraper.git
```

### 3: create and activate environment
```
python3 -m venv [environment_name]
source [environment_name]/bin/activate
```

### 4: install libraries
```
pip3 install requests
pip3 install beautifulsoup4
```

### 5: run python file
```
python3 get_arxiv.py "[search word]"
```

## Create short cut
### 1: put arxiv folder on home folder
```
mv arxiv ~/
```

### 2: edit ~/.bashrc or ~/.zshrc file
```
vim ~/.bashrc or vim~/.zshrc
```
```
arxiv () {
    source ~/shell_env/bin/activate
    python3 ~/arxiv/get_arxiv.py "$1"
    deactivate
}
```
```
source ~/.bashrc or source ~/.zshrc
```

### 3 use arxiv command
```
arxiv [search word]
```
