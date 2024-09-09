import psycopg2

def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""create table if not exists client (
            id serial primary key,
            name varchar(20) not null,
            surname varchar(20) not null,
            email varchar(40) unique check (email like '%@%'),
            phone varchar(20) unique check (phone like '+%')
        );
        """)
        conn.commit()

def add_client(conn, first_name, last_name, email, phones=None):
    with conn.cursor() as cur:
        sql_select_query = 'insert into client (name, surname, email, phone) values (%s, %s, %s, %s);'
        cur.execute(sql_select_query, (first_name, last_name, email, phones))
        conn.commit()

def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        sql_update_query = 'update client set phone = %s where id = %s;'
        cur.execute(sql_update_query, (phone, client_id))
        conn.commit()

def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    with conn.cursor() as cur:
        if first_name != None:
            sql_update_query = 'update client set name = %s where id = %s;'
            cur.execute(sql_update_query, (first_name, client_id))
        if last_name != None:
            sql_update_query = 'update client set surname = %s where id = %s;'
            cur.execute(sql_update_query, (last_name, client_id))
        if email != None:
            sql_update_query = 'update client set email = %s where id = %s;'
            cur.execute(sql_update_query, (email, client_id))
        if phones != None:
            sql_update_query = 'update client set phone = %s where id = %s;'
            cur.execute(sql_update_query, (phones, client_id))
        conn.commit()

def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        sql_update_query = 'update client set phone = %s where id = %s;'
        cur.execute(sql_update_query, (phone, client_id))
        conn.commit()


def delete_client(conn, client_id):
    with conn.cursor() as cur:
        sql_delete_query = 'delete from client where id = %s;'
        cur.execute(sql_delete_query, (client_id,))
        conn.commit()

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:
        if first_name != None:
            sql_select_query = ("""select c.id, c.name, c.surname, c.email, c.phone from client c
                                    where c.name = %s
                                    group by c.id;
                                """)
            cur.execute(sql_select_query, (first_name,))
            print(cur.fetchall())
        if last_name != None:
            sql_select_query = ("""select c.id, c.name, c.surname, c.email, c.phone from client c
                                                where c.surname = %s
                                                group by c.id;
                                            """)
            cur.execute(sql_select_query, (last_name,))
            print(cur.fetchall())
        if email != None:
            sql_select_query = ("""select c.id, c.name, c.surname, c.email, c.phone from client c
                                                where c.email = %s
                                                group by c.id;
                                            """)
            cur.execute(sql_select_query, (email,))
            print(cur.fetchall())
        if phone != None:
            sql_select_query = ("""select c.id, c.name, c.surname, c.email, c.phone from client c
                                                where c.phone = %s
                                                group by c.id;
                                            """)
            cur.execute(sql_select_query, (phone,))
            print(cur.fetchall())


with psycopg2.connect(database="test", user="postgres", password="postgres") as conn:
    create_db(conn)

    add_client(conn, 'Anton', 'Adam', 'anton@gmail.com', '+7000')
    add_client(conn, 'Danil', 'Dan', 'dan@gmail.com', '+7001')
    add_client(conn, 'Dima', 'Don', 'don@gmail.com')

    add_phone(conn, 3, '+7002')

    change_client(conn, 3, 'Dmitriy', 'Donskoy', 'dima@gmail.com')

    delete_phone(conn, 1, phone=None)

    delete_client(conn, 2)

    find_client(conn, last_name='Donskoy')

conn.close()