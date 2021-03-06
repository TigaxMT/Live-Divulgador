import os
from sqlalchemy import create_engine, MetaData
from psycopg2 import OperationalError as PostgreSqlError
from sqlalchemy.exc import OperationalError as SqlAlchemyError
from dotenv import load_dotenv

load_dotenv()

user_db = os.getenv('user_db')
passwd_db = os.getenv('passwd_db')

if user_db is None or user_db == '':
    raise ValueError('user_db não encontrado')

if passwd_db is None or passwd_db == '':
    raise ValueError('passwd_db não encontrado')

try:
    engine = create_engine(
        "postgresql://{}:{}@localhost:5432/streamers".format(
            user_db, passwd_db
        )
    )

    engine.execute(
        "CREATE TABLE IF NOT EXISTS livecoders (Nome varchar(50), Id integer,\
    Twitch varchar(150), Twitter varchar(50), OnStream boolean, Print boolean,\
    Tipo varchar(5), Hashtags varchar(300))"
    )

    # Guardar objeto da table livecoders
    metadata = MetaData(bind=engine)

    # Por algum motivo o reflect=True no MetaData deixou de funcionar
    # tendo então de chamar o método reflect
    metadata.reflect()

    livecoders = metadata.tables["livecoders"]
except PostgreSqlError as e:
    print(e)
    exit()
except SqlAlchemyError as e:
    print(e)
    exit()


def return_streamer_info():
    # Retonar as os valores das colunas de todos os streamers
    result = engine.execute("SELECT * FROM livecoders")

    return result


def return_streamer_names():
    # Retorna o nome dos streamers
    result = engine.execute("SELECT Nome FROM livecoders")

    return result


def insert_streamers(streamers):
    # Insere novos streamers na DB
    for index, row in streamers.iterrows():

        ins = livecoders.insert().values(
            nome=row["Nome"],
            id=int(row["Id"]),
            twitch=row["Twitch"],
            twitter=row["Twitter"],
            onstream=row["OnStream"],
            print=row["Print"],
            tipo=row["Tipo"],
            hashtags=row["Hashtags"],
        )

        engine.execute(ins)

    return


def insert_on_stream(idt, value):
    # Atribui true ou false à coluna OnStream
    upd = (
        livecoders.update()
        .values(onstream=value)
        .where(livecoders.c.id == idt)
    )
    engine.execute(upd)

    return


def update_name(idt, name, twitch):
    """ Função que atualizar o nome e o link com base no id"""

    # Atualizar nome
    upd = (
        livecoders.update()
        .values(nome=name, twitch=twitch)
        .where(livecoders.c.id == idt)
    )
    engine.execute(upd)

    return


def delete_streamer(idt):
    """ Função que elimina streamer da DB com base no id"""
    delete = livecoders.delete().where(livecoders.c.id == int(idt))
    engine.execute(delete)

    return
