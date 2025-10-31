Q(...) & Exists(...) raises a TypeError

Exists(...) & Q(...) works, but Q(...) & Exists(...) raises a TypeError. The & (and |) operators should be commutative on Q-Exists pairs, but it’s not. I think there’s a missing definition of __rand__ somewhere.