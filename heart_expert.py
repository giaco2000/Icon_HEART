from typing_extensions import Self
from experta import *
from colorama import Fore


def chiedi_domanda(domanda: str):
    print(domanda) 
    flag = False
    while(not(flag)):
        userInput = ''
        userInput = input(" ==> ")
        try:
            risposta = int(userInput)
            if(risposta < 1 or risposta > 2):
                raise Exception()
            flag = True
        except (ValueError, Exception) as ex:
            print("Errore! Risposta non valida. La risposta deve essere un INTERO compreso tra 1 e 3\n")
    return risposta

def menu(title: str, options: list[str]) -> int:
    response = 0
    while response == 0:
        print(title + ":")
        i = 1
        for option in options:
            print(str(i) + ") " + option)
            i = i + 1
        response = int(input("Seleziona il numero della scelta: "))
        if (response < 1) or (response > len(options)): response = 0

    return response

def user(): input("Premi un pulsante qualsiasi per continuare...")


def runex():
    engine = DiagnosticsES()
    engine.reset()
    engine.run()

class DiagnosticsES(KnowledgeEngine):

    @DefFacts()
    def _initial_action(self):
        yield Fact(domanda=True)
        yield Fact(ordineDomande=1)
    
    
    # SINTOMI COMUNI DI ARRESTO CARDIACO E INSUFFICIENZA CARDIACA
    # RESPIRO CORTO E DOLORE AL TORACE

    @Rule(AND(Fact(domanda=True),Fact(ordineDomande=1)))
    def chiedi_respiro_corto(self):
        self.declare(Fact(respiro_corto=chiedi_domanda("Quando svolgi un movimento, hai il respiro corto?\n\t(1) si\n\t(2) no")))
        self.declare(Fact(ordineDomande=2))


    @Rule(AND(Fact(domanda=True),Fact(ordineDomande=2)))
    def chiedi_affaticamento(self):
        self.declare(Fact(affaticamento=chiedi_domanda("Avverti un senso di affaticamento?\n\t(1) si\n\t(2) no")))
        self.declare(Fact(ordineDomande=3))

    @Rule(AND(Fact(domanda=True),Fact(ordineDomande=3)))
    def chiedi_dft(self):
        self.declare(Fact(dft=chiedi_domanda("Avverti un dolore o fastidio al torace?\n\t(1) si\n\t(2) no")))
        self.declare(Fact(ordineDomande=4))

   

    # PARTE RELATIVA AI PROBLEMI DI STOMACO

    @Rule(AND(Fact(domanda=True),Fact(ordineDomande=4)))
    def chiedi_problemi_stomaco(self):
        self.declare(Fact(problemi_stomaco=chiedi_domanda("Stai avendo problemi di stomaco?\n\t(1) si\n\t(2) no")))
        self.declare(Fact(ordineDomande=5))



    # PALPITAZIONI AL PETTO

    @Rule(AND(Fact(domanda=True),Fact(ordineDomande=5)))
    def chiedi_palpitazioni(self):
        self.declare(Fact(palpitazioni=chiedi_domanda("Avverti palpitazioni al petto?\n\t(1) si\n\t(2) no")))
        self.declare(Fact(ordineDomande=6))


    # GONFIORE PARTE INFERIORE DEL CORPO

    @Rule(AND(Fact(domanda=True),Fact(ordineDomande=6)))
    def chiedi_gonfiore(self):
        self.declare(Fact(gonfiore=chiedi_domanda("Noti rigonfiamenti nella parte inferiore del corpo?\n\t(1) si\n\t(2) no")))
        


    # REGOLE

    
    # 1-ARITMIA
    @Rule(AND(Fact(respiro_corto=2),Fact(affaticamento=2),
    Fact(dft=2),Fact(problemi_stomaco=2),Fact(palpitazioni=1),Fact(gonfiore=2)))
    def aritmia(self):
        self.declare(Fact(aritmia=True))
        print(Fore.GREEN + "Il sintomo indica che molto probabilmente sei affetto da ARITMIA.")
        print('\033[39m')

    @Rule(Fact(aritmia=True))
    def keep_calm(self):
        print(Fore.GREEN + "Contatta il tuo medico di base e stai tranquillo!")
        print('\033[39m')
        self.reset()


    # 2-ATTACCO CARDIACO
    @Rule(AND(Fact(respiro_corto=1),Fact(affaticamento=1),Fact(dft=1),
              Fact(problemi_stomaco=1),Fact(palpitazioni=2),Fact(gonfiore=2)))
    def attacco_cardiaco(self):
        self.declare(Fact(attacco_cardiaco=True))
        print(Fore.LIGHTBLUE_EX + "I sintomi indicano che potresti avere un ATTACCO CARDIACO.")
        print('\033[39m')

    @Rule(Fact(attacco_cardiaco=True))
    def call_118(self):
        print(Fore.LIGHTBLUE_EX + "Recati immediatamente presso un pronto soccorso o chiama il 118!")
        print('\033[39m')
        self.reset()


    # 3-PROBLEMA STOMACO, NO MALATTIE CARDIACHE
    @Rule(AND(OR(Fact(respiro_corto=1),Fact(respiro_corto=2)), 
              OR(Fact(affaticamento=1),Fact(affaticamento=2)),
              Fact(problemi_stomaco=1),Fact(dft=2)))
    def no_heart(self):
        self.declare(Fact(no_heart=True))
        print(Fore.CYAN + "Con i sintomi indicati non si tratterebbe di una possibile malattia cardiaca,")
        print('\033[39m')

    @Rule(Fact(no_heart=True))
    def stomach(self):
        print(Fore.CYAN + "ma bensì di un problema legato allo stomaco.Ti consiglio di effettuare una gastroscopia.")
        print('\033[39m')
        self.reset()


    # 4-ATTACCO DI PANICO
    @Rule(OR(Fact(respiro_corto=1),
          (AND(Fact(dft=1), Fact(respiro_corto=1)))))
    def attacco_di_panico(self):
        self.declare(Fact(attacco_di_panico=True))
        print(Fore.LIGHTYELLOW_EX + "I sintomi rivelano che stai avendo un ATTACCO DI PANICO.")
        print('\033[39m')
    
    @Rule(Fact(attacco_di_panico=True))
    def respira(self):
        print(Fore.LIGHTYELLOW_EX + "Inizia a respirare lentamente e chiedi aiuto.")
        print('\033[39m')
        self.reset()

    
    # 5-INSUFFICIENZA CARDIACA
    @Rule(AND(Fact(respiro_corto=1),Fact(affaticamento=1),Fact(gonfiore=1),Fact(problemi_stomaco=2),Fact(dft=2),
          OR(Fact(palpitazioni=1),Fact(palpitazioni=2))))
    def insufficienza_cardiaca(self):
        self.declare(Fact(insufficienza_cardiaca=True))
        print(Fore.LIGHTWHITE_EX + "I sintomi indicano una possibile INSUFFICIENZA CARDIACA.")
        print('\033[39m')

    @Rule(Fact(insufficienza_cardiaca=True))
    def immediate_assistance(self):
        print(Fore.LIGHTWHITE_EX + "Contatta il tuo medico di base e la guardia medica per ricevere assistenza immediata.")
        print('\033[39m')
        self.reset()

    
    # 6-NIENTE MALATTIA
    @Rule(OR(
          AND(Fact(affaticamento=2),Fact(dft=2),Fact(respiro_corto=2)),
          AND(Fact(affaticamento=1),Fact(dft=2),Fact(problemi_stomaco=2), OR(Fact(gonfiore=2),Fact(gonfiore=1))),
          AND(Fact(respiro_corto=1),Fact(dft=2),Fact(affaticamento=1),Fact(gonfiore=2),Fact(problemi_stomaco=2)),
          AND(Fact(problemi_stomaco=2),Fact(palpitazioni=2),Fact(gonfiore=2),Fact(respiro_corto=2),Fact(dft=2),Fact(affaticamento=2))
          ))
    def no_malattia(self):
        self.declare(Fact(no_malattia=True))
        print(Fore.LIGHTMAGENTA_EX + "L'assenza di sintomi rilevanti escludono una particolare malattia cardiaca.")
        print('\033[39m')

    @Rule(Fact(no_malattia=True))
    def no_sintomi(self):
        print(Fore.LIGHTMAGENTA_EX + "Se avverti altri sintomi riavvia il sistema di diagnostica.")
        print('\033[39m')
        self.reset()

    
    # 7-PROBLEMA CARDIACO GENERICO / PROBLEMA GENERALE
    @Rule(OR(Fact(dft=1),
    AND(Fact(respiro_corto=2),Fact(palpitazioni=1),Fact(affaticamento=2),Fact(dft=1),
    OR(Fact(gonfiore=1),Fact(gonfiore=2))),
    AND(Fact(respiro_corto=1),Fact(affaticamento=1),Fact(dft=1),Fact(problemi_stomaco=1),Fact(palpitazioni=1),Fact(gonfiore=1))))
    def problema_cardiaco_generico(self):
        self.declare(Fact(problema_cardiaco_generico=True))
        print(Fore.LIGHTRED_EX + "Potrebbe trattarsi di un problema cardiaco.")
        print('\033[39m')
    
    @Rule(Fact(problema_cardiaco_generico=True))
    def sii_specifico(self):
        print(Fore.LIGHTRED_EX + "Sii più specifico nel valutare i sintomi in modo tale da poter individuare la problematica, e nel frattempo consulta un medico.")
        print('\033[39m')
        self.reset()

    