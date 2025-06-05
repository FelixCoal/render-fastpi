from utils.prompt_loader import load_prompt
from utils.llm import call_openAI
import json

def generate_sectioned_article(outline: str, style_anchors: list, model: str = "gpt-4.1-nano") -> str:
    article = []
    outline = json.loads(outline)
    print(len(outline))
    print(outline)

    for section in outline:
        article_text = "\n\n".join(article)
        article_summary = generate_summary(article_text, model=model)
        #print(f"\n\nSummary: {article_summary} \n\n")

        last_paragraph = article[-1] if article else ""
        section_outline = f"""
        Title: {section['title']}
        Description: {section['description']}
        """
        section_text = generate_section(
            summary=article_summary,
            section_outline=section_outline,
            last_paragraph=last_paragraph,
            style_anchors=style_anchors,
            full_outline=outline,
            min_words=section['min_word_count'],
            max_words=section['max_word_count'],
            model=model
        )

        # Append the generated section to the article
        to_add = f"""
        {section['title']}
        {section_text}
        """
        #print(f"\n\n New Section: {to_add} \n\n")
        article.append(to_add)


    return "\n\n".join(article)

def generate_section(summary: str, section_outline: str, last_paragraph: str, style_anchors: str, full_outline:str, min_words: int, max_words: int, model: str = "gpt-4.1-nano") -> str:
    """
    Generates a section of an article based on the provided outline and summary.

    Args:
        summary (str): The summary of the article.
        section_outline (str): The outline for the section to be generated.
        summarized_last_paragraph (str): The last paragraph of the previous section.
        model (str): The OpenAI model to use for generation.

    Returns:
        str: The generated section text.
    """
    # Load prompt
    replacements = {
        "[SUMMARY]": summary, #Summary up until this point
        "[SECTION-OUTLINE]": section_outline, #Outline of the section to be generated
        "[LAST_PARAGRAPH]": last_paragraph, #Last paragraph of the previous section\
        "[STYLE_ANCHORS]": style_anchors, #Style anchors
        "[ARTICLE_OUTLINE]" : full_outline,
        "[MIN_WORDS]" : min_words,
        "[MAX_WORDS]" : max_words

    }

    prompt = load_prompt(
        folder_path="prompts/sectioned_article_gen",
        replacements=replacements
    )

    #print(f"\n\n Prompt: {prompt}\n\n")

    # Call OpenAI API
    response = call_openAI(
        instructions=prompt,
        input=section_outline,
        model=model
    )

    return response

def generate_summary(text: str, model: str = "gpt-4.1-nano") -> str:
    """
    Generates a summary of the provided text.

    Args:
        text (str): The text to be summarized.
        model (str): The OpenAI model to use for generation.

    Returns:
        str: The generated summary.
    """
    # Load prompt
    replacements = {
        "[GEGENEREERDE_SECTIES_TOT_NU]": text
    }

    prompt = load_prompt(
        folder_path="prompts/sectioned_article_gen/summary_gen",
        replacements=replacements
    )

    # Call OpenAI API
    response = call_openAI(
        instructions=prompt,
        input=text,
        model=model
    )

    return response
