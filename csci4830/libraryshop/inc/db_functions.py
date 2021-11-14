from libraryshop.models import Book, BookCollectionMapping, Collection, BooksCollectionMapping


def get_books_in_collection(collection: Collection):
    bookmap = BookCollectionMapping.objects.filter(collection_id=collection.id)
    
def user_own_book(book: Book):
    if 
    

