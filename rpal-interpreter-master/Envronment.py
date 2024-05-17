import logging

from ASTNode import ASTNode


class Environment:
    logger = logging.getLogger(__name__)

    def __init__(self, index):
        self.idx = index
        self.map_vars = {}
        self.parent = None

    def set_env_parameters(self, parent_env, key, val):
        self.map_vars[key] = val
        if isinstance(key, ASTNode) and isinstance(val, ASTNode):
            pass
            # print("setEnvParams: {} | {} | val: {}".format(key, key.name, val.name))
        else:
            # self.logger.info("setEnvParams: key: {} | val: {}".format(key, val.name))
            pass
        self.parent = parent_env
        # print(self.map_vars)
        # print("setting parent of environment: {} as env: {}".format(self.idx, parent_env.idx))

    def get_env_index(self):
        return self.idx

    def get_val(self, key):
        # self.logger.info("getVal: {} | {}".format(key, key.name))
        if key in self.map_vars.keys():
            val = self.map_vars[key]
            self.logger.info("found in cur env id {}".format(self.idx))
            if isinstance(val, ASTNode):
                self.logger.info("val: {}".format(val.val))
            return val
        else:
            self.logger.info("not found in cur env")
            return None
