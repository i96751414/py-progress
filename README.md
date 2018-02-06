<h1 align="center">
  <img alt="py-progress" src="https://www.python.org/static/opengraph-icon-200x200.png" width="200px" height="200px"/>
  <br/>
  py-progress
</h1>
<p align="center">Minimalistic implementation of a progress bar in Python</p>
<br/>
This is a very minimalistic implementation of a text progress bar in Python (both 2 and 3). If your needs require something more complex, please take a look into <a href="https://github.com/WoLpH/python-progressbar">python-progressbar</a>.


## Usage
To use py-progress, simply import Progress class. Then, using the ```with``` statement, you will be able to update the progress.

```python
from progress import Progress

with Progress() as p:
    p.update(1)
```

```
>>> [########################################] 100% | Time: 0:00:00
```

It is also possible to use Progress without using ```with``` statement. In this case, you will have to manually initialize and close the progress bar.

```python
from progress import Progress

p = Progress()
p.init()
p.update(1)
p.close()
```

```
>>> [########################################] 100% | Time: 0:00:00
```

- **Progress**

    Parameters are the following:
    
    | Param | Description | Type |
    | :--: | :-- | :--:|
    | show_time | Show time passed since progress bar was initialized | bool |
    | keep_bars | Keep progress bars while printing in the middle | bool |
    | keep_final | Show progress bar after finished | bool |
    | size | Size of the progress bar | integer |