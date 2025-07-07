-- name: get_app_info
SELECT app_name, version, author, github_link, example_path
FROM about_info LIMIT 1;