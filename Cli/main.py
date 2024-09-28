import typer
from Utils.ConfLoader import ConfLoader
from Db.DbManager import DbManager

app = typer.Typer()
db = DbManager()
conf = ConfLoader()

@app.command()
def savetestinfo():
    print("Saving test info")
    
if __name__ == "__main__":
    app()