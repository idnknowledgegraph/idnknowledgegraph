from django.http import JsonResponse
from .utils import run_query, run_update

def create_character(request, name):
    query = """
        PREFIX idn: <http://example.org/idn#>
        INSERT DATA {
            GRAPH <http://example.org/graph> {
                _:char a idn:Character ;
                idn:hasName "%s" .
            }
        }
    """ % name
    run_update(query)
    return JsonResponse({'name': name, 'message': 'Character created'})

def get_character(request, name):
    query = """
        PREFIX idn: <http://example.org/idn#>
        SELECT ?name WHERE {
            GRAPH <http://example.org/graph> {
                ?char a idn:Character;
                idn:hasName "%s" .
            }
        }
    """ % name
    results = run_query(query)
    try:
        character_name = results["results"]["bindings"][0]["name"]["value"]
        return JsonResponse({'name': character_name})
    except IndexError:
        return JsonResponse({'error': 'Character not found'}, status=404)

# Define additional CRUD operations similarly for other entities.

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .utils import run_update
import json

@csrf_exempt
@require_http_methods(["POST"])  # Ensure only POST requests are handled
def create_characters(request):
    try:
        # Load character names from POST request data
        data = json.loads(request.body)
        characters = data.get('characters', [])
        
        if not characters:
            return JsonResponse({'error': 'No characters provided'}, status=400)
        
        # Build the SPARQL INSERT DATA query for multiple characters
        insert_data = ' '.join([
            f'<http://example.org/characters/{char["name"]}> a <http://example.org/idn#Character> ; <http://example.org/idn#hasName> "{char["name"]}" .'
            for char in characters
        ])
        
        query = f"""
            PREFIX idn: <http://example.org/idn#>
            INSERT DATA {{
                GRAPH <http://example.org/graph> {{
                    {insert_data}
                }}
            }}
        """
        run_update(query)
        return JsonResponse({'message': f'Created {len(characters)} characters'})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)


