from cloudbot import hook
import unicodedata

@hook.command("u", "unicode")
def unicode(text):
    if text:
        
        name = ", ".join(["{}({})".format(unicodedata.name(character, "Unknown"), character) for character in text[:10]])
        return(name)
