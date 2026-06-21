CountVectorizer's get_feature_names raise not NotFittedError when the vocabulary parameter is provided  
If you initialize a `CountVectorizer` and try to perform a transformation without training you will get a `NotFittedError` exception.

For example, you might import `CountVectorizer`, instantiate it with default settings, prepare a list of four short documents, and then call `transform` immediately:

NotFittedError: CountVectorizer - Vocabulary wasn't fitted.

On the other hand if you provide the `vocabulary` at the initialization of the vectorizer you could transform a corpus without a prior training, right?

Suppose you take the same four documents and define a fixed list of tokens as your vocabulary when creating the vectorizer. Before calling any methods, checking for the fitted vocabulary shows that `vocabulary_` is not set. If you then try to retrieve feature names, you still encounter:

NotFittedError: CountVectorizer - Vocabulary wasn't fitted.

Now, if you pass the document list to `transform`, it processes without error and returns:

<4x9 sparse matrix of type '<class 'numpy.int64'>'
        with 19 stored elements in Compressed Sparse Row format>

After this call, the vectorizer object gains the `vocabulary_` attribute.

In the same manner I believe that the `get_feature_names` method should not raise `NotFittedError` if the vocabulary parameter is provided but the vectorizer has not been trained.