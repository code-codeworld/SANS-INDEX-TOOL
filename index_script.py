import PyPDF2
import ssl
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from collections import defaultdict
from nltk.util import ngrams
import csv

# Disable SSL verification
ssl._create_default_https_context = ssl._create_unverified_context

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

# Define an extended list of stopwords Check the formating of the instructor name.
stopwords_list = set(stopwords.words('english')).union({
    "instructor last name", "instructor first name", "page"
})

# Function to process a PDF file
def process_pdf(pdf_file_path, password=None):
    with open(pdf_file_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        # Attempt to decrypt the PDF if it is encrypted
        if pdf_reader.is_encrypted:
            if password:
                pdf_reader.decrypt(password)
            else:
                raise ValueError(f"The PDF file {pdf_file_path} is encrypted but no password was provided.")
        
        # Iterate over each page in the PDF
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            
            if text:
                # Tokenize the text
                tokens = word_tokenize(text)
                
                # Filter out non-alphabetic tokens and stopwords, and convert to lowercase
                tokens = [token.lower() for token in tokens if token.isalpha() and token.lower() not in stopwords_list]
                
                # Perform Part-of-Speech tagging
                tagged_tokens = nltk.pos_tag(tokens)
                
                # Select nouns and proper nouns
                key_terms = [word for word, pos in tagged_tokens if pos in ('NN', 'NNS', 'NNP', 'NNPS')]
                
                # Calculate the frequency of each token
                fdist = FreqDist(key_terms)
                
                # Identify key terms based on frequency threshold (e.g., terms appearing more than once)
                frequent_terms = [word for word, freq in fdist.items() if freq > 1]
                
                # Adjust the page number for actual content
                actual_page_num = page_num + 1 - page_offset
                
                # Ensure the page number is not negative
                if actual_page_num > 0:
                    # Add the key terms to the index
                    for term in frequent_terms:
                        index[term].append((pdf_file_path, actual_page_num))
                    
                    # Generate bigrams and trigrams
                    bigrams = ngrams(tokens, 2)
                    trigrams = ngrams(tokens, 3)
                    
                    # Calculate the frequency of each n-gram
                    bigram_fdist = FreqDist(bigrams)
                    trigram_fdist = FreqDist(trigrams)
                    
                    # Identify frequent n-grams
                    frequent_bigrams = [' '.join(gram) for gram, freq in bigram_fdist.items() if freq > 1]
                    frequent_trigrams = [' '.join(gram) for gram, freq in trigram_fdist.items() if freq > 1]
                    
                    # Add the n-grams to the index
                    for bigram in frequent_bigrams:
                        index[bigram].append((pdf_file_path, actual_page_num))
                    
                    for trigram in frequent_trigrams:
                        index[trigram].append((pdf_file_path, actual_page_num))

# Load and process multiple PDF files
pdf_files = [
    ('Book1.pdf', 'bookpasswordgoeshere'),
    ('Book2.pdf', 'bookpasswordgoeshere'),  # Example of a password-protected PDF
    ('Book3.pdf', 'bookpasswordgoeshere'),
    ('Book4.pdf', 'bookpasswordgoeshere'),
    ('Book5.pdf', 'bookpasswordgoeshere')
]
index = defaultdict(list)

# Define the page offset.  This assumes the content you are indexing doesn't start on the very first page of the PDF.
page_offset = 2

for pdf_file_path, password in pdf_files:
    process_pdf(pdf_file_path, password)

# Write the index to a CSV file
with open('index2.csv', 'w', newline='') as csvfile:
    fieldnames = ['Term', 'Occurrences']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for term, occurrences in sorted(index.items()):
        occurrences_str = '; '.join([f"{pdf} (page {page})" for pdf, page in occurrences])
        writer.writerow({'Term': term, 'Occurrences': occurrences_str})
