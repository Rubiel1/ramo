PROJECT RAMO
============

This program reads several pdf's located on the folder and finds common phrases among all files. It also returns all common words. Fake research papers may share common words, and this tool automatizes the search for common prhases.

You dont need to know how to code to use this program just follow the colab notebook at https://colab.research.google.com/drive/1ZdOw8O5Bwq9WKFIPbHlcUTHKLFPyVmJn?usp=sharing

The function analyzer has two parameters, the name of the folder and the size
-the folder should be located at the same place that the file main,
-size is the minimun number of words that a phrase should have.
Note that size = 1 asks for all words shared by all documents, we actually return this value, so use size>1.

Example:
>> analyzer("mill",3)

Requirements:
- numpy
- scipy
- scikit-learn==0.23.1
- pdfminer>=1.3.1 


### ramo
After don Quijote lost his spade while attacking the mill, he explained to Sancho the advantages of using a "ramo" instead of a "espada":
"-Yo me acuerdo haber leído que un caballero español llamado Diego Pérez de Vargas, habiéndosele en una batalla roto la espada, desgajó de una encina un pesado ramo o tronco, y con él hizo tales cosas aquel día, y machacó tantos moros, que le quedó por sobrenombre Machuca..."
Don Quixote
Novel by Miguel de Cervantes
