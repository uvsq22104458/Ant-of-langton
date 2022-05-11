# **Ant of Langton project**
>**Group BI 2
Bastien COMBES
Adrien AUGIS
Many AFAGHPOUR
Perrine ILARY**
>>[Ant of Langton project](https://github.com/uvsq22104458/ant_of_langton_project)
------------------------------------------------------------------
![Ant of Langton](https://media4.giphy.com/media/y3bYxboJL1YL5k9biK/giphy.gif?cid=790b761173be56ccf2fc87cc6fc86b9eac1b91fa3199bbcf&rid=giphy.gif&ct=g 'Ant')

> 💠 ***```The Langton Ant is a cellular automaton composed of a grid of two dimensions and an ant.```*** 💠

## **Rules**
The rules for the ant for a single iteration:

* If the ant is at a white square, rotate 90 degrees right, if it's at a black square, rotate left.
* Change the color of the square in the ant's current position (black turns to white, white turns to black).
* Move forward one space.
* Repeat these steps for each iteration.

## **Features**
* Button Play/Pause : This allows the steps to be carried out as long as it is active.
* Button Next : This allows you to do one iteration at a time.
* Button Back : This allows you to go back in iteration.
* Button Save : Saves a current instance to a file.
* Button Load : Opens a registered instance.
* Button quit : Quit the program.
* Entry to change the delay between each iteration : Select a number and click on 'Set', its allow you to change the delay. Max value is 200.
* Entry to change the scale of the grid : Select a number and clic on 'Set', its allow you to change the scale of the grid. Be aware, it reset the grid. Max value is 200.
* Iteration counter : In the grid, count each iteration. It can increase or decrease using Button back.
* Creates an ant on click and set the clicked square to red.

## **Futher improvements**
The rules can be modified to integrate multiple colors that affects the ants movements.

[Full explanation here](http://www.thealmightyguru.com/Wiki/index.php?title=Langton%27s_ant#Additional_Rules)