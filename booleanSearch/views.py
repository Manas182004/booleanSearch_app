#booleanSearch/views.py



from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from .models import Candidate

@api_view(['POST'])
def boolean_search(request):
    """
    API endpoint to handle Boolean search queries.
    """
    data = request.data
    query = data.get("query", "")
    
    if not query:
        return Response({"error": "Query cannot be empty."}, status=400)

    try:
        # Parse the query and construct a Q object
        search_filter = parse_boolean_query(query)
        results = Candidate.objects.filter(search_filter).values_list("profile", flat=True)
        return Response({"results": list(results)})
    except Exception as e:
        return Response({"error": str(e)}, status=400)

def parse_boolean_query(query):
    """
    Parses a Boolean query string into a Django Q object.
    Supports AND, OR, NOT, parentheses, and quoted phrases.
    """
    import re
    tokens = re.findall(r'".+?"|\(|\)|\bAND\b|\bOR\b|\bNOT\b|[\w]+', query)
    
    stack = []
    current_query = Q()
    operator = None

    for token in tokens:
        token = token.strip()

        if token.upper() == "AND":
            operator = "AND"
        elif token.upper() == "OR":
            operator = "OR"
        elif token.upper() == "NOT":
            operator = "NOT"
        elif token == "(":
            # Push current state to stack and start a new group
            stack.append((current_query, operator))
            current_query = Q()
            operator = None
        elif token == ")":
            # Pop from stack and combine with the current query
            if not stack:
                raise ValueError("Unmatched parentheses in query.")
            previous_query, previous_operator = stack.pop()
            if previous_operator == "AND":
                current_query = previous_query & current_query
            elif previous_operator == "OR":
                current_query = previous_query | current_query
            elif previous_operator == "NOT":
                current_query = previous_query & ~current_query
        elif token.startswith('"') and token.endswith('"'):
            # Handle quoted phrases
            phrase = token[1:-1]
            condition = Q(profile__icontains=phrase)
            current_query = combine_queries(current_query, condition, operator)
        else:
            # Handle single keywords
            condition = Q(profile__icontains=token)
            current_query = combine_queries(current_query, condition, operator)
    
    # Ensure stack is empty (no unmatched parentheses)
    if stack:
        raise ValueError("Unmatched parentheses in query.")
    
    return current_query

def combine_queries(existing_query, new_condition, operator):
    """
    Combines an existing Q object with a new condition based on the operator.
    """
    if operator == "AND":
        return existing_query & new_condition
    elif operator == "OR":
        return existing_query | new_condition
    elif operator == "NOT":
        return existing_query & ~new_condition
    else:
        return new_condition