from dataclasses import dataclass
import os


@dataclass()
class Profile:

    """
    This class represents HB online profile. Profiles exist so that the same HB online instance can support multiple
    users, each one has his own input/output folders and HB configuration profile.
    """

    name: str
    hb_profile: str
    stream_input_folder: str
    stream_output_folder: str
    hb_input_folder: str
    hb_output_folder: str
    copy: bool
    max_size_to_load: int

    @staticmethod
    def make(config: dict):
        """
        Receives config dict and generates Profile objects.
        :param config:
        :return:
        """
        for name, profile_config in config['profiles'].items():
            yield Profile(name=name,
                          hb_profile=profile_config['hb_profile'],
                          stream_input_folder=profile_config['input'],
                          stream_output_folder=profile_config['output'],
                          hb_input_folder=os.path.join(config['hb_path'], name, 'in'),
                          hb_output_folder=os.path.join(config['hb_path'], name, 'out'),
                          copy=profile_config.get('copy_files', False),
                          max_size_to_load=profile_config.get('max_size_to_load_in_gb', 0) * pow(1024, 3))
