from json import dumps, load


class JsonConfig:
    def __init__(self, file):
        """
        Json input arguments parser
        :param file: input file path to input file
        """
        # self.param = {'notify': None}
        self.value = {**load(open(file, "r"))['config']}

    def print_config(self):
        """
        Print input arguments
        """
        out_dump = dumps(self.value,
                         indent=4,
                         sort_keys=True)
        out_dump = out_dump.replace(',', '')
        out_dump = out_dump.replace('{', '').replace('}', '')
        out_dump = out_dump.replace('[', '').replace(']', '')
        print('Config loaded:\n{config}'.format(config=out_dump))


if __name__ == '__main__':
    conf = JsonConfig('./../config/example/config.json')
    conf.print_config()
