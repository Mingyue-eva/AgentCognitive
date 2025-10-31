Migrations uses value of enum object instead of its name.

Description  
(last modified by oasl)

When using an Enum object as a default value for a CharField, the generated migration file uses the value of the Enum object instead of its name. This causes a problem when using Django translation on the value of the Enum object. The problem is that, when the Enum object value gets translated into the user’s language, old migration files raise an error stating that the Enum does not have the corresponding value because the translated text no longer matches any member of the Enum.

To reproduce this issue, define an enumeration whose members use Django’s lazy translation for their values, then add a model with a CharField that defaults to one of those enum members. When you run makemigrations, Django will produce a migration that embeds the translated text into the default argument rather than referring to the enum member’s constant name. If you later switch the application to a different language and try to apply that migration again, the translated default string will not match any entry in the original Enum class, causing the migration to fail.

When you apply the migration in a locale where the enum value has been translated, Django raises a validation error indicating that the supplied default string is not a valid member of the Enum. In practice this appears as a ValueError complaining that the translated term is not a valid choice for the Status enum.

Shouldn’t the migration refer to the enum member by its constant name instead of its mutable translated value? In other words, it should record the default using the enum’s key (for example looking up Status['GOOD']) so that the migration remains valid regardless of how the text is translated.