Using exclude on annotated FilteredRelation doesn't work  
Description  

It looks like using exclude on queryset with annotated FilteredRelation give a FieldError on the annotation name.  
For exemple, in Django tests (django/tests/filtered_relation/tests.py) if we change this :  
def test_with_join(self):  
	self.assertSequenceEqual(  
		Author.objects.annotate(  
			book_alice=FilteredRelation('book', condition=Q(book__title__iexact='poem by alice')),  
		).filter(book_alice__isnull=False),  
		[self.author1]  
	)  
to this  
def test_with_join(self):  
	self.assertSequenceEqual(  
		Author.objects.annotate(  
			book_alice=FilteredRelation('book', condition=Q(book__title__iexact='poem by alice')),  
		).exclude(book_alice__isnull=False),  
		[]  
	)  
When running this, Django raises a FieldError because it cannot resolve the annotation name “book_alice.” The ORM reports that there is no field or relation by that name on Author and suggests the valid names: book, content_object, content_type, content_type_id, favorite_books, id, name, and object_id.  

As far as I understand, the function split_exclude(self, filter_expr, can_reuse, names_with_path) seams to be the faulty one. A new query is created without all extra datas from the original query.