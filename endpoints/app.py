import sys
import os
import requests
# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, jsonify
from flasgger import Swagger, swag_from
from models.pokemon_model import Pokemon


app = Flask(__name__)
swagger = Swagger(app)

# Define uma rota para o endpoint '/pokemon/<pokemon_name>' com o método HTTP GET
@app.route('/pokemon/<pokemon_name>', methods=['GET'])
@swag_from('swagger_config.yml')
def get_pokemon_info(pokemon_name):
    # Constrói a URL da API do Pokémon usando o nome do Pokémon fornecido na URL
    api_url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}'

    # Tenta fazer uma requisição GET à API do Pokémon
    try:
        # Realiza a requisição GET
        response = requests.get(api_url)
        # Lança uma exceção se a resposta HTTP indicar um erro (código 4xx ou 5xx)
        response.raise_for_status()
        # Converte a resposta JSON da API para um objeto Python
        data = response.json()

        # Cria uma instância do modelo Pokemon com base nos dados da API
        pokemon = Pokemon(name=data['name'], height=data['height'], weight=data['weight'])

        # Retorna a resposta JSON para o cliente
        return jsonify({'name': pokemon.name, 'height': pokemon.height, 'weight': pokemon.weight})

    # Captura exceções relacionadas a erros HTTP (códigos de status 4xx e 5xx)
    except requests.exceptions.HTTPError as errh:
        # Retorna uma mensagem de erro JSON
        return jsonify({'error': f'HTTP Error: {errh}'}), 404
    
    # Captura exceções gerais de requisição
    except requests.exceptions.RequestException as err:
        # Retorna uma mensagem de erro JSON
        return jsonify({'error': f'Request Exception: {err}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
