from sqlalchemy import create_engine, text

db_connection_string = "mysql+pymysql://2naahj3wjte7sag4lgll:pscale_pw_aHoiZ6aD6S7rZCyYDAlUAXxjie1DrD5oxLxXDTaBCqh@ap-southeast.connect.psdb.cloud/sportsgowhere_db?charset=utf8mb4"

engine = create_engine(
    db_connection_string,
    connect_args={
        "ssl": {
            "ssl_ca": "/etc/ssl/cert.pem"
        }
    })


#def load_accounts_from_db():
   # with engine.connect() as conn:
        #result = conn.execute(text("select * from Accounts"))
        #accounts = []
        #for row in result.all():
            #accounts.append(dict(row))
        #return accounts


def load_accounts_from_db():
    return
    with engine.connect() as conn:
        result = conn.execute(text("select * from Accounts"))
        print(result)
        return result


