CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE
    v_contact_id INTEGER;
BEGIN
    SELECT id INTO v_contact_id FROM phonebook WHERE first_name = p_name;

    IF v_contact_id IS NULL THEN
        INSERT INTO phonebook (first_name) VALUES (p_name)
        RETURNING id INTO v_contact_id;
    END IF;

    IF NOT EXISTS (SELECT 1 FROM phones WHERE contact_id = v_contact_id AND phone = p_phone) THEN
        INSERT INTO phones (contact_id, phone, type) VALUES (v_contact_id, p_phone, 'mobile');
    END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE bulk_insert_contacts(p_data VARCHAR[][])
LANGUAGE plpgsql AS $$
DECLARE
    i               INT;
    v_name          VARCHAR;
    v_phone         VARCHAR;
    v_contact_id    INTEGER;
    invalid_records VARCHAR[][] := ARRAY[]::VARCHAR[][];
BEGIN
    FOR i IN 1..array_length(p_data, 1) LOOP
        v_name  := p_data[i][1];
        v_phone := p_data[i][2];

        IF v_phone ~ '^\+?[0-9]{7,15}$' THEN
            SELECT id INTO v_contact_id FROM phonebook WHERE first_name = v_name;

            IF v_contact_id IS NULL THEN
                INSERT INTO phonebook (first_name) VALUES (v_name)
                RETURNING id INTO v_contact_id;
            END IF;

            IF NOT EXISTS (SELECT 1 FROM phones WHERE contact_id = v_contact_id AND phone = v_phone) THEN
                INSERT INTO phones (contact_id, phone, type) VALUES (v_contact_id, v_phone, 'mobile');
            END IF;
        ELSE
            invalid_records := array_append(invalid_records, ARRAY[v_name, v_phone]);
        END IF;
    END LOOP;

    IF array_length(invalid_records, 1) > 0 THEN
        RAISE NOTICE 'Invalid records: %', invalid_records;
    END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE delete_contact(p_value VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phones WHERE phone = p_value) THEN
        DELETE FROM phonebook WHERE id = (
            SELECT contact_id FROM phones WHERE phone = p_value LIMIT 1
        );
    ELSE
        DELETE FROM phonebook WHERE first_name = p_value;
    END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone        VARCHAR,
    p_type         VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    v_contact_id INTEGER;
BEGIN
    SELECT id INTO v_contact_id FROM phonebook WHERE first_name = p_contact_name;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact "%" not found', p_contact_name;
    END IF;

    INSERT INTO phones (contact_id, phone, type) VALUES (v_contact_id, p_phone, p_type);
END;
$$;


CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name   VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    v_contact_id INTEGER;
    v_group_id   INTEGER;
BEGIN
    SELECT id INTO v_contact_id FROM phonebook WHERE first_name = p_contact_name;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact "%" not found', p_contact_name;
    END IF;

    SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;

    IF v_group_id IS NULL THEN
        INSERT INTO groups (name) VALUES (p_group_name) RETURNING id INTO v_group_id;
    END IF;

    UPDATE phonebook SET group_id = v_group_id WHERE id = v_contact_id;
END;
$$;


CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (
    id         INTEGER,
    first_name VARCHAR,
    email      VARCHAR,
    birthday   DATE,
    group_name VARCHAR,
    phone      VARCHAR,
    phone_type VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT
        pb.id,
        pb.first_name,
        pb.email,
        pb.birthday,
        g.name   AS group_name,
        ph.phone,
        ph.type  AS phone_type
    FROM phonebook pb
    LEFT JOIN groups g  ON pb.group_id = g.id
    LEFT JOIN phones ph ON ph.contact_id = pb.id
    WHERE
        pb.first_name ILIKE '%' || p_query || '%'
        OR pb.email   ILIKE '%' || p_query || '%'
        OR ph.phone   ILIKE '%' || p_query || '%';
END;
$$;


CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT)
RETURNS TABLE (
    id         INTEGER,
    first_name VARCHAR,
    email      VARCHAR,
    birthday   DATE,
    group_name VARCHAR,
    phone      VARCHAR,
    phone_type VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT
        pb.id,
        pb.first_name,
        pb.email,
        pb.birthday,
        g.name   AS group_name,
        ph.phone,
        ph.type  AS phone_type
    FROM phonebook pb
    LEFT JOIN groups g  ON pb.group_id = g.id
    LEFT JOIN phones ph ON ph.contact_id = pb.id
    ORDER BY pb.first_name
    LIMIT p_limit OFFSET p_offset;
END;
$$;