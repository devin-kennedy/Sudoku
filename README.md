# Sudoku Solver

In this project, I took some base code I had worked on in my Computer Science III class and created an automatic solver to be used on a website.

## What the program does

First, the program opens a sudoku website and finds and captures the board from the website, saving the board itself as a .png file

Next, the program isolates each cell and iterates over the cells, using OCR to read the contents of the cell

Now that the program knows the board, it runs the parsed board through the solving algorithm to produce a solved board in the 'parsed' format

The program then takes the solved board data and writes the correct numbers at their respective spot on the board, and displays the solved board to the user
