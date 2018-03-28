"""[summary]
"""
import pandas as pd
import wx

from ui import Ui
from service import Service


class Application:
    """[summary]
    """

    def __init__(self, name, data_dir, file_name, history):
        """[summary]

        Arguments:
            name {[type]} -- [description]
            data_dir {[type]} -- [description]
        """
        self.name = name
        self.data_base_directory = data_dir
        self.country_file = file_name
        self.sales_history_file = history
        # updated by __register_service  contains service names
        self.country_and_zone_data = {}
        # updated by __instantiate_service()contains list of service instances
        self.service_name_collection = {}
        self.services_collection = []
        self.sales_history = []
        self.available_serice_price_options = []

        self.__initialise_volotile()

        self.country_and_zone_data = self.__import_country_and_zone_data()
        self.sales_history = self.__import_sales_history()

        self.__register_service(
            'Economy Letter', 'Economy Letters Price Guide ($).csv')
        self.__register_service(
            'Economy Parcel by Air',
            'Economy Parcel Price Guide_by Air ($).csv')
        self.__register_service(
            'Economy Parcel by Sea',
            'Economy Parcel Price Guide_by Sea ($).csv')
        self.__register_service(
            'Express Letter', 'Express Letter Price Guide ($).csv')
        self.__register_service(
            'Express Parcel', 'Express Parcel Price Guide ($).csv')
        self.__register_service(
            'Standard Parcel', 'Standard Parcel Price Guide ($).csv')

        self.__instantiate_service()

        POSTAGE_SERVICE_UI = wx.App()
        FRAME = Ui(self.name, parent=None, id=-1, app=self)

        FRAME.Centre()
        FRAME.Show()
        POSTAGE_SERVICE_UI.MainLoop()

    def __initialise_volotile(self):

        self.country = ''
        self.weight = 0
        self.single_row = False
        self.available_serice_price_options = []
        self.invoice = []

    def get_sales_history_by_sales_number(self, sales_number):
        return_iterable = []
        if self.sales_history.loc[sales_number].values.ndim > 1:
            self.single_row = False
            for each_value in self.sales_history.loc[sales_number].values:
                return_iterable.append(each_value)
        else:
            self.single_row = True
            return_iterable = self.sales_history.loc[sales_number].values
        return return_iterable

    def __import_sales_history(self):
        """

        """
        try:
            return_frame = pd.read_csv(
                self.data_base_directory + self.sales_history_file, header=0,
                index_col=0, squeeze=True)
        except FileNotFoundError:
            print('File "{}" could not be found. Please, make sure it exists and you have rights to read it.\nProgram will terminate now.'.format(  # pylint: disable=C0301
                self.sales_history_file))
            exit(404)
        return return_frame

    def __enter__(self):
        """[summary]
        Returns:
            [type] -- [description]
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """[summary]
        Arguments:
            exc_type {[type]} -- [description]
            exc_val {[type]} -- [description]
            exc_tb {[type]} -- [description]
        """

        pass

    def __register_service(self, service_name, data_file):
        """[summary]

        Arguments:
            name {[type]} -- [description]
            file {[type]} -- [description]
        """

        self.service_name_collection[service_name] = data_file

    def __instantiate_service(self):
        """[summary]
        """

        for each_service in self.service_name_collection:
            service = Service(
                each_service, self.data_base_directory,
                self.service_name_collection.get(each_service))
            service.application = self
            self.services_collection.append(service)

    def get_available_serice_price_options(self):
        """[summary]
        """
        l = []
        for each_service in self.services_collection:
            nm = each_service.get_service_name()
            pr = each_service.get_service_price(self.country, self.weight)
            if pr:
                l.append([nm, pr])
                # print('{} --> {}'.format(nm,pr))
        return l

    def __import_country_and_zone_data(self):
        """[summary]

        """

        return_dictionary = {}
        try:
            with open(self.data_base_directory + self.country_file) as csv_file:
                next(csv_file)
                for each_line in csv_file.readlines():
                    each_line = each_line.split(',')
                    return_dictionary[each_line[0]] = each_line[1]
        except FileNotFoundError:
            print('File "{}" could not be found. Please, make sure it exists and you have rights to read it.\nProgram will terminate now.'.format(  # pylint: disable=C0301
                self.country_file))
            exit(404)
        return return_dictionary