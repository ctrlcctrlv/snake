snake
=====

Full featured Python snake game. Supports Py2k and Py3k.

I recommend that you use a square font. On my system, the optimal font definiton to use is `-schumacher-clean-medium-r-normal--8-80-75-75-c-80-iso646.1991-irv` and is provided by the file `/usr/share/fonts/misc/clR8x8.pcf.gz`. So I run the xterm that will be launching snake with:

```
xterm -fn -schumacher-clean-medium-r-normal--8-80-75-75-c-80-iso646.1991-irv -bg black -fg white
```

To see font definitons on your system, look at the file `fonts.dir` in your X11 font directory or use the `xfontsel` program.

For a full list of options, type `./snake.py -h`.

snake supports maps. To use the example map, type `./snake.py map.smp`. The provided `rendermap_image.py` script generates maps from images using PIL. 
