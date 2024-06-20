from django.shortcuts import render
from django.contrib import messages
from .read import  read_documents,read_doc_file
from .boolean_model import boolean_search
from .extended_boolean_model import extended_boolean_search
from .vectors_model import vecotr_search
def home(request):
    search_results = []
    content = ''

    if request.method == 'POST':
        search_input = request.POST.get('search-input', '').strip()
        search_option = request.POST.get('select-option', '').strip()

        if not search_input or not search_option:
            messages.error(request, 'Both search input and select option are required.')
            return render(request, 'index.html')

        try:
            search_results_str = ''
            if search_option == 'Boolean Model':
                search_results_str = boolean_search(search_input)
            elif search_option == 'Extended Boolean':
                search_results_str = extended_boolean_search(search_input)
            elif search_option == 'Vector Model':
                search_results_str = vecotr_search(search_input)

            if search_results_str:
                search_results = search_results_str
                documents = read_documents()  # Ensure documents are read and cached
                if search_results[0] in documents:
                    content = documents[search_results[0]]

        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')

    return render(request, 'index.html', {'search_results': search_results, 'CONT': content})

def read(request, pk):
    content = ''
    try:
        # Directly read the document from the path based on the primary key (pk) which is the filename
        content = read_doc_file(pk)
    except FileNotFoundError:
        messages.error(request, "Document not found.")
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')

    return render(request, 'content.html', {'CONT': content, 'pk': pk})