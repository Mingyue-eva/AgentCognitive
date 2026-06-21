Custom template tags raise TemplateSyntaxError when keyword-only arguments with defaults are provided.

Description

(last modified by P-Seebauer)

When creating simple tags with a keyword argument that has a default value, it is not possible to supply any other variable. Supplying a keyword argument a second time also produces an incorrect error message. The same issue occurs with inclusion tags. A fix is ready and will be pushed after creating the ticket; this issue has been present since version 2.0.