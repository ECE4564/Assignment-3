# Unit tests for MongoDB class

import MongoDB
import unittest


db1 = MongoDB.MongoDB()

# clear the database to remove duplicates
db1.clear_db()

test_post1 = {"Author": "Stephen King",
              "Name": "It"}

db1.insert(test_post1)

print(db1.find({"Author": "Stephen King"}))

db1.change_stock({"Name": "It"}, 6)

print('test find')
print(db1.find({"Name": "It", "Author": "Stephen King"}))

test_post2 = {"Author": "Herman Melville",
              "Name": "Moby Dick"}

res = db1.insert(test_post2)
print(res)
print(db1.find({"Name": "Moby Dick"}))

print("First list all")
temp_list = db1.list_all(1)
print(temp_list)

db1.remove({"Name": "It"})
res = db1.change_stock({"Name": "Moby Dick"}, None)
print(res)

print("Second list all")
temp_list = db1.list_all(0)
print(*temp_list, sep='\n')

print('print get stock:')
res = db1.get_stock({"Name": "Moby Dick"})
print(res)

res = db1.insert(test_post2)
print(res)