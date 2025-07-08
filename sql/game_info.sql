-- name: get_game_info
SELECT game_root_path, server_path, server_name, server_version,
       fika_server_path, fika_server_name, fika_server_version
FROM game_info LIMIT 1;

-- name: count_game_info
SELECT COUNT(*) FROM game_info;

-- name: insert_game_info_key
INSERT INTO game_info ({key}) VALUES (?);

-- name: update_game_info_key
UPDATE game_info SET {key} = ?;