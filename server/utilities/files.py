import numpy as np
import json
import pandas as pd
import io
from base64 import encodebytes
from PIL import Image

from .validator import Validator
class Files():
    def __init__(self):
        pass

    @staticmethod
    def get_response_image(image_path):
        pil_img = Image.open(image_path, mode='r') # reads the PIL image
        byte_arr = io.BytesIO()
        pil_img.save(byte_arr, format='PNG') # convert the PIL image to byte array
        encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii') # encode as base64
        return encoded_img

    @staticmethod
    def __validate_input_data(matrix, extension, criteria_types):
        """
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
        """


        # TODO add checking if all rows have the same length
        def read_from_csv_crisp(file):
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
            