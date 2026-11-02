from deep_translator import GoogleTranslator


def translate_text(text, target="en"):

    if text.strip() == "":
        return "Please enter some text."

    try:
        translated = GoogleTranslator(
            source='auto',
            target=target
        ).translate(text)

        return translated

    except Exception as e:
        return f"Error: {str(e)}"