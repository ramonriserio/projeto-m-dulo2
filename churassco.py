import requests

# Função que valida o CEP do churrasco
def validar_cep(cep):
    try:
        response = requests.get(f'https://cdn.apicep.com/file/apicep/{cep}.json', timeout = 5)

        # Gera uma exceção se a resposta contiver um código de status HTTP de erro
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        print(f'Erro ao fazer a solicação à API: {e}')
        return False, None
    
    data = response.json()
    if 'erro' not in data:
        return True, data
    else:
        return False, None
    
# Função que valida o CPF do usuário
def validar_cpf(cpf):
    try:
        # Remove caracteres não numéricos
        cpf = ''.join(filter(str.isdigit, cpf))

        # Verifica se o CPF tem 11 dígitos
        if len(cpf) != 11:
            return False
        
        # Calcula o primeiro dígito verificador
        soma = 0
        for digito, peso in zip(cpf[:9], range(10, 1, -1)):
            soma += int(digito) * peso
        resto = soma % 11
        digito1 = (11 - resto if 1 < resto < 10 else 0)

        # Calcula o segundo dídito verificador
        soma = 0
        for digito, peso in zip(cpf[:10], range(11, 1, -1)):
            soma += int(digito) * peso
        resto = soma % 11
        digito2 = (11 - resto if 1 < resto < 10 else 0)

    except ValueError:
        print("O CPF deve conter apenas números.")
        return False
    
    except Exception as e:
        print(f'Erro ao validar o CPF: {e}')
        return False
    
    return cpf[-2:] == f'{digito1}{digito2}'

# Calcula a quantidade de carne e de bebidas
def calcular_carne_bebidas(num_covidados):

    # Quantidade de carne por pessoa (em kg)
    carne_por_pessoa = 0.4

    # Quantidade de bebida alcoólica por pessoa (em litros)
    bebida_por_pessoa = 2

    # Calcula a quantidade total de carne e bebida
    total_carne = num_covidados * carne_por_pessoa
    total_bebida = num_covidados * bebida_por_pessoa

    return {'carne': total_carne, 'bebida': total_bebida}

# Coletar os dados para planejar o churrasco
def planejar_churrasco():
    cep = input("Insira o CEP onde os ingredientes serão entregues: ")
    valido, endereco_entrega = validar_cep(cep)
    if not valido:
        print('CEP inválido.')
        return
    
    cpf = input("Insira seu CPF: ")
    if not validar_cpf(cpf):
        print("CPF inválido.")
        return
    
    num_convidados = int(input("Insira o número de convidados: "))
    necessidades = calcular_carne_bebidas(num_convidados)
    
    print(f"Você vai precisar de {necessidades['carne']} kg de carne e {necessidades['bebida']} litros de bebida")
#    print("Opções de entrega disponíveis: ", ','.join(opcoes_entrega))
    print("a ser entregue no seguinte endereço: ")
    print(endereco_entrega)

# Programa principal
if __name__ == '__main__':
    planejar_churrasco()