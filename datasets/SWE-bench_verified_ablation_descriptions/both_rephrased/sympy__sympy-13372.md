UnboundLocalError in evalf

When you multiply x by Max(0, y) with evaluation turned off and then call the numerical evaluation method, it simply returns x*Max(0, y). If you instead place Max(0, y) before x in the multiplication and then invoke the same numerical evaluation, the process fails with an UnboundLocalError because an internal precision variable was never initialized.

I found this after changing the order of Mul args in https://github.com/sympy/sympy/pull/13059.

Based on the code, I think the elif clauses that define reprec and imprec should have an `else: raise NotImplementedError`. That appears to fix it, although I didn't try to debug to see why the arg order is mattering here.