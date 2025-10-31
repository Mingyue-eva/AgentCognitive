physics.hep.kahane_simplify() incorrectly reverses order of leading uncontracted gamma matrices

The kahane_simplify() function applies identities such as γ^μ γ_μ = 4 I₄ to simplify products of gamma matrices in which contracted matrices occur. Leading gamma matrices without contractions should be unaffected, but a bug causes such leading terms to be prepended in reverse order.

To reproduce the problem, take a product of gamma matrices where a contracted pair appears at one end of the sequence and simplify it. For example, when simplifying γ^μ γ_μ γ^ρ γ^σ, the function correctly returns 4 γ^ρ γ^σ. However, if the contracted pair γ^μ γ_μ appears at the end of the product γ^ρ γ^σ γ^μ γ_μ, kahane_simplify() yields 4 γ^σ γ^ρ instead of the expected 4 γ^ρ γ^σ.

Because of this reversed ordering, an assertion that checks for equality with 4 γ^ρ γ^σ fails during testing, indicating that the simplification result does not match the expected sequence of uncontracted gamma matrices.

Both γ^μ γ_μ γ^ρ γ^σ and γ^ρ γ^σ γ^μ γ_μ should simplify to 4 γ^ρ γ^σ, but the order of γ^ρ and γ^σ is flipped in the second case due to the bug.

I found the source of the bug and it is simple to fix. In kahane_simplify() the leading matrices are removed at the beginning of the function and then inserted at the start of the product at the end of the function, and the insertion loop is just backward.

I'll generate a pull request for this shortly.