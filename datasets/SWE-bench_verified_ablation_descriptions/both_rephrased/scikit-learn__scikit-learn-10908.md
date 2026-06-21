CountVectorizer's get_feature_names raise not NotFittedError when the vocabulary parameter is provided

If you create a CountVectorizer without supplying any vocabulary or fitting it on data, and then immediately call its transform method on a small set of text documents (for example, “This is the first document.”, “This is the second second document.”, “And the third one.”, “Is this the first document?”), it will raise a NotFittedError because no vocabulary has been learned.

On the other hand, if you initialize CountVectorizer with a predefined list of terms (for instance “and”, “document”, “first”, “is”, “one”, “second”, “the”, “third”, “this”), you might expect it to be ready for use right away. In fact, right after construction the internal vocabulary_ attribute does not exist, and calling get_feature_names at that point still triggers a NotFittedError. If you then transform the same collection of documents, the method succeeds and returns a sparse matrix with four rows and nine columns, and only after this transformation does the vocabulary_ attribute become available.

The `CountVectorizer`'s `transform` calls `_validate_vocabulary` method which sets the `vocabulary_` instance variable.

In the same manner I believe that the `get_feature_names` method should not raise `NotFittedError` if the vocabulary parameter is provided but the vectorizer has not been trained.