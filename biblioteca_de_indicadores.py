import wbdata

# Listar todos os indicadores disponíveis
indicadores = wbdata.get_indicators()

# Exibir os códigos e os nomes dos indicadores
for indicador in indicadores:
    print(f"{indicador['id']}: {indicador['name']}")
