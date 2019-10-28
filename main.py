import argparse
import yaml

class JekyllNetlifyCMSGen:
    def __init__(self, site_path, config_file_name):
        # Path to Jekyll Site
        self.jekyll_site_path = site_path
        # Name of the config file to use to generate the netlfiycms config
        self.config_file_name = config_file_name

        self.config_file_path = "{}/{}".format(
            self.jekyll_site_path, self.config_file_name)

        # Load the config
        self.generator_config = self.open_config_file()

        print(self.jekyll_site_path)
        print(self.config_file_path)

        print(self.generator_config["layouts"])
        # self.main()

    def main(self):
        """ Main entry method """
        pass

    def open_config_file(self):
        with open(self.config_file_path) as config_file:
            return yaml.load(config_file, Loader=yaml.FullLoader)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
    description="Generate a NetlifyCMS config file based on a Jekyll Site")
    parser.add_argument('-d', '--directory', required=True, dest="site_path",
                    nargs='?', default=None, help='The path to a Jekyll site.')
    parser.add_argument('-c', '--config', required=False, dest="config_file_name", nargs='?',
                    default="netlifycms.config.yml", help='The name of the generator config file.')
    args = parser.parse_args()
    site_path = args.site_path
    config_file_name = args.config_file_name

    generator = JekyllNetlifyCMSGen(site_path, config_file_name)
