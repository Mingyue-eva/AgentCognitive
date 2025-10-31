Custom template tags raise TemplateSyntaxError when keyword-only arguments with defaults are provided.

Description

    (last modified by P-Seebauer)

If you define a simple_tag that only accepts a single keyword‐only parameter with a default value and no **kwargs, any attempt to pass that parameter in the template will fail. For example, you might register a tag called `hello` that takes a `greeting` argument defaulting to `"hello"`. When you invoke it in your template with `greeting="hi"`, you get:

    "'hello' received unexpected keyword argument 'greeting'"

Likewise, if you register a tag named `hi` that requires a `greeting` argument and then supply `greeting` twice in the same template call, you again see:

    "'hi' received unexpected keyword argument 'greeting'"

when the correct response should be:

    "'hi' received multiple values for keyword argument 'greeting'"

Inclusion tags behave the same way because they use the identical underlying code. I already have a fix ready and will push it as soon as I’ve created the ticket (I have a ticket# for the commit). This bug has existed in all versions since 2.0, because the offending line dates back that far.