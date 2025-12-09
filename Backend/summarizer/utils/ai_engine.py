from transformers import pipeline


def summarize_text(text, max_length=150, min_length=50):
    """
    Summarize text using facebook/bart-large-cnn model.
    
    Args:
        text (str): The text to summarize
        max_length (int): Maximum length of the summary
        min_length (int): Minimum length of the summary
    
    Returns:
        str: The summarized text
    """
    try:
        # Initialize the summarization pipeline with BART model
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        
        # BART has a max input length of 1024 tokens
        # Split text if it's too long
        max_chunk_length = 1024
        
        if len(text.split()) > max_chunk_length:
            # Split text into chunks
            words = text.split()
            chunks = [' '.join(words[i:i+max_chunk_length]) 
                     for i in range(0, len(words), max_chunk_length)]
            
            # Summarize each chunk
            summaries = []
            for chunk in chunks:
                summary = summarizer(chunk, 
                                   max_length=max_length, 
                                   min_length=min_length, 
                                   do_sample=False)
                summaries.append(summary[0]['summary_text'])
            
            # Combine summaries
            combined_summary = ' '.join(summaries)
            
            # If combined summary is still long, summarize again
            if len(combined_summary.split()) > max_length:
                final_summary = summarizer(combined_summary, 
                                          max_length=max_length, 
                                          min_length=min_length, 
                                          do_sample=False)
                return final_summary[0]['summary_text']
            
            return combined_summary
        else:
            # Summarize directly if text is short enough
            summary = summarizer(text, 
                               max_length=max_length, 
                               min_length=min_length, 
                               do_sample=False)
            return summary[0]['summary_text']
    
    except Exception as e:
        print(f"Error summarizing text: {e}")
        return None
