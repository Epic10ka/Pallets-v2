from rich import print
from rich.panel import Panel
from storage import messages
from storage import data
from time import sleep
from math import ceil


class Pallet:
    """
    Class to represent a pallet.

    - Add a name and quantity
    - Add quantity by rows and height
    """


    def __init__(self, typ, qtd = 0): #Type is name (Chep, broken, etc...)
        self.type = typ
        self.quantity = qtd


    # [ROWxHEIGHT MENU] Add pallets counting by row and height
    def row_counting(self):

        print(Panel(f'   [ Fileira X Altura ]', title = self.type, width = 30))

        while True:

            row = input('N° de fileiras: ').strip()
            height = input('Altura: ').strip()

            # If user type a blank space, it'll leave the RxH menu
            if height == '' or row == '': break

            # Try to make it an int number
            try:
                row = int(row)
                height = int(height)

            except ValueError:
                messages.error_message('NÚMERO INVÁLIDO')
                continue

            qtd = row * height

            print(f'[green1]+{qtd}[/]\n')
            self.quantity += qtd
        print(f'\ntotal {self.type}: {self.quantity}\n')
        return self.quantity


    # [INDIVIDUAL MENU] Add pallets individually
    def individual_counting(self):

        print(Panel(f'   [ Avulso ]', title = self.type, width = 20))

        while True:

            qtd = input('Quantidade: ').strip()

            if qtd == '': break #Again, checking if user types a blank space, if so, it'll leave the individual counting

            try:
                qtd = int(qtd)

                if qtd < 0:
                    print(f'[red]{qtd}[/]\n')
                else:
                    print(f'[green1]+{qtd}[/]\n')

            except ValueError:
                messages.error_message('NÚMERO INVÁLIDO')
                continue

            self.quantity += qtd
        print(f'\ntotal {self.type}: [green]{self.quantity}[/]\n')


    def dispatcher(self):
        while True:
            print(Panel.fit('[A] FILEIRA x ALTURA \n[B] AVULSO', title=self.type))
            opt = input(' > ').strip().upper()

            if opt == '':
                break

            if opt == 'A':
                sleep(0.2)
                self.row_counting()

            elif opt == 'B':
                sleep(0.2)
                self.individual_counting()


    def to_dict(self):
        return {

            'type': self.type,
            'quantity': self.quantity
        }


    @classmethod
    def from_dict(cls, data_l, default_type):
        return cls(
            data_l.get("type", default_type),
            data_l.get("quantity", 0)
        )


def slip_sheet():

    total = 0
    print(Panel.fit('[ SLIP SHEET ]'))

    while True:

        val = input(' > ').strip()
        if val == '':
            break

        try:
            val = float(val)
        except ValueError:
            messages.error_message('NÚMERO INVÁLIDO')
            continue

        qtd = val*25

        print(f'[green1]{val}*25[/]\n+')
        total += qtd

    print(f'TOTAL SESSÃO: {total}')
    return total


def summary(slip, quebrado, fumigado, chep):

    texto = (f'SLIP SHEET: {slip}\n'
             f'QUEBRADOS: {quebrado}\n'
             f'FUMIGADO: {fumigado}\n'
             f'CHEP: {chep}'
    )


    print(Panel(texto, title= 'RESUMO', width = 30))


def main_menu():
    dados = data.data_load()

    pallet_chep = Pallet(
        "CHEP",
        dados.get("chep", {}).get("quantity", 0)
    )

    pallet_quebrados = Pallet(
        "QUEBRADOS",
        dados.get("quebrados", {}).get("quantity", 0)
    )

    pallet_fumigado = Pallet(
        "FUMIGADO",
        dados.get("fumigados", {}).get("quantity", 0)
    )

    slip_sheet_qty = dados.get("slip_shit", 0)


    content = '\n[bright_white]      [1]CHEP\n      [2]QUEBRADOS\n      [3]FUMIGADO\n      [4]SLIP SHEET\n     -------------\n      [5]RESUMO\n      [/][[red]6[/]]RESETAR\n      [bright_white][0]AJUDA[/]'

    while True:

        print(Panel(content, title = '[blue]Super Frio[/]', width = 30))

        opt = input(' > ').strip().upper()

        match opt:

            case '1' | 'CHEP':
                pallet_chep.dispatcher()

            case '2' | 'QUEBRADOS':
                pallet_quebrados.dispatcher()

            case '3' | 'FUMIGADO':
                pallet_fumigado.dispatcher()

            case '4' | 'SLIP SHEET':
                slip_sheet_qty = slip_sheet()

            case '5' | 'RESUMO':
                while True:
                    summary(slip_sheet_qty, pallet_quebrados.quantity,
                            pallet_fumigado.quantity, pallet_chep.quantity)

                    wait = input(' > ').strip()

                    if wait == '': break


            case '6' | 'RESETAR':
                while True:
                    ask = input('RESETAR DADOS?: ').strip().upper()

                    if ask =='': break

                    if ask [0]== 'S':
                        pallet_chep = Pallet("CHEP", 0)
                        pallet_quebrados = Pallet("QUEBRADOS", 0)
                        pallet_fumigado = Pallet("FUMIGADO", 0)
                        slip_sheet_qty = 0
                        sleep(0.2)
                        print(f'[green1]Contagens resetadas[/]')
                        sleep(0.8)

                        data.data_save({
                            "chep": pallet_chep.to_dict(),
                            "quebrados": pallet_quebrados.to_dict(),
                            "fumigado": pallet_fumigado.to_dict(),
                            "slip_sheet": slip_sheet_qty
                        })
                        break

                    elif ask[0] == 'N':
                        break

                    else:
                        messages.error_message('OPÇÃO INVÁLIDA')

            case '0' | 'AJUDA':
                while True:

                    content1 = '[bright_white]VOLTAR - ENTER EM BRANCO\n\nSALVAMENTO - APÓS ADD PALLETS, VOLTAR (ENTER EM BRANCO)\n\n[red]RESETAR[/] - RESETA TODAS AS CONTAGENS'
                    print(Panel(content1, title='[yellow1]COMANDOS[/]', width=60))

                    back = input(' ').strip()

                    if back == '':break


        data_s = {
            'chep': pallet_chep.to_dict(),
            'quebrados': pallet_quebrados.to_dict(),
            'fumigados': pallet_fumigado.to_dict(),
            'slip_shit': slip_sheet_qty
        }

        data.data_save(data_s)

        sleep(0.2)
        print(f'[green1] Dados salvos com sucesso[/]\n')
        sleep(0.8)



if __name__ == '__main__':
    main_menu()