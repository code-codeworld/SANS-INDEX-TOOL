# SANS-INDEX-TOOL
This python script will index your SANS books to prepare for your exam.

You will need to modify your script for the instructor last and first names in line 13 of the script.

You will need to modify the script for the correct name of the pdf files of your SANS books.

There is a line in the script for Page Number Offset.  This may need to be adjusted based on the beginning of the content in the books. For example the slides in the books are not on the same page as the PDF file.  Once your index has been output to a csv file, you can search for any "page 0" and identify what the correct page number should be and conduct a "find and replace" pretty quickly.

If you prefer to attempt to remove the password from your book:
 Use the qpdf tool and this command: qpdf --password=enterpasswordhere -decrypt "InputFilename.pdf" "OutputFilename.pdf"
