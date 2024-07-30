from pymongo import MongoClient

from utils.errors import get_error_message

class MongoDB:
    def __init__(self, uri, name):
        """
        Initializes the MongoDB connection.

        Parameters
        ----------
        uri : str
            The URI for connecting to MongoDB.
        name : str
            The name of the database.
        
        Raises
        ------
        ConnectionError
            If the connection to the MongoDB server fails.
        """
        self.__client = None
        self.__name = name
        try:
            self.__client = MongoClient(uri)
        except:
            raise ConnectionError(get_error_message('en', 'db-connection'))
    
    def __del__(self):
        """
        Closes the MongoDB client connection when the object is deleted.
        """
        if self.__client:
            self.__client.close()

    def get_db(self):
        """
        Retrieves the MongoDB client instance.

        Returns
        -------
        MongoClient
            The MongoDB client instance.
        """
        return self.__client

    def get_collection(self, collection_name):
        """
        Retrieves a collection from the database.

        Parameters
        ----------
        collection_name : str
            The name of the collection to retrieve.

        Returns
        -------
        Collection
            The MongoDB collection instance.

        Raises
        ------
        ConnectionError
            If the collection name is invalid or the collection cannot be retrieved.
        """
        try:
            collection = self.__client[self.__name][collection_name]
            return collection
        except:
            raise ConnectionError(f'{get_error_message("en", "db-collection-name")} {collection_name}')

    def get_usage_survey_results(self):
        """
        Retrieves usage survey results from the 'surveys' collection.

        Returns
        -------
        list
            A list of dictionaries containing the survey results.
        """
        collection = self.get_collection('surveys')
        cursor = collection.find({})

        return [{"id": idx, "option": item['option'], "name": item['name']} for idx, item in enumerate(list(cursor)) if "option" in list(item.keys())]

    def add_usage_survey_item(self, option, name):
        """
        Adds a usage survey item to the 'surveys' collection.

        Parameters
        ----------
        option : str
            The survey option.
        name : str
            The name of the respondent.

        Returns
        -------
        str
            Success message if the item is added successfully.

        Raises
        ------
        ConnectionError
            If there is an error adding the item to the collection.
        """
        collection = self.get_collection('surveys')
        item = { "option": option, "name": name }

        try:
            collection.insert_one(item)
            return 'Success'
        except:
            raise ConnectionError(get_error_message("en", "db-add-error"))

    def get_rating_survey_results(self):
        """
        Retrieves rating survey results from the 'ratings' collection.

        Returns
        -------
        list
            A list of dictionaries containing the rating survey results.
        """
        collection = self.get_collection('ratings')
        cursor = collection.find({})
        
        return [{
                "id": idx, 
                "helpful": item['helpful'],
                "easyInterface": item['easyInterface'],
                "changeSuggestion": item['changeSuggestion'],
                "easeOfUse": item['easeOfUse'],
                "overallRating": item['overallRating'],
                "features": item['features'],
            } 
            for idx, item in enumerate(list(cursor))
            ]

    def add_rating_survey_item(self, survey_item):
        """
        Adds a rating survey item to the 'ratings' collection.

        Parameters
        ----------
        survey_item : dict
            A dictionary containing the survey item data.

        Returns
        -------
        str
            Success message if the item is added successfully.

        Raises
        ------
        ConnectionError
            If there is an error adding the item to the collection.
        """
        collection = self.get_collection('ratings')

        try:
            collection.insert_one(survey_item)
            return 'Success'
        except:
            raise ConnectionError(get_error_message("en", "db-add-error"))
