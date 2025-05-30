from doctomarkdown.utils.prompts import docx_to_markdown_system_role_prompt,html_to_markdown_system_role_prompt
import logging
logger = logging.getLogger(__name__)
def handleException(max_retry, fun,fallback_fun, **kwargs):
    retries_left = max_retry if max_retry else 0
    try:
        if kwargs.get("context") == "pdf":
            return fun(
                llm_client=kwargs.get("llm_client"),
                llm_model=kwargs.get("llm_model"),
                base64_image=kwargs.get("base64_image")
            )
        elif kwargs.get("context") == "docx":
            return fun(
                llm_client=kwargs.get("llm_client"),
                llm_model=kwargs.get("llm_model"),
                system_prompt=docx_to_markdown_system_role_prompt(),
                raw_text=kwargs.get("raw_text")
            )
        elif kwargs.get("context") == "url":
            return fun(
                llm_client=kwargs.get("llm_client"),
                llm_model=kwargs.get("llm_model"),
                system_prompt=html_to_markdown_system_role_prompt(),
                raw_text=kwargs.get("content")
            )

    except Exception as e:
        logger.warning(f"Extraction failed retry left over exception {e} : {retries_left}")
        if retries_left > 0:
            return handleException(max_retry=retries_left - 1, fun=fun, fallback_fun=fallback_fun,  **kwargs)
        else:
            if fallback_fun:
                logger.warning('Fall back to the fallback function')
                if kwargs.get("context") == "pdf":
                    return fallback_fun(kwargs.get("pix"))
                elif kwargs.get("context") == "docx":
                    return fallback_fun(kwargs.get("raw_text"))
                elif kwargs.get("context") == "url":
                    return fallback_fun(kwargs.get("content"))
            raise Exception("Unable to extract using LLM after max retries") from e
