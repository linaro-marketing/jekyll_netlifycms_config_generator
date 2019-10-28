import argparse
import yaml


class JekyllNetlifyCMSGen:
    def __init__(self, site_path, config_file_name):
        # Verbosity boolean - toggles the output of fine grained messages
        self._verbose = True
        # Path to Jekyll Site
        self.jekyll_site_path = site_path
        # Name of the config file to use to generate the netlfiycms config
        self.config_file_name = config_file_name

        self.config_file_path = "{}/{}".format(
            self.jekyll_site_path, self.config_file_name)

        # Load the config
        self.generator_config = self.load_yaml_file(self.config_file_path)

        print(self.generator_config["layouts"])
        self.generate()

    def generate(self):
        """ Generate the netlfiycms config file """
        # Add the initial cms_settings
        self.netlifycms_config = self.generator_config["cms_settings"]

    def get_cms_config_from_yaml(self, yaml_object):
        """
        Main logic method - process a yaml block i.e a Jekyll data file
        or a block of frontmatter and return the corresponding
        netlifycms config.yml section
        """
        print("YAML object output")
        for item in yaml_object:
            print(item)

    def process_data_files_collection(self, collection):
        """
        Process a Jekyll _data files collection
        Returns a dictionary describing the YAML for this collection
        """
        base_yaml_settings = collection["collection_settings"]
        data_files_yaml_array = []
        for data_file in collection["files"]:
            data_file_full_path = "{}/{}".format(
                self.jekyll_site_path, data_file["file"])
            data_file_yaml = self.load_yaml_file(data_file_full_path)
            data_file_cms_config = self.get_cms_config_from_yaml(
                data_file_yaml)
            data_file_generated_yaml = data_file
            data_file_generated_yaml["fields"] = data_file_cms_config
            data_files_yaml_array.append(data_file_generated_yaml)
        cms_config_yaml = base_yaml_settings
        cms_config_yaml["files"] = data_files_yaml_array

        return cms_config_yaml

    def process_directory_collection(self, collection):
        """
        Process a directory collection e.g _pages
        Returns a dictionary describing the YAML for this netlifycms collection
        """
        base_yaml_settings = collection["collection_settings"]
        layout_path = "{}/{}/{}".format(
            self.jekyll_site_path, self.generator_template_dir, collection["layout"])
        layout_yaml = self.load_yaml_file(layout_path)
        cms_config_yaml = base_yaml_settings
        cms_config_yaml["fields"] = self.get_cms_config_from_yaml(layout_yaml)

        return cms_config_yaml

    def parse_cms_collections(self):
        """
        Loops over the defined cms collections and adds config yaml
        Returns a yaml object
        """
        cms_collections_list = []
        for collection in self.generator_config["cms_collections"]:
            if collection["type"] == "directory":
                yaml_obj = self.process_directory_collection(collection)
            elif collection["type"] == "data_files":
                yaml_obj = self.process_data_files_collection(collection)
            else:
                if self._verbose:
                    print("")
                pass
            cms_collections_list.append(yaml_obj)

    def load_yaml_file(self, file_path):
        """ Loads a yaml file """
        with open(file_path) as yaml_file:
            return yaml.load(yaml_file, Loader=yaml.FullLoader)


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
