-- name: get_language_info
INSERT INTO language_info (
                item_id,
                name,
                short_name,
                description,
                fail_message,
                success_message,
                accept_player_message,
                decline_player_message,
                complete_player_message,
                other_value,
                type
            ) VALUES (
                :item_id,
                :name,
                :short_name,
                :description,
                :fail_message,
                :success_message,
                :accept_player_message,
                :decline_player_message,
                :complete_player_message,
                :other_value,
                :type
            )

-- name: delete_language_info
DELETE FROM language_info

-- name: search_data
SELECT *
FROM language_info
WHERE
    item_id LIKE '%' || ? || '%' OR
    name LIKE '%' || ? || '%' OR
    short_name LIKE '%' || ? || '%' OR
    description LIKE '%' || ? || '%' OR
    fail_message LIKE '%' || ? || '%' OR
    success_message LIKE '%' || ? || '%' OR
    accept_player_message LIKE '%' || ? || '%' OR
    decline_player_message LIKE '%' || ? || '%' OR
    complete_player_message LIKE '%' || ? || '%' OR
    other_value LIKE '%' || ? || '%';

-- name: search_data_by_field
SELECT *
FROM language_info
WHERE {key} LIKE ?



-- name: search_data_by_type
SELECT *
FROM language_info
WHERE (
    item_id LIKE :kw OR
    name LIKE :kw OR
    short_name LIKE :kw OR
    description LIKE :kw OR
    fail_message LIKE :kw OR
    success_message LIKE :kw OR
    accept_player_message LIKE :kw OR
    decline_player_message LIKE :kw OR
    complete_player_message LIKE :kw OR
    other_value LIKE :kw
) AND type = :type;

-- name: search_data_all
SELECT *
FROM language_info
WHERE
    item_id LIKE :kw OR
    name LIKE :kw OR
    short_name LIKE :kw OR
    description LIKE :kw OR
    fail_message LIKE :kw OR
    success_message LIKE :kw OR
    accept_player_message LIKE :kw OR
    decline_player_message LIKE :kw OR
    complete_player_message LIKE :kw OR
    other_value LIKE :kw;