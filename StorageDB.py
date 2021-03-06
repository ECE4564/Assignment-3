# MongoDB.py - Encapsulates MongoDB related functions for ECE 4564 Assignment 2
# MOST UP TO DATE VERSION

import pymongo
import pprint


class MongoDB:

    def __init__(self):
        # open default port and host (local client)
        self.client = pymongo.MongoClient()
        # generate book database
        self.db = self.client.db  # lazy initialisation
        self.collection = self.db.collection

    # inserts a new book into the database
    # requires full information in JSON format, automatically set stock value of 0
    def insert(self, new_book):
        # check if the book is already in the database
        try:
            new_book['stock'] = 0
            post_id = self.collection.insert_one(new_book).inserted_id
        except:
            return {'Msg': 'Error: Unable to add. Book already exists'}
        return {'Msg': 'OK: Successfully inserted. Book id ' + str(post_id)}

    # query the database to find a book, search by title, author, or both
    def find(self, query):
        return str(self.collection.find_one(query))

    # list all books in the database, returns a list object containing JSON elements
    def list_all(self, list):
        # returns all posts in the db
        cursor = self.collection.find({})
        all_books = []
        for document in cursor:
            all_books.append(document)
        if list == 1:
            return {"Msg": "OK. Getting " + str(len(all_books)) + " books information", "Books": str(all_books)}
        else:
            return all_books

    # modify the stock of a given book
    # can search with title, author, or both
    # for a BUY request, stock_change should be positive
    # for a SELL request, stock_change should be negative
    def change_stock(self, book, stock_change):
        # self.collection.update_one(title, {'$set': {'Stock': new_stock}})
        try:
            print(str(book))
            found_book = self.collection.find_one(book)
            print(str(found_book))
            old_stock = found_book['stock']
            print(str(old_stock))
        except:
            return {'Msg': 'Error: Book doesn\'t exist. Please add book first'}
        if stock_change is None:
            return {'Msg': 'Error: No value was provided'}
        else:
            if old_stock + int(stock_change) > 0:  # ensure stock does not go below zero
                self.collection.update_one(book, {'$set': {'stock': old_stock + int(stock_change)}})
                return {'Msg': 'OK: ' + str(found_book) + 'Stock: ' + str(old_stock + int(stock_change))}
            else:
                return {'Msg': 'Error: Stock is not enough'}

    # remove a book from the database
    # returns a boolean if wanted
    def remove(self, book):
        result = self.collection.delete_one(book)
        if result.deleted_count == 1:
            return {'Msg': 'OK: Successfully deleted.'}
        else:
            return {'Msg': 'Book not found in database'}

    # clears the database, this can be used to remove duplicate objects in the database when testing
    def clear_db(self):
        self.db.drop_collection(self.collection)

    # returns the current stock of a book
    def get_stock(self, title):
        found_book = self.collection.find_one(title)
        return str(found_book['stock'])

    def get_count(self, book):
        try:
            found_book = self.collection.find_one(book)
            old_stock = found_book['stock']
        except:
            return {'Msg': 'Error: Book doesn\'t exist. Please add book first'}
        return {'Msg': 'OK: ' + str(old_stock) + ' books in stock'}
