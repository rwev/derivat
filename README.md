# derivat
Desktop application for theoretical visualization of financial derivatives, using PyQT, Cython, and OpenGL.

## Getting Started

To run the application, 

1. Assure installation of *Python 2.7* with *pip* and (optionally) *virtualenv* packages installed
2. Clone the repository
   ```shell
   > git clone https://github.com/rwev/derivat.git
   ```
3. Navigate to the repository with CLI
    ```shell
   > cd derivat
   ```
4. (Optional, but recommended): create an isolated virtual environment
   ```shell
   \derivat > virtualenv <name>
   ```
   This is to mitigate version conflicts with the global system Python installation. This project intentionally relies on some former package versions.
5. Install dependencies
   
   **PyQt4**: download the Windows wheel (*.whl*) file [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyqt4) (be sure to select *cp27* for Python 2.7) and and manually install: 
   ```shell
   \derivat > pip install PyQt4-4.11.4-cp27-<bit-system>.whl
   ```
   All other dependencies can be automatically installed with
   ```shell
   \derivat > pip install -r requirements.txt
   ```
6. Compile Cython valuation module
    ```shell
    \derivat > python components\libs\setup.py build_ext --inplace
    ```
7. Execute
   ```shell
   \derivat > python derivat.py 
   ```
## Contribution

To-date development has been done exclusively in Visual Studio Code for Windows, with the assistance of a custom execute-on-change tool [resurgence.py](https://gist.github.com/rwev/cb5d117c9dbe0efb923e4bb1ed3619f0). 

### Debug Configuration

```javascript
    {
        "name": "Python: Resurgence",
        "type": "python",
        "request": "launch",
        "program": "${path}/resurgence.py",
        "args": [
            "--cwd",
            "--extensions=*.py",
            "--dirs=./components", 
            "--command=${path}/derivat/python.exe derivat.py"
        ],
    }
```

While running this configuration, a change of one of the *.py* source files in the project directory or the *components/* subdirectories will restart the program execution (*python derivat.py*). See *python resurgence.py --help* or read the source for more details on this mechanism. 







