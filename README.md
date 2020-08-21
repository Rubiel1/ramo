The function analyzer has two parameters, the name of the folder and the size
-the folder should be located at the same place that the file main,
-size is the minimun number of words that a phrase should have.
Note that size = 1 asks for all words shared by all documents, we actually return this value, so use size>1.

Example:
analyzer("mill",3)

# ramo
-Yo me acuerdo haber leído que un caballero español llamado Diego Pérez de Vargas, habiéndosele en una batalla roto la espada, desgajó de una encina un pesado ramo o tronco, y con él hizo tales cosas aquel día, y machacó tantos moros, que le quedó por sobrenombre Machuca...
