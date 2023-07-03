import pathlib
import re


from neo4j import GraphDatabase, basic_auth

def read_conf_file(path):
    """
    reading the configuration file
    It must be assembled in the following manner: key = configuration value
    It will return a dictionary in the following format: {workers : 3, limit : 100}
    """
    res = {}

    with open(path) as file:
        lines = file.readlines()
        for line in lines:
            if '=' in line:
                prop = line.strip()
                l_str = prop.split('=')
                if len(l_str) >2:
                    l_str[1] = "=".join(l_str[1:])

                res[l_str[0].strip()] = l_str[1].strip()

    return res


class DatabaseAccessManager:
    _driver = None

    def __init__(self, conf_file_path: str = None):
        self.conf_file_path = conf_file_path

    @property
    def driver(self):
        if self._driver is None:
            raise Exception("Driver not initialized, call establish_connection first")
        else:
            return self._driver

    def establish_connection(self,path = None, uri: str = None, user: str = None, password: str = None):
        if uri is None or user is None or password is None:
            uri, user, password = self._get_credentials_from_file(path=path)
        self._driver = GraphDatabase.driver(uri, auth=basic_auth(user, password))

    def establish_connection_from_file(self, path):
        uri, user, password = self._get_credentials_from_file(path)
        self.establish_connection(path,uri, user, password)

    def connect(self):
        self.establish_connection()
        return self.driver

    @staticmethod
    def write_config_file(file_path: str, uri: str = None, user: str = None, password: str = None):
        uri_bool = False
        user_bool = False
        pass_bool = False
        lines = []
        if pathlib.Path(file_path).exists():
            with open(file_path, "r") as f:
                lines = f.readlines()

        with open(file_path, "w") as f:
            if lines:
                for line in lines:
                    if re.match("^uri=", line):
                        uri_bool = True
                        f.write("uri=" + uri + "\n")
                    elif re.match("^user=", line):
                        user_bool = True
                        f.write("user=" + user + "\n")
                    elif re.match("^password=", line):
                        pass_bool = True
                        f.write("password=" + password + "\n")
                    else:
                        f.write(line)

            if not uri_bool:
                f.write("uri=" + uri + "\n")

            if not user_bool:
                f.write("user=" + user + "\n")

            if not pass_bool:
                f.write("password=" + password + "\n")

    def close(self):
        self._driver.close()

    def run_query(self, query, params=None):
        with self._driver.session() as session:
            result = session.run(query, params)
        return result

    def _get_credentials_from_file(self, path=None):
        if path is not None:
            self.conf_file_path = path
        if not pathlib.Path(self.conf_file_path).exists():
            raise Exception("Database credentials file not found")
        else:
            uri, user, password = self.read_database_credentials()
            return uri, user, password


    def read_database_credentials(self):

        if pathlib.Path(self.conf_file_path).exists():
            configs = read_conf_file(self.conf_file_path)

            if "uri" in configs.keys() and "user" in configs.keys() and "password" in configs.keys():
                uri = configs["uri"]
                user = configs["user"]
                password = configs["password"]

                return uri, user, password

        else:

            raise Exception("Please insert the required database information using set_database_information function")


def read_config_file(file_path):
    if pathlib.Path(file_path).exists():
        configs = read_conf_file(file_path)

        if "uri" in configs.keys() and "user" in configs.keys() and "password" in configs.keys():
            uri = configs["uri"]
            user = configs["user"]
            password = configs["password"]

            return uri, user, password

    else:

        raise Exception("Please insert the required database information using set_database_information function")




