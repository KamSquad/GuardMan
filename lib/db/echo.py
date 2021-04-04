from sqlalchemy.orm.exc import NoResultFound

from lib.db import base as dbm
from lib import creds
from lib import crypt_pass


class EchoDB(dbm.DatabaseInstance):
    def check_user_token(self, token):
        """
        Check user token and return role info
        :param token:
        :return:
        """
        try:
            # get user id
            user_auth_res = self.session.query(dbm.UserAuth).filter_by(
                token=token).one()
            # get user role
            user_login_res = self.session.query(dbm.UserLogin).filter_by(
                user_id=user_auth_res.user_id).one()
            # get user role table
            user_role_res = self.session.query(dbm.UserRole).filter_by(
                role_id=user_login_res.role_id).one()
            # prepare db result
            user_role_res_dict = dbm.make_dict_result(user_role_res)
            return user_role_res_dict
        except NoResultFound:
            return None

    def check_user_exist(self, user_name):
        """
        Check user exist by its username
        :param user_name: target username
        :return:
        """
        try:
            user_id_res = self.session.query(dbm.UserLogin).filter_by(
                    username=user_name).one()
            # prepare db result
            user_id_res_dict = dbm.make_dict_result(user_id_res)
            return user_id_res_dict['user_id']
        except NoResultFound:
            return None

    def gen_and_save_user_salt(self, user_id):
        """
        Generate, save and return salt for user login-in
        :param user_id: target user id
        :return: str
        """
        res_salt = creds.generate_salt()
        new_salt_obj = dbm.UserSalt(user_id=user_id, value=res_salt)
        self.session.merge(new_salt_obj)
        self.session.commit()
        return res_salt

    def check_user_hash_pass(self, user_name, inp_hash_pass):
        """
        Check user hashed password
        :param user_name: target username
        :param inp_hash_pass: hashed password of target user
        :return:
        """
        user_id = self.check_user_exist(user_name)
        if user_id:
            pass_crypted_res = self.session.query(dbm.UserLogin).filter_by(
                user_id=user_id).one().password
            salt_res = self.session.query(dbm.UserSalt).filter_by(
                user_id=user_id).one().value
            # decrypt password
            pass_clear = crypt_pass.decrypt_password(pass_crypted_res)
            # generate password hash
            db_pass_hash = creds.gen_md5(pass_clear + salt_res)
            # remove salt
            if self.remove_salt(salt_res):
                # return equal bool
                return db_pass_hash == inp_hash_pass
            else:
                return None
        else:
            return None

    def remove_salt(self, inp_salt_str):
        try:
            salt_to_delete = self.session.query(dbm.UserSalt).filter_by(value=inp_salt_str).one()
            self.session.delete(salt_to_delete)
            self.session.commit()
            return True
        except NoResultFound:
            return False

    def gen_and_save_token(self, user_name):
        user_id = self.check_user_exist(user_name)
        if user_id:
            user_token = creds.gen_uid()
            user_token_obj = dbm.UserAuth(user_id=user_id,
                                          token=user_token)
            self.session.merge(user_token_obj)
            self.session.commit()
            return user_token
        else:
            return False
