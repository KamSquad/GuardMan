check_user_exist_cmd = "SELECT check_user_exist($1);"
gen_and_save_user_salt_cmd = "CALL gen_and_save_user_salt($1, $2);"
check_user_hash_pass_cmd = "SELECT check_user_hash_pass($1);"
gen_and_save_token_cmd = "CALL gen_and_save_token($1, $2);"
