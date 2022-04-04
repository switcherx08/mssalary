books_dict = {}
counter = 1
def books_generate():
    global counter
    for books in range(5):
        books_dict[counter] = {'44':'55'}
        counter += 1
        print(books_dict)



books_generate()
