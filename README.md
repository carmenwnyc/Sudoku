# Sudoku

The objective of Sudoku is to fill a 9x9 grid with the numbers 1-9 so that each column, row, and 3x3 sub-grid (or box) contains one of each digit. You may try out the game here: sudoku.com. Sudoku has 81 variables, i.e. 81 tiles. The variables are named by row and column, and are valued from 1 to 9 subject to the constraints that no two cells in the same row, column, or box may be the same.

The program takes an input string and output a string that represents a finished Sudoku board.<br/>
The command to run the program:
$python3 sudoku.py <input string>

An input string is made up of 81 numbers that represent a 9x9 grid Sudoku board. For example:
003020600900305001001806400008102900700000008006708200002609500800203009005010300
Which is equivalent to:
003020600<br/>
900305001<br/> 
001806400<br/>
008102900 
700000008 
006708200 
002609500 
800203009 
005010300
