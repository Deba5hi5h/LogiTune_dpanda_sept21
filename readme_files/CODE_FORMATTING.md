
### 1. pylint

`pylint` is a tool for finding bugs and style problems in Python source code. It finds problems that are typically caught by a compiler for less dynamic languages like C and C++. Because of the dynamic nature of Python, some warnings may be incorrect; however, spurious warnings should be fairly infrequent.

#### A. _Pros_

Catches easy-to-miss errors like typos, using-vars-before-assignment, etc.

#### B. _Cons_

pylint isn’t perfect. To take advantage of it, sometimes we’ll need to write around it, suppress its warnings or fix it.

#### C. _How to configure_
Install `pylint` library (included in `requirements.txt`)

```commandline
$ pip install pylint==2.13.4
```

Install pylint plugin:

<img width="734" alt="pyling_plugin" src="https://user-images.githubusercontent.com/64977502/162045860-e1d2b8a5-8dc8-4158-a2a7-46d87b029bc7.png">

#### D.  **How to run**
Open pylint label at the bottom and press play to run analysis on open file.

<img width="947" alt="image" src="https://user-images.githubusercontent.com/64977502/162047179-508b7c9a-156a-4e66-a982-0fe72d3bdcee.png">

### 2. Black auto-formatter

https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html

#### How to configure

A. Install black.

```commandline
$ pip install black==22.3.0
```

B. Locate your black installation folder.

On macOS / Linux / BSD:

```commandline
$ which black
$ /usr/local/bin/black  # possible location
```

On Windows:

```commandline
where black
LocalAppData%\Programs\Python\Python36-32\Scripts\black.exe  # possible location
```
#### Note that if you are using a virtual environment detected by PyCharm, this is an unneeded step. In this case the path to black is $PyInterpreterDirectory$/black.

C. Open External tools in PyCharm/IntelliJ IDEA

On macOS:

`PyCharm -> Preferences -> Tools -> External Tools`

On Windows / Linux / BSD:

`File -> Settings -> Tools -> External Tools`

Click the + icon to add a new external tool with the following values:

```commandline
Name: Black

Description: Black is the uncompromising Python code formatter.

Program: <install_location_from_step_B>

Arguments: "$FilePath$"
```

<img width="783" alt="image" src="https://user-images.githubusercontent.com/64977502/162051266-c51b007e-4a2a-4362-b72f-a106beebdbbc.png">

Format the currently opened file by selecting `Tools -> External Tools -> black`.

Alternatively, you can set a keyboard shortcut by navigating to Preferences or `Settings -> Keymap -> External Tools -> External Tools - Black.`
