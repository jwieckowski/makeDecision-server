from pymongo import MongoClient

from utils.errors import get_error_message

class MongoDB:
    def __init__(self, uri, name):
        self.__client = None
        self.__name = name
        try:
            self.__client = MongoClient(uri)
        except:
            raise ConnectionError(get_error_message('en', 'db-connection'))
    
    def __del__(self):
        if self.__client:
            self.__client.close()

    def get_db(self):
        return self.__client

    def get_collection(self, collection_name):
        try:
            collection = self.__client[self.__name][collection_name]
            return collection
        except:
            raise ConnectionError(f'{get_error_message("en", "db-collection-name")} {collection_name}')

    def get_usage_survey_results(self):
        collection = self.get_collection('surveys')
        cursor = collection.find({})
         
        return [{"id": idx, "option": item['option'], "name": item['name']} for idx, item in enumerate(list(cursor)) if "option" in list(item.keys())]

    def add_usage_survey_item(self, option, name):
        collection = self.get_collection('surveys')
        item = { "option": option, "name": name }

        try:
            collection.insert_one(item)
            return 'Success'
        except:
            raise ConnectionError(get_error_message("en", "db-add-error"))

    def get_rating_survey_results(self):
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
        collection = self.get_collection('ratings')

        try:
            collection.insert_one(survey_item)
            return 'Success'
        except:
            raise ConnectionError(get_error_message("en", "db-add-error"))
