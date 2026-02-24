# ai_translator.py

import logging
from transformers import MarianMTModel, MarianTokenizer

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Supported language pairs: display label -> (src_code, tgt_code)
# ---------------------------------------------------------------------------
SUPPORTED_PAIRS: dict[str, tuple[str, str]] = {
    "English → French":    ("en", "fr"),
    "English → German":    ("en", "de"),
    "English → Spanish":   ("en", "es"),
    "English → Hindi":     ("en", "hi"),
    "English → Italian":   ("en", "it"),
    "English → Dutch":     ("en", "nl"),
    "French → English":    ("fr", "en"),
    "German → English":    ("de", "en"),
    "Spanish → English":   ("es", "en"),
    "Hindi → English":     ("hi", "en"),
    "Italian → English":   ("it", "en"),
    "Dutch → English":     ("nl", "en"),
}

# Internal model cache so we never reload the same model twice in a session
_MODEL_CACHE: dict[str, tuple[MarianTokenizer, MarianMTModel]] = {}


def get_model_name(src: str, tgt: str) -> str:
    """
    Build the Helsinki-NLP model identifier for a given language pair.

    Args:
        src: BCP-47 source language code (e.g. 'en').
        tgt: BCP-47 target language code (e.g. 'fr').

    Returns:
        Hugging Face model hub path string.
    """
    return f"Helsinki-NLP/opus-mt-{src}-{tgt}"


def load_model(src: str, tgt: str) -> tuple[MarianTokenizer, MarianMTModel]:
    """
    Load (or retrieve from cache) the MarianMT tokenizer and model for the
    requested language pair.

    Models are stored in a module-level dict so repeated calls within the same
    Python process pay zero I/O overhead after the first load.

    Args:
        src: Source language code.
        tgt: Target language code.

    Returns:
        A (tokenizer, model) tuple ready for inference.

    Raises:
        OSError: If the model cannot be fetched from the Hugging Face hub.
        Exception: Re-raised for any unexpected failure during model init.
    """
    cache_key = f"{src}-{tgt}"

    if cache_key in _MODEL_CACHE:
        logger.info("Cache hit — reusing model for '%s'.", cache_key)
        return _MODEL_CACHE[cache_key]

    model_name = get_model_name(src, tgt)
    logger.info("Downloading / loading model: %s", model_name)

    try:
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
        model.eval()  # inference-only; disables dropout
    except OSError as exc:
        logger.error(
            "Model '%s' not found on the Hugging Face hub. "
            "Check that the language pair is supported.",
            model_name,
        )
        raise OSError(
            f"Could not load model '{model_name}'. "
            "Verify the language pair exists at https://huggingface.co/Helsinki-NLP"
        ) from exc
    except Exception as exc:
        logger.error("Unexpected error while loading model: %s", exc)
        raise

    _MODEL_CACHE[cache_key] = (tokenizer, model)
    logger.info("Model '%s' loaded and cached successfully.", model_name)
    return tokenizer, model


def translate(
    text: str,
    src: str,
    tgt: str,
    max_input_tokens: int = 512,
) -> str:
    """
    Translate *text* from *src* language into *tgt* language using MarianMT.

    Long inputs are silently truncated to *max_input_tokens* tokens to stay
    within the model's positional-embedding limit (512 for most Marian models).

    Args:
        text:             The source string to translate.
        src:              Source language code (e.g. 'en').
        tgt:              Target language code (e.g. 'fr').
        max_input_tokens: Hard ceiling on tokenised input length.

    Returns:
        The translated string, or an empty string if *text* is blank.

    Raises:
        OSError:   Propagated from :func:`load_model` if the pair is invalid.
        Exception: Re-raised for any unexpected inference failure.
    """
    text = text.strip()
    if not text:
        return ""

    tokenizer, model = load_model(src, tgt)

    try:
        inputs = tokenizer(
            text,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=max_input_tokens,
        )

        if inputs["input_ids"].shape[1] == max_input_tokens:
            logger.warning(
                "Input was truncated to %d tokens. "
                "Consider splitting long texts for best quality.",
                max_input_tokens,
            )

        translated_tokens = model.generate(**inputs)
        result = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)
        return result[0]

    except Exception as exc:
        logger.error("Translation failed: %s", exc)
        raise


# ---------------------------------------------------------------------------
# Quick smoke-test — run directly: python ai_translator.py
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    TEST_CASES = [
        ("Hello, how are you today?",             "en", "fr"),
        ("The weather is beautiful this morning.", "en", "de"),
        ("I love building AI applications.",       "en", "es"),
        ("Hello, how are you?", "en", "hi"),
        ("Hello, how are you?", "en", "it"),
        ("Hello, how are you?", "en", "nl"),
        ("Hello, how are you?", "fr", "en"),
        ("Hello, how are you?", "de", "en"),
        ("Hello, how are you?", "hi", "en"),
        ("Hello, how are you?", "es", "en"),
        ("Hello, how are you?", "it", "en"),
        ("Hello, how are you?", "nl", "en"),
    ]

    print("\n" + "=" * 60)
    print("  MarianMT Translation Engine — Terminal Test")
    print("=" * 60)

    for source_text, src_lang, tgt_lang in TEST_CASES:
        print(f"\n[{src_lang.upper()} → {tgt_lang.upper()}]")
        print(f"  Source : {source_text}")
        try:
            output = translate(source_text, src_lang, tgt_lang)
            print(f"  Output : {output}")
        except OSError as e:
            print(f"  ERROR  : {e}")

    print("\n" + "=" * 60 + "\n")