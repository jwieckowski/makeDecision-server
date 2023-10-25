# Copyright (c) 2023 Jakub Więckowski

import numpy as np
import json
import pandas as pd

from .validator import validate_dimensions, validate_matrix, validate_types
from .errors import get_error_message

class Files():
    @staticmethod
    def __validate_input_data(locale, matrix, extension, criteria_types):
        """
            Validate the decision matrix and criteria types regarding the given data extension 

            Parameters
            ----------
                locale : string
                    User application language

                matrix : ndarray
                    Decision matrix formatted as numpy array, 2 dimensional for crisp data and 3 dimensional for fuzzy data 

                extension : string
                    Extension of data in decision matrix (crisp or fuzzy)
                
                criteria_types : ndarray
                    Criteria types formatted as numpy array, number of criteria types should be the same as the number of columns in decision matrix

            Raises
            -------
                ValueError Exception
                    If data is formatted badly or the data shapes is different, the exception is thrown
        """

        try:
            Validator.validate_matrix(locale, matrix, extension)
        except Exception as err:
            raise ValueError(err)

        try:
            Validator.validate_types(locale, criteria_types)
        except Exception as err:
            raise ValueError(err)

        try:
            Validator.validate_dimensions(locale, matrix, criteria_types)
        except Exception as err:
            raise ValueError(err)

    @staticmethod
    def read_matrix_from_file(locale, file, type, extension):
        """
            Process data from file and convert it to numpy array.
            Based on the type of file, the matrix is converted with different processing approach.

            Parameters
            ----------
                locale : string
                    User application language

                file : file (CSV, JSON, or XLSX)
                    Uploaded file, containing the decision matrix and criteria types

                type : string
                    File extension (csv, json, or xlsx)
                
                extension : string
                    Extension of data in decision matrix (crisp or fuzzy)

            Returns
            -------
                ndarray, ndarray
                    Decision matrix and vector of criteria types formatted as numpy array
        """

        def read_from_csv_crisp(file):
            """
                Process crisp data from CSV file and convert it to numpy array 

                Parameters
                ----------
                    file : CSV file
                        Uploaded CSV file, containing the decision matrix and criteria types 

                Raises
                ------
                    ValueError Exception
                        If data is formatted badly or the data shapes is different, the exception is thrown    
                
                Returns
                -------
                    ndarray, ndarray
                        Decision matrix and vector of criteria types formatted as numpy array
            """

            df = pd.read_csv(file, header=None)
            columns = [f'{i}' for i in df.columns]
            df.columns = columns
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
            df = df.dropna(axis=1, how='all')

            matrix, criteria_types = None, None
            try:
                matrix = df.iloc[0:-1].to_numpy().astype(float)            
                if any([any(np.isnan(m)) for m in matrix]):
                    raise ValueError(f'{get_error_message(locale, "crisp-matrix-not-numeric-error")}')

            except:
                raise ValueError(f'{get_error_message(locale, "crisp-matrix-not-numeric-error")}')
                

            try:
                criteria_types = df.iloc[-1].to_numpy().astype(int)
                if any(np.isnan(criteria_types)):
                    raise ValueError(f'{get_error_message(locale, "criteria-types-not-numeric-error")}')
            except:
                raise ValueError(f'{get_error_message(locale, "criteria-types-not-numeric-error")}')
                

            try:
                Files.__validate_input_data(locale, matrix, extension, criteria_types)
                return matrix, criteria_types
            except Exception as err:
                raise ValueError(err)
        
        def read_from_csv_fuzzy(file):
            """
                Process fuzzy data from CSV file and convert it to numpy array 

                Parameters
                ----------
                    file : CSV file
                        Uploaded CSV file, containing the decision matrix and criteria types 

                Raises
                ------
                    ValueError Exception
                        If data is formatted badly or the data shapes is different, the exception is thrown
                
                Returns
                -------
                    ndarray, ndarray
                        Decision matrix and vector of criteria types formatted as numpy array

            """

            df = pd.read_csv(file, header=None)
            columns = [f'{i}' for i in df.columns]
            df.columns = columns
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
            df = df.dropna(axis=1, how='all')

            matrix, criteria_types = None, None
            try:
                data = df.iloc[0:-1].to_numpy()
                matrix = []
                for row in range(data.shape[0]):
                    temp = []
                    for col in range(data.shape[1]):
                        items = data[row, col].split(' ')
                        items = [float(item) for item in items if item != ''] 
                        temp.append(items)
                    matrix.append(temp)             
                matrix = np.array(matrix, dtype='object')

                if any([any([len(mm) != 3 for mm in m]) for m in matrix]):
                    raise ValueError(f'{get_error_message(locale, "fuzzy-matrix-format-error")}')
                
            except:
                raise ValueError(f'{get_error_message(locale, "fuzzy-matrix-format-error")}')

            try:
                criteria_types = df.iloc[-1].to_numpy().astype(int)
                if any(np.isnan(criteria_types)):
                    raise ValueError(f'{get_error_message(locale, "criteria-types-not-numeric-error")}')
            except:
                raise ValueError(f'{get_error_message(locale, "criteria-types-not-numeric-error")}')
                
            try:
                Files.__validate_input_data(locale, matrix, extension, criteria_types)
                return matrix, criteria_types
            except Exception as err:
                raise ValueError(err)

        def read_from_xlsx_crisp(file):
            """
                Process crisp data from XLSX file and convert it to numpy array 

                Parameters
                ----------
                    file : XLSX file
                        Uploaded XLSX file, containing the decision matrix and criteria types 

                Raises
                ------
                    ValueError Exception
                        If data is formatted badly or the data shapes is different, the exception is thrown    
                
                Returns
                -------
                    ndarray, ndarray
                        Decision matrix and vector of criteria types formatted as numpy array
            """

            df = pd.read_excel(file, header=None)
            columns = [f'{i}' for i in df.columns]
            df.columns = columns
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
            df = df.dropna(axis=1, how='all')
            
            matrix, criteria_types = None, None
            try:
                matrix = df.iloc[0:-2].to_numpy().astype(float)            
                if any([any(np.isnan(m)) for m in matrix]):
                    raise ValueError(f'{get_error_message(locale, "crisp-matrix-not-numeric-error")}')
                
            except:
                raise ValueError(f'{get_error_message(locale, "crisp-matrix-not-numeric-error")}')

            try:
                criteria_types = df.iloc[-1].to_numpy().astype(float)
                if any(np.isnan(criteria_types)):
                    raise ValueError(f'{get_error_message(locale, "criteria-types-not-numeric-error")}')
                    
            except:
                raise ValueError(f'{get_error_message(locale, "criteria-types-not-numeric-error")}')

            try:
                Files.__validate_input_data(locale, matrix, extension, criteria_types)
                return matrix, criteria_types
            except Exception as err:
                raise ValueError(err)
        
        def read_from_xlsx_fuzzy(file):
            """
                Process fuzzy data from XLSX file and convert it to numpy array 

                Parameters
                ----------
                    file : XLSX file
                        Uploaded XLSX file, containing the decision matrix and criteria types 

                Raises
                ------
                    ValueError Exception
                        If data is formatted badly or the data shapes is different, the exception is thrown    
                
                Returns
                -------
                    ndarray, ndarray
                        Decision matrix and vector of criteria types formatted as numpy array
            """

            df = pd.read_excel(file, header=None)
            columns = [f'{i}' for i in df.columns]
            df.columns = columns
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
            df = df.dropna(axis=1, how='all')
            
            matrix, criteria_types = None, None
            try:
                data = df.iloc[0:-2].to_numpy()
                matrix = []
                for row in range(data.shape[0]):
                    temp = []
                    for col in range(data.shape[1]):
                        items = data[row, col].split(' ')
                        items = [float(item) for item in items if item != ''] 
                        temp.append(items)
                    matrix.append(temp)             
                matrix = np.array(matrix, dtype='object')

                if any([any([len(mm) != 3 for mm in m]) for m in matrix]):
                    raise ValueError(f'{get_error_message(locale, "fuzzy-matrix-format-error")}')

            except:
                raise ValueError(f'{get_error_message(locale, "fuzzy-matrix-format-error")}')

            try:
                criteria_types = df.iloc[-1].to_numpy().astype(float)
                if any(np.isnan(criteria_types)):
                    raise ValueError(f'{get_error_message(locale, "criteria-types-not-numeric-error")}')
            except:
                raise ValueError(f'{get_error_message(locale, "criteria-types-not-numeric-error")}')

            try:
                Files.__validate_input_data(locale, matrix, extension, criteria_types)
                return matrix, criteria_types
            except Exception as err:
                raise ValueError(err)

        def read_from_json_crisp(file):
            """
                Process crisp data from JSON file and convert it to numpy array 

                Parameters
                ----------
                    file : JSON file
                        Uploaded JSON file, containing the decision matrix and criteria types 

                Raises
                ------
                    ValueError Exception
                        If data is formatted badly or the data shapes is different, the exception is thrown    
                                    
                Returns
                -------
                    ndarray, ndarray
                        Decision matrix and vector of criteria types formatted as numpy array
            """

            file.seek(0)
            data = json.load(file)
            
            if not all(item in list(data.keys()) for item in ['matrix', 'criteriaTypes']):
                raise ValueError(f'{get_error_message(locale, "not-all-keys-json-error")}')

            matrix = data['matrix']
            try:
                matrix = np.array(matrix)
            except:
                raise ValueError(f'{get_error_message(locale, "matrix-array-convert-error")}')
            
            criteria_types = data['criteriaTypes']
            try:
                criteria_types = np.array(criteria_types)
            except:
                raise ValueError(f'{get_error_message(locale, "criteria-array-convert-error")}')

            try:
                Files.__validate_input_data(locale, matrix, extension, criteria_types)
                return matrix, criteria_types
            except Exception as err:
                raise ValueError(err)
        
        def read_from_json_fuzzy(file):
            """
                Process fuzzy data from JSON file and convert it to numpy array 

                Parameters
                ----------
                    file : JSON file
                        Uploaded JSON file, containing the decision matrix and criteria types 

                Raises
                ------
                    ValueError Exception
                        If data is formatted badly or the data shapes is different, the exception is thrown    
                
                Returns
                -------
                    ndarray, ndarray
                        Decision matrix and vector of criteria types formatted as numpy array
            """

            file.seek(0)
            data = json.load(file)
            
            if not all(item in list(data.keys()) for item in ['matrix', 'criteriaTypes']):
                raise ValueError(f'{get_error_message(locale, "not-all-keys-json-error")}')

            matrix = data['matrix']
            try:
                matrix = np.array(matrix)
            except:
                raise ValueError(f'{get_error_message(locale, "matrix-array-convert-error")}')
            
            criteria_types = data['criteriaTypes']
            try:
                criteria_types = np.array(criteria_types)
            except:
                raise ValueError(f'{get_error_message(locale, "criteria-array-convert-error")}')

            try:
                Files.__validate_input_data(locale, matrix, extension, criteria_types)
                return matrix, criteria_types
            except Exception as err:
                raise ValueError(err)

        if extension == 'crisp':
            if type == 'csv':
                matrix, criteria_types = read_from_csv_crisp(file)
                return matrix, criteria_types
            
            elif type == 'xlsx':
                matrix, criteria_types = read_from_xlsx_crisp(file)
                return matrix, criteria_types

            elif type == 'json':
                matrix, criteria_types = read_from_json_crisp(file)
                return matrix, criteria_types
            
            raise ValueError(f'{get_error_message(locale, "file-type-error")}')

        elif extension == 'fuzzy':
            if type == 'csv':
                matrix, criteria_types = read_from_csv_fuzzy(file)
                return matrix, criteria_types
            
            elif type == 'xlsx':
                matrix, criteria_types = read_from_xlsx_fuzzy(file)
                return matrix, criteria_types

            elif type == 'json':
                matrix, criteria_types = read_from_json_fuzzy(file)
                return matrix, criteria_types
                
            raise ValueError(f'{get_error_message(locale, "file-type-error")}')
        else:
            raise ValueError(f'{extension} {get_error_message(locale, "data-extension-error")}')
            