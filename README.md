# michigan_card_reader
Setup Instructions (one time)

1. Skip this step if you already have python 3 installed on your computer.
Otherwise, follow the directions on this site.

https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-macos

Stop after you run the command "brew install python3" in step 4, as you will now
have python 3 and you don't need any of the other stuff after that.

2. Create a folder for the program to live in. Every time you run it and create
a new guest list, it creates a new file, so put the program in an empty folder
so that it will only ever contain the program itself and the files it creates.
It's easiest to just keep it on your desktop. Don't put spaces into the folder
name, having spaces makes navigating to it much harder.

Instructions for running (every time)

1. Open terminal and navigate to that file. There are a few simple terminal
commands that you'll need to know to do this.

- cd changes the directory that terminal is looking at and you need to use it
  to navigate to your folder.
- if you navigate to the wrong directory, type cd .. to go back one step.
- ls shows the files that are in the folder you're in, you can just use it
  to make sure you get to the next folder correctly.

2. Now that I'm in the correct directory, I can run the program with:
  > python cardSwiper.py

3. The program will now be running, so here's a few important notes about it.

  - I'd recommend turning on caps lock once you start running it, as you need
    to use all caps to search and enter names.

  - Because of the way the mcards give info for names, you have to search and
    enter names in a weird way. my name would be GODLEY,W

  - When you're creating the guest list, you MUST use the QUIT command when
    you're done. If you don't, the excel file won't be created/updated. If
    you have to us control + c to force quit, just restart it and only the
    last entry won't be saved. Everything else will be in another file,
    and will update to the excel sheet when you exit the program properly

  - The program supports swiping out, the person just swipes their card again
    if they have an mcard. The program will only give the time entered If the
    person doesn't swipe out.

  - If you want to save the data at any point while you are swiping people in,
    just type QUIT, then start the program again. As long as you type in the
    date correct again, you will be using the same file so swiping in new people
    will save it for the file for that date and swiping out will work.
