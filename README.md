# remote_sensing

Здесь собраны блокноты IPython (Jupyter), которые используются для документирования экспериментов в области ДЗЗ.


## Замечания по установке

Для запуска GRASS из блокнотов (использования модуля grasslib.py) необходимо предварительно установить переменную export `LD_LYBRARY_PATH` **до** вызова `Jupyter`, иначе при импорте возникнет ошибка связывания библиотек, т.к. установка этой переменной в ходе исполнения не работает (см. http://stackoverflow.com/questions/856116/changing-ld-library-path-at-runtime-for-ctypes):
```
export LD_LIBRARY_PATH=/usr/lib/grass70/lib
```

После установки переменной можно запускать `Jupyter`:
```
jupyter notebook
```
Или в фоновом режиме:
```
jupyter notebook 2> /dev/null > /dev/null &
```
