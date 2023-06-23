import numpy as np
import json
import pandas as pd


from .validator import Validator
class Files():
    @staticmethod
    def __validate_input_data(matrix, extension, criteria_types):
        """
            Validate the decision matrix and criteria types regarding the given data extension 

            Parameters
            ----------
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
            Validator.validate_matrix(matrix, extension)
        except Exception as err:
            raise ValueError(err)

        try:
            Validator.validate_types(criteria_types)
        except Exception as err:
            raise ValueError(err)

        try:
            Validator.validate_dimensions(matrix, criteria_types)
        except Exception as err:
            raise ValueError(err)

    @staticmethod
    def read_matrix_from_file(file, type, extension):
        """
            Process data from file and convert it to numpy array.
            Based on the type of file, the matrix is converted with different processing approach.

            Parameters
            ----------
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


        # TODO add checking if all rows have the same length
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
                    raise ValueError('Matrix contains elements that are not a number')
                    
            except:
                raise ValueError('Matrix contains elements that are not a number')
                

            try:
                criteria_types = df.iloc[-1].to_numpy().astype(int)
                if any(np.isnan(criteria_types)):
                    raise ValueError('Criteria types contains elements that are not a number')
            except:
                raise ValueError('Criteria types contains elements that are not a number')
                

            try:
                Files.__validate_input_data(matrix, extension, criteria_types)
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
                    raise ValueError('Matrix contains elements that are not a number')
            except:
                raise ValueError('Matrix contains elements that are not a number')

            try:
                criteria_types = df.iloc[-1].to_numpy().astype(int)
                if any(np.isnan(criteria_types)):
                    raise ValueError('Criteria types contains elements that are not a number')
            except:
                raise ValueError('Criteria types contains elements that are not a number')
                
            try:
                Files.__validate_input_data(matrix, extension, criteria_types)
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
                    raise ValueError('Matrix contains elements that are not a number')
            except:
                raise ValueError('Matrix contains elements that are not a number')

            try:
                criteria_types = df.iloc[-1].to_numpy().astype(float)
                if any(np.isnan(criteria_types)):
                    raise ValueError('Criteria types contains elements that are not a number')
            except:
                raise ValueError('Criteria types contains elements that are not a number')

            try:
                Files.__validate_input_data(matrix, extension, criteria_types)
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
                    raise ValueError('Matrix contains elements that are not a number')
            except:
                raise ValueError('Matrix contains elements that are not a number')

            try:
                criteria_types = df.iloc[-1].to_numpy().astype(float)
                if any(np.isnan(criteria_types)):
                    raise ValueError('Criteria types contains elements that are not a number')
            except:
                raise ValueError('Criteria types contains elements that are not a number')

            try:
                Files.__validate_input_data(matrix, extension, criteria_types)
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
                raise ValueError('Not all required keys were in file')

            matrix = data['matrix']
            try:
                matrix = np.array(matrix)
            except:
                raise ValueError('Error in matrix during converting data')
            
            criteria_types = data['criteriaTypes']
            try:
                criteria_types = np.array(criteria_types)
            except:
                raise ValueError('Error in criteria types during converting data')

            try:
                Files.__validate_input_data(matrix, extension, criteria_types)
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
                raise ValueError('Not all required keys were in file')

            matrix = data['matrix']
            try:
                matrix = np.array(matrix)
            except:
                raise ValueError('Error in matrix during converting data')
            
            criteria_types = data['criteriaTypes']
            try:
                criteria_types = np.array(criteria_types)
            except:
                raise ValueError('Error in criteria types during converting data')

            try:
                Files.__validate_input_data(matrix, extension, criteria_types)
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
            
            raise ValueError('Wrong file type')

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
            raise ValueError('Wrong file type')
        else:
            raise ValueError('Wrong data type extension')
            