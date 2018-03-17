"""[summary]

Returns:
    [type] -- [description]
"""


import re
import pandas as pd


class Application():
    """[summary]
    """

    def __init__(self, name, data_dir):
        """[summary]

        Arguments:
            name {[type]} -- [description]
            data_dir {[type]} -- [description]
        """

        self.name = name
        self.services_collection = []
        self.service_name_collection = {}
        self.data_base_directory = data_dir
        self.country = ''
        self.weight = 0

    def register_service(self, name, file):
        """[summary]

        Arguments:
            name {[type]} -- [description]
            file {[type]} -- [description]
        """

        self.service_name_collection[name] = file

    def instantiate_service(self):
        """[summary]
        """

        for each_service in self.service_name_collection:
            self.services_collection.append(Service(
                each_service, self.data_base_directory,
                self.service_name_collection.get(each_service)))

    def get_available_options(self):
        """[summary]
        """

        for each_service in self.services_collection:
            print('{} --> {}'.format(each_service.get_service_name(),
                                     each_service.get_service_price(self.country, self.weight)))


class Service:
    """[summary]

    Returns:
        [type] -- [description]
    """

    def __init__(self, name, data_dir, data_file):
        """[summary]

        Arguments:
            name {[type]} -- [description]
            data_dir {[type]} -- [description]
            data_file {[type]} -- [description]
        """

        self.name = name
        self.data_dir = data_dir
        self.data_file = data_file
        self.country_file = 'Countries and Zones.csv'
        self.zone_weight_data = {}
        self.country_and_zone_data = {}

        self.country_and_zone_data = self.import_country_and_zone_data()
        self.zone_weight_data = self.import_data_from_csv_file()

    def import_data_from_csv_file(self):
        """[summary]

        Returns:
            [type] -- [description]
        """

        return_dictionary = {}
        try:
            return_dictionary = pd.read_csv(
                self.data_dir + self.data_file, header=0, index_col=0,
                squeeze=True).to_dict()
        except FileNotFoundError:
            print('File "{}" could not be found. Please, make sure it exists and you have rights to read it.\nProgram will terminate now.'.format( # pylint: disable=C0301
                self.data_file))
            exit(404)
        return return_dictionary

    def import_country_and_zone_data(self):
        """[summary]

        Returns:
            [type] -- [description]
        """

        return_dictionary = {}
        try:
            with open(self.data_dir + self.country_file) as csv_file:
                next(csv_file)
                for each_line in csv_file.readlines():
                    each_line = each_line.split(',')
                    return_dictionary[each_line[0]] = each_line[1]
        except FileNotFoundError:
            print('File "{}" could not be found. Please, make sure it exists and you have rights to read it.\nProgram will terminate now.'.format( # pylint: disable=C0301
                self.country_file))
            exit(404)
        return return_dictionary

    def get_zone_label(self, zone):
        """[summary]

        Arguments:
            zone {[type]} -- [description]

        Returns:
            [type] -- [description]
        """

        zone_pattern = re.compile(r'(' + str(zone) + ')')
        zone_label = None

        for i in self.zone_weight_data.keys():
            matches = re.search(zone_pattern, i)
            if matches is not None:
                zone_label = i
        return zone_label

    def get_weight_label(self, weight):
        """[summary]

        Arguments:
            dictionary {[type]} -- [description]
            weight {[type]} -- [description]

        Returns:
            [type] -- [description]
        """

        i = None
        for i in self.zone_weight_data.values():
            key_list = list(i.keys())

        weight_number_pattern = re.compile(r'\d{1,3}')
        weigh_unit_pattern = re.compile(r'\d{1,3}(kg)')
        j = 0
        while j < len(key_list):
            number_matches = re.findall(weight_number_pattern, key_list[j])
            unit_matches = re.findall(weigh_unit_pattern, key_list[j])

            # if found 'kg after the number prepare to convert to gr,
            # otherwise make sure it stays in gr
            if unit_matches:
                unit_multiplier = 1000
            else:
                unit_multiplier = 1

            if number_matches:  # if numbers are found in the label
                # if only one number id found like in 'up to 500gr' or 'up to 1 kg'
                if len(number_matches) == 1:
                    if float(weight) <= float(
                            float(unit_multiplier) * float(number_matches[0])):
                        return key_list[j]
                if len(number_matches) == 2:
                    w_1 = unit_multiplier * float(number_matches[0])
                    w_2 = unit_multiplier * float(number_matches[1])
                    if (float(weight) >= float(w_1)) and (float(weight) <= float(w_2)):
                        return key_list[j]
            j += 1
        return None

    def get_service_price(self, country, weight):
        """[summary]

        Arguments:
            country {[type]} -- [description]
            weight {[type]} -- [description]

        Returns:
            [type] -- [description]
        """

        zone = self.get_zone_info_from_country(
            self.country_and_zone_data, country)
        try:
            zone_label = self.get_zone_label(zone)
            weight_label = self.get_weight_label(weight)
            return float(self.zone_weight_data.get(zone_label).get(
                str(weight_label)))
        except(ValueError, AttributeError, TypeError):
            return None

    def is_servicable_country(self, dictionary, country_name): # pylint: disable=R0201
        """[summary]

        Arguments:
            dictionary {[type]} -- [description]
            country_name {[type]} -- [description]

        Returns:
            [type] -- [description]
        """

        if country_name in dictionary:
            return True
        return False

    def get_zone_info_from_country(self, dictionary, country_name):# pylint: disable=R1710
        """[summary]

        Arguments:
            dictionary {[type]} -- [description]
            country_name {[type]} -- [description]

        Returns:
            [type] -- [description]
        """

        if self.is_servicable_country(dictionary, country_name):
            result = dictionary.get(country_name)
            number_pattern = re.compile(r'\d{1}')
            matches = re.findall(number_pattern, result)
            if matches:
                return matches[0]
        else:
            return None

    def get_service_name(self):
        """[summary]
        """

        pass

    def get_all_countries(self):
        """[summary]

        Returns:
            [type] -- [description]
        """
        list_of_countries = []
        for all_items in self.country_and_zone_data:
            list_of_countries.append(all_items)
        return list_of_countries


POSTAGE_SERVICE = Application('Postage Service', './/data//')
POSTAGE_SERVICE.country = 'New Zealand'
POSTAGE_SERVICE.weight = 150

POSTAGE_SERVICE.register_service(
    'Economy Letter', 'Economy Letters Price Guide ($).csv')
POSTAGE_SERVICE.register_service(
    'Economy Parcel by Air', 'Economy Parcel Price Guide_by Air ($).csv')
POSTAGE_SERVICE.register_service(
    'Economy Parcel by Sea', 'Economy Parcel Price Guide_by Sea ($).csv')
POSTAGE_SERVICE.register_service(
    'Express Letter', 'Express Letter Price Guide ($).csv')
POSTAGE_SERVICE.register_service(
    'Express Parcel', 'Express Parcel Price Guide ($).csv')
POSTAGE_SERVICE.register_service(
    'Standard Parcel', 'Standard Parcel Price Guide ($).csv')

POSTAGE_SERVICE.instantiate_service()

# pprint(POSTAGE_SERVICE.service_name_collection)
# pprint(POSTAGE_SERVICE.services_collection)


if POSTAGE_SERVICE.services_collection:
    LIST_OF_ALL_COUNTRIES = POSTAGE_SERVICE.services_collection[0].get_all_countries()
    for  every_item in LIST_OF_ALL_COUNTRIES:
        print(every_item)



POSTAGE_SERVICE.get_available_options()