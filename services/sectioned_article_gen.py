from utils.prompt_loader import load_prompt
from utils.llm import call_openAI
import json

def generate_sectioned_article(outline: dict, model: str = "gpt-4.1-nano", model_summary: str = "gpt-4.1-nano") -> str:
    article = []
    outline = json.dumps(outline)
    print(len(outline))
    print(outline)
    
    style_anchors = [['Ik heb ontdekt dat ik in een flow kom als ik kennis kan doorgronden en delen met anderen.', 'Fysiek werkt het voor mij om me af te sluiten met mijn noise-cancelling koptelefoon en vertrouwde muziek.', 'Qua omstandigheden werkt het als ik niet veel kleine to do s heb, maar juist tijd heb geblokkeerd in mijn agenda.'], ['Niet alleen horen, kijken, analyseren en verwerken, maar ook door de vele stimuli op het scherm, jouw eigen verschijning en veel andere factoren, maken het voor jouw hersenen zwaar.', 'Met de stofkam door de eigen agenda gaan zorgde ervoor dat 30% van de videocalls zijn omgezet naar Slack of e-mail.', 'Onderzoek laat daarnaast zien dat het kijken naar jouw eigen emoties, zoals angst of verdriet, deze emoties zelfs nóg veel meer kan versterken.'], ['Ondanks het stijgende bereik van de campagnes, blijkt na een maand de interactie met de advertenties af te nemen.', 'Het creëren van de juiste campagne is dan ook een continu proces.', 'Blind varen op deze targeting is een groot risico, dus overweeg tevens een iets bredere insteek van de campagne.', 'De tactiek waarbij je targeting op 25-35 jaar is ingesteld heeft 20% meer klikken opgeleverd.', 'Vol adrenaline vertel je blij aan de stakeholders dat je experiment heeft gewerkt.']]


    for section in outline:
        article_text = "\n".join(article)
        article_summary = generate_summary(article_text, model=model_summary)
        #print(f"\n\nSummary: {article_summary} \n\n")
        print(section)
        last_paragraph = article[-1] if article else ""
        section_text = generate_section(
            summary=article_summary,
            section_outline=section,
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


    return "\n".join(article)

def generate_section(summary: str, section_outline: str, last_paragraph: str, style_anchors: str, full_outline: str , min_words: int, max_words: int, model: str = "gpt-4.1-nano") -> str:
    print("\n\n\nGenerating section...\n\n\n")
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
    #section_outline = json.loads(section_outline)

    # Load prompt
    replacements = {
        "[SUMMARY]": summary, #Summary up until this point
        "[SECTION-TITLE]": section_outline['title'], #Title of the section to be generated
        "[SECTION-DESCRIPTION]": section_outline['description'], #Description of the section to be generated
        "[SECTION-TYPE]": section_outline['type'], #Type of the section to be generated
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

def generate_summary(text: str, model: str = "gpt-4o-nano") -> str:
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
