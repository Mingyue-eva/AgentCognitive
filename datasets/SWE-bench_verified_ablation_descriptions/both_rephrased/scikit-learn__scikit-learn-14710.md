#### Description
The scorer used under the hood during early stopping is provided with `y_true` being integer while `y_pred` are original classes (i.e. string). We need to encode `y_true` each time that we want to compute the score.

#### Steps/Code to Reproduce
To reproduce the problem, generate a dataset of 100 samples with 10 numerical features each. Create a target array consisting of fifty `'x'` labels followed by fifty `'y'` labels. Instantiate a `HistGradientBoostingClassifier` configured to stop early if no improvement is seen after ten rounds, and then call its `fit` method on the generated features and string labels.

#### Expected Results
The model fitting process should complete normally without raising any exceptions.

#### Actual Results
When early stopping kicks in, the internal scoring function receives the true labels as integer codes while the predicted labels remain as the original strings. Because the scorer tries to compare these differently typed values, a type comparison error occurs and the training aborts.

#### Potential resolution

Maybe one solution would be to do:

```diff
--- a/sklearn/ensemble/_hist_gradient_boosting/gradient_boosting.py
+++ b/sklearn/ensemble/_hist_gradient_boosting/gradient_boosting.py
@@ -248,7 +248,6 @@ class BaseHistGradientBoosting(BaseEstimator, ABC):
                     (X_binned_small_train,
                      y_small_train) = self._get_small_trainset(
                         X_binned_train, y_train, self._small_trainset_seed)
-
                     self._check_early_stopping_scorer(
                         X_binned_small_train, y_small_train,
                         X_binned_val, y_val,
@@ -426,11 +425,15 @@ class BaseHistGradientBoosting(BaseEstimator, ABC):
 
         Scores are computed on validation data or on training data.
         """
+        if hasattr(self, 'classes_'):
+            y_small_train = self.classes_[y_small_train.astype(int)]
         self.train_score_.append(
             self.scorer_(self, X_binned_small_train, y_small_train)
         )
 
         if self._use_validation_data:
+            if hasattr(self, 'classes_'):
+                y_val = self.classes_[y_val.astype(int)]
             self.validation_score_.append(
                 self.scorer_(self, X_binned_val, y_val)
```