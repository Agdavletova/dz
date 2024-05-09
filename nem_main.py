import psycopg2


def create_table(cur):

    cur.execute("""
    CREATE TABLE IF NOT EXISTS client(
        id SERIAL PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL
    );
    """)
    conn.commit()

def create_table_phones(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS phones(
        id SERIAL PRIMARY KEY,
        client_id INTEGER REFERENCES client(id) ON DELETE CASCADE,
        telephone TEXT
    );
    """)
    conn.commit()

def add_client(cur, first_name, last_name, email, phones=None):
    cur.execute("""
        INSERT INTO client(first_name, last_name, email) 
        VALUES(%s, %s, %s)
        RETURNING id;
        """, (first_name, last_name, email))
    client_id = cur.fetchone()[0]
    if phones:
        cur.execute("""
            INSERT INTO phones(client_id, telephone)
            VALUES(%s, %s)
            RETURNING id;
            """,(client_id, phones))
    return client_id

def add_phone(cur, client_id, phone):
    cur.execute("""
    INSERT INTO phones(client_id, telephone) 
    VALUES(%s, %s);
    """, (client_id, phone))
    conn.commit()

def change_client(cur, client_id, first_name=None, last_name=None, email=None):
    if first_name:
        cur.execute("""
        UPDATE client 
        SET first_name = %s 
        WHERE id = %s;
        """, (first_name, client_id))
    if last_name:
        cur.execute("""
        UPDATE client 
        SET last_name = %s 
        WHERE id = %s;
        """, (last_name, client_id))
    if email:
        cur.execute("""
        UPDATE client 
        SET email = %s 
        WHERE id = %s;
        """, (email, client_id))
    conn.commit()

def delete_phone(cur, phone_id):
    cur.execute("""
    DELETE FROM phones 
    WHERE id = %s;
    """, (phone_id,))
    conn.commit()

def delete_client(cur, client_id):
    cur.execute("""
    DELETE FROM client 
    WHERE id = %s;
    """, (client_id,))
    conn.commit()

def find_client(cur, first_name=None, last_name=None, email=None, phone=None):
    conditions = []
    params = []

    if first_name:
        conditions.append("first_name = %s")
        params.append(first_name)
    if last_name:
        conditions.append("last_name = %s")
        params.append(last_name)
    if email:
        conditions.append("email = %s")
        params.append(email)
    if phone:
        conditions.append("phone = %s")
        params.append(phone)

    if conditions:
        condition_str = " AND ".join(conditions)
        cur.execute(f"""
        SELECT * FROM client 
        WHERE {condition_str};
        """, params)
    else:
        cur.execute("""
        SELECT * FROM client;
        """)
    return cur.fetchall()


def show_client(cur):
    cur.execute("""
            SELECT * FROM client;
                """)
    return cur.fetchall()

def show_phones(cur, client_id):
    cur.execute("""
        SELECT * FROM phones
        WHERE client_id = %s;
    """,(client_id))
    return cur.fetchall()


conn = psycopg2.connect(database="clients", user="postgres", password="password")
with conn.cursor() as cur:
    cur.execute("""
            DROP TABLE client, phones;
            """)
    create_table(cur)
    create_table_phones(cur)

    client_id_1 = add_client(cur, "Иван", "Иванов", "ivan@example.com")
    client_id_2 = add_client(cur, "Федя", "Ффффф", "a@ipsdo", "8988888779")
    add_phone(cur, client_id_1, "123-456-7890")
    add_phone(cur, client_id_1, "89822704444")
    print(show_client(cur))
    print(show_phones(cur, "1"))
    change_client(cur, client_id_1, last_name="Федоров")
    print(show_client(cur))
    delete_phone(cur, 2)
    print(show_phones(cur, "1"))
    # delete_client(cur, 1)
    # print(show_client(cur))
    print(find_client(cur, last_name="Ффффф", email="a@ipsdo"))

conn.close()