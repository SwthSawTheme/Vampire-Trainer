from pymem.process import *
from pymem import *
from builtins import open
import json


with open("settings.json", "r") as arquivo:
    data = json.load(arquivo)
    name = data["Gold"]["module"]

pm = Pymem("VampireSurvivors.exe")
module = module_from_name(pm.process_handle,name).lpBaseOfDll

def getPointer(base, offsets):
    # Lê o endereço base na memória do processo
    addr = pm.read_ulonglong(base)
    # Itera sobre os offsets fornecidos para calcular o endereço final
    for offset in offsets:
        if offset != offsets[-1]:  # Se não for o último offset, continua o cálculo
            addr = pm.read_ulonglong(addr + offset)
    # Adiciona o último offset para obter o endereço final
    addr += offsets[-1]
    return addr  # Retorna o endereço final calc



def injectGold(valor:float):
    enderecoG = int(data["Gold"]["endereco"], 16)
    offsets = [int(f"0x{offset}",16) for offset in data["Gold"]["offsets"]]
    return pm.write_float(getPointer(module + enderecoG, offsets),valor)


if __name__ == "__main__":
    print("Teste de Injeção!")
    while True:
        valor = float(input("Digite a quantidade de gold: "))
        injectGold(valor)
        print(f"Valor {valor} injetado!")