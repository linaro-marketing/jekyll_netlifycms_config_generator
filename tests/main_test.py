from main import JekyllNetlifyCMSGen

testGenerator = JekyllNetlifyCMSGen("","netlifycms.config.yaml")

def test_open_config_file():
    assert testGenerator.open_config_file()
