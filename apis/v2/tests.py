# a = {i: i**2 for i in range(10)}
# print(a)
find = 'Book222'
a = {1: {'id': 11,
         'title': 'Book111',
         'description': 'is good'
         },
     2: {'id': 22,
         'title': 'Book222',
         'description': 'is good'
         },
     3: {'id': 33,
         'title': 'Book333',
         'description': 'is good'
         }
     }
def findbook():
    finder = []
    for book in a.values():
        if book['title'] == find:
            finder.append(book)
    return finder


#print(findbook())




#print(abc(books_dict))


# def even(a):
#     return a % 2 == 0
# # a = filter(even, range(10))
# # print(list(a))
# # print(list(range(10)))
# def myfilter(func, a):
#     result = list()
#     for i in a:
#         if func(i):
#             result.append(i)
#     return result
#
# print(myfilter(even, range(10)))
# cond = even
# print(myfilter(cond, range(10)))
# cond2 = lambda x: x % 2 != 0
# print(myfilter(lambda x: x % 2 != 0, range(10)))
# print (cond2(7))

# import json
# a = list(range(10))
# print(json.dumps(a)[1:-1])

#Написать генератор, который преобразует словарь так, чтобы его ключ и значение поменялись местами, если значение имеет строковый тип, иначе — не вошли в новый словарь:
#{'a': 'b', 'c': 1, 'd': 'e', 'f': [2, 3]} —> {'b': 'a', 'e': 'd'}

dict1 = {'a': 'b',
         'c': 1,
         'd': 'e',
         'f': [2, 3]
         }
var = {v: k for k,v in dict1.items() if type(v) == str}
print(var)

#2. Написать генератор, который на основе списка формирует словарь, значения которого — порядковые индексы, а а значения — словарь с ключом 'value' и значением из исходного списка:

#[1, 'a', [2, 3, 4], {'b': 5}] —> {
#  0: {'value': 1},
#  1: {'value': 'a'},
#  2: {'value': [2, 3, 4]},
#  3: {'value': {'b': 5}}
#}

list2 = [1, 'a', [2, 3, 4], {'b': 5}]
dict2 = {}
def dict_creator():
    index_counter = 0
    for i in list2:
        dict2[(list2.index(i))] = {'value': list2[index_counter]}
        index_counter += 1
    print(dict2)
dict_creator()

