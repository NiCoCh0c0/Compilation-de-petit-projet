import mysql.connector

def select(column, table, where=None, order=None):
    """
    Return un tuple des éléments séléctionnés
    Parametres:
      - column : Nom de la colonne --> str() ou tuple()
      - table : Nom de la table --> str()

      - where : La condition si il faut faire un where --> str()
      - order : La condition du order (champ + ASC/DESC) --> srt()
    """
    mydb = connexion()
    my_cursor = mydb.cursor()
    if type(column) == tuple:
        column = ",".join(column)

    if where != None:
        request = "SELECT {} FROM {} WHERE {}".format(column, table, where)
    elif order != None:
        request = "SELECT {} FROM {} ORDER BY {}".format(column, table, order)
    else:
        request = "SELECT {} FROM {}".format(column, table)
    print(request)
    my_cursor.execute(request)
    result = my_cursor.fetchall()

    if len(result[0]) == 1:
        my_list = []
        for element in result:
            my_list.append(element[0])
        result = my_list

    return result




def connexion():
    """
    Return la base de donnée avec une connexion client
    """
    mydb = mysql.connector.connect(
        host="localhost",
        user="client",
        password="password",
        database="chat_en_ligne"
    )
    return mydb


def insert(table, column, values):
    """
    Permet de faire une insertion
    Parametres:
      - table : Nom de la table --> str()
      - column : Nom de la colonne --> str() ou tuple()
      - values : Nom de la valeur --> str() ou tuple() ou int()
    """
    if type(column) == tuple:
        column = str(column).replace("'", "")
    else:
        column = "({})".format(column)
        values = "({})".format(values)

    mydb = connexion()
    my_cursor = mydb.cursor()
    request = "INSERT INTO {} {} VALUES {}".format(table, column, values)
    print(request)
    my_cursor.execute(request)
    mydb.commit()


print(select("max(id)", "historique"))