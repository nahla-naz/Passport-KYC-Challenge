import configparser



''' Run this file to create a new CONFIG.INI file'''



class Configuration():


    ''' Class for writing to Config file '''

    def write_config():

        # Create a configparser object
        config = configparser.ConfigParser()

        config['settings'] = {
            'Area_threshold': '80000',
            'ip': '127.0.0.1',
            'port':'8000'
        }

        # Write to file
        with open('CONFIG.ini', 'w') as configfile:
            config.write(configfile)

        print("\nConfig file saved successfully.")


if __name__ == "__main__":

    Config = Configuration()

    Config.write_config()
    

   