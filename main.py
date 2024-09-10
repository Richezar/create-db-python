import psycopg2

def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""create table if not exists client (
                    id serial primary key,
                    name varchar(20) not null,
                    surname varchar(20) not null,
                    email varchar(40) unique check (email like '%@%')
        );
        """)
        cur.execute("""create table if not exists client_phone (
                    id serial primary key,
                    client_id integer references client(id), 
                    phone varchar(20) unique check (phone like '+%')
                );
                """)

def add_client(conn, first_name, last_name, email, phones=None):
    with conn.cursor() as cur:
        sql_insert_query = 'insert into client (name, surname, email) values (%s, %s, %s);'
        cur.execute(sql_insert_query, (first_name, last_name, email))
        if phones != None:
            sql_insert_query = f'''insert into client_phone (client_id, phone) values ((select c.id as client_id from client c 
where c.name = '{first_name}' and c.surname = '{last_name}' and c.email = '{email}'), %s);'''
            cur.execute(sql_insert_query, (phones,))

def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        sql_insert_query = 'insert into client_phone (client_id, phone) values(%s, %s);'
        cur.execute(sql_insert_query, (client_id, phone))

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
            sql_update_query = 'update client_phone set phone = %s where client_id = %s;'
            cur.execute(sql_update_query, (phones, client_id))

def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        sql_update_query = 'delete from client_phone where client_id = %s and phone = %s;'
        cur.execute(sql_update_query, (client_id, phone))

def delete_client(conn, client_id):
    with conn.cursor() as cur:
        sql_delete_query = 'delete from client_phone where client_id = %s;'
        cur.execute(sql_delete_query, (client_id,))
        sql_delete_query = 'delete from client where id = %s;'
        cur.execute(sql_delete_query, (client_id,))

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:
        sql_select_query = ("""select c.id, c.name, c.surname, c.email, cp.phone from client c
                                    left join client_phone cp on c.id = cp.client_id
                                    where c.name = %s or c.surname = %s or c.email = %s or cp.phone = %s
                                """)
        cur.execute(sql_select_query, (first_name, last_name, email, phone))
        print(cur.fetchall())

if __name__ == '__main__':
    with psycopg2.connect(database="test", user="postgres", password="postgres") as conn:
        create_db(conn)

        add_client(conn, 'Anton', 'Adam', 'anton@gmail.com', '+7000')
        add_client(conn, 'Dima', 'Don', 'don@gmail.com')
        add_client(conn, 'Danil', 'Dan', 'dan@gmail.com', '+7001')

        add_phone(conn, 2, '+7002')

        change_client(conn, 2, 'Dmitriy', 'Donskoy', 'dima@gmail.com', '+33')

        delete_phone(conn, 1, '+7000')

        delete_client(conn, 3)

        find_client(conn, 'Anton')

    conn.close()