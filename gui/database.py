from abc import ABC, abstractmethod
from typing import Any, Dict, List

from bson.objectid import ObjectId
from pymongo import MongoClient
from pymongo.collection import Collection


class IRepository(ABC):
    @abstractmethod
    def insert_one(self, item: Dict[str, Any]) -> ObjectId:
        pass

    @abstractmethod
    def update_one(self, object_id: str, new_item: Dict[str, Any]) -> int:
        pass

    @abstractmethod
    def delete_one(self, object_id: str) -> int:
        pass

    @abstractmethod
    def get_all_items(self) -> List[Dict[str, Any]]:
        pass


class MongoCollection(IRepository):
    def __init__(self, collection: Collection[Any]):
        self.collection: Collection[Any] = collection

    def insert_one(self, item: Dict[str, Any]) -> Any:
        result = self.collection.insert_one(item)
        return result.inserted_id

    def update_one(self, object_id: str, new_item: Dict[str, Any]) -> int:
        result = self.collection.update_one(
            {"_id": ObjectId(object_id)}, {"$set": new_item}
        )
        return result.modified_count

    def delete_one(self, object_id: str) -> int:
        result = self.collection.delete_one({"_id": ObjectId(object_id)})
        return result.deleted_count

    def get_all_items(self) -> List[Dict[str, Any]]:
        return list(self.collection.find())


class Database:
    _CONNECTION_STRING: str = (
        "mongodb+srv://hungdhv97:hung23081997@cluster0.pxjti4x.mongodb.net/"
    )

    def __init__(self, database_name: str):
        self.client: MongoClient[Any] = MongoClient(self._CONNECTION_STRING)
        self.database = self.client[database_name]

    def get_collection(self, collection_name: str) -> MongoCollection:
        return MongoCollection(self.database[collection_name])
