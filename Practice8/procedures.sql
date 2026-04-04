CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE first_name = p_name) THEN
        UPDATE phonebook SET phone = p_phone WHERE first_name = p_name;
    ELSE
        INSERT INTO phonebook (first_name, phone) VALUES (p_name, p_phone);
    END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE bulk_insert_contacts(p_data VARCHAR[][])
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
    v_name VARCHAR;
    v_phone VARCHAR;
    invalid_records VARCHAR[][] := ARRAY[]::VARCHAR[][];
BEGIN
    FOR i IN 1..array_length(p_data, 1) LOOP
        v_name := p_data[i][1];
        v_phone := p_data[i][2];

        IF v_phone ~ '^\+?[0-9]{7,15}$' THEN
            IF EXISTS (SELECT 1 FROM phonebook WHERE first_name = v_name) THEN
                UPDATE phonebook SET phone = v_phone WHERE first_name = v_name;
            ELSE
                INSERT INTO phonebook (first_name, phone) VALUES (v_name, v_phone);
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
    IF EXISTS (SELECT 1 FROM phonebook WHERE phone = p_value) THEN
        DELETE FROM phonebook WHERE phone = p_value;
    ELSE
        DELETE FROM phonebook WHERE first_name = p_value;
    END IF;
END;
$$;