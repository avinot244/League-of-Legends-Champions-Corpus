import transformers

def augment_data(text : str, 
                 pipeline_en_fr : transformers.pipelines.text2text_generation.TranslationPipeline, 
                 pipeline_fr_en : transformers.pipelines.text2text_generation.TranslationPipeline) -> None:


    text_fr = pipeline_en_fr(text)[0]['translation_text']
    text_en = pipeline_fr_en(text_fr)[0]['translation_text']
    return text_en
# del pipe
# torch.cuda.empty_cache()


