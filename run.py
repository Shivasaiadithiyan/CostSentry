from Backend import myDB
from Furniture import Furniture


DB = myDB()
DB.createDB()
myScrapper = Furniture()
myScrapper.run()
