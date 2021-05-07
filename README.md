# Sudoku

## Sudoku Game Explained
* The objective of Sudoku is to fill a 9x9 grid with the numbers 1-9 so that each column, row, and 3x3 sub-grid (or box) contains one of each digit. You may try out the game here: sudoku.com. Sudoku has 81 variables, i.e. 81 tiles. The variables are named by row and column, and are valued from 1 to 9 subject to the constraints that no two cells in the same row, column, or box may be the same.

## Running the Program
* The program takes an input.txt file with input strings and output a output.txt file containing strings that represents finished Sudoku boards for each board represented by the input strings from input.txt file.<br/>
The command to run the program:<br/>

'''
python3 sudoku.py input.txt
'''

* An input string is made up of 81 numbers that represent a 9x9 grid Sudoku board. For example:<br/>
003020600900305001001806400008102900700000008006708200002609500800203009005010300<br/>

Which is equivalent to:<br/>
<br/>
003020600<br/>
900305001<br/> 
001806400<br/>
008102900<br/>
700000008<br/>
006708200<br/>
002609500<br/>
800203009<br/>
005010300<br/>
