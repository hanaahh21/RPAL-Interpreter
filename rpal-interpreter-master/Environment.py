import logging

from ASTNode import ASTNode


class Environment:
    # Logger for logging environment activities
    logger = logging.getLogger(__name__)

    def __init__(self, index):
        # Initialize the environment with an index and an empty map for variables
        self.idx = index
        self.map_vars = {}
        self.parent = None # Parent environment

    def set_env_parameters(self, parent_env, key, val):
        # Set the environment parameters
        self.map_vars[key] = val # Store the key-value pair in the environment's map

        # Check if key and val are instances of ASTNode
        if isinstance(key, ASTNode) and isinstance(val, ASTNode):
            pass  # If both are ASTNode instances, do nothing (placeholder for future code)
            # print("setEnvParams: {} | {} | val: {}".format(key, key.name, val.name))
        else: 
            # self.logger.info("setEnvParams: key: {} | val: {}".format(key, val.name))
            pass  # Placeholder for logging or other actions if key and val are not ASTNode instances
        self.parent = parent_env  # Set the parent environment
        # print(self.map_vars)
        # print("setting parent of environment: {} as env: {}".format(self.idx, parent_env.idx))

    def get_env_index(self):
        # Return the index of the environment
        return self.idx

    def get_val(self, key):
        # self.logger.info("getVal: {} | {}".format(key, key.name))
        # Get the value associated with the key in the environment
        if key in self.map_vars.keys():
            val = self.map_vars[key]  # Retrieve the value from the environment's map
            self.logger.info("found in cur env id {}".format(self.idx))  # Log that the key was found in the current environment
            if isinstance(val, ASTNode):
                self.logger.info("val: {}".format(val.val))  # Log the value if it's an ASTNode
            return val
        else:
            self.logger.info("not found in cur env")  # Log that the key was not found in the current environment
            return None
