from rest_framework.filters import SearchFilter

class QTextSearchFilter(SearchFilter):
    search_param = "q"