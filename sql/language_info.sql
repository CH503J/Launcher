-- name: get_language_info
INSERT INTO language_info (
                item_id, name, short_name, description,
                fail_message, success_message,
                accept_player_message, decline_player_message, complete_player_message,
                other_value
            ) VALUES (
                :item_id, :name, :short_name, :description,
                :fail_message, :success_message,
                :accept_player_message, :decline_player_message, :complete_player_message,
                :other_value
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