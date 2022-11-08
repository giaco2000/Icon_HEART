from heart_expert import runex, menu, user
from heart_ontology import heart_ontology



def expert_system():
    print("===============================================================================")
    print("|Benvenuto nel sistema esperto di diagnostica delle malattie cardiache.       |")
    print("|                                                                             |")
    print("|Rispondi alle domande proposte dal sistema a seconda dei sintomi riscontrati.|")
    print("===============================================================================")
    runex()

def ontology():
    do = heart_ontology()

    do.get_symptoms_descriptions()
    symptoms, keys_symptoms = do.print_symptoms()

    print("\nSeleziona il sintomo di cui vuoi conosere la descrizione, inserisci il numero del sintomo")
    symptom_number = int(input())

    while symptom_number not in symptoms.keys():
        print("\nSeleziona il sintomo di cui vuoi conosere la descrizione, inserisci il numero del sintomo")
        symptom_number = int(input())
            
    print("Sintomo: %s, descrizione: %s"%(keys_symptoms[symptom_number]," ".join(symptoms[symptom_number])))

    

if __name__ == '__main__':
    title = "Modello da usare"
    options = [
        "Mostrare alcuni sintomi delle malattie cardiache",
        "Sistema esperto",
        "Esci"
    ]
    res = 0
    while res != 3:
        res = menu(title, options)
        if res == 1:
            ontology()
        if res == 2:
            expert_system()
            user()
        if res == 3:
            print("======================")
            print("|                    |")
            print("|                    |")
            print("|Programma terminato |")
            print("|                    |")
            print("|                    |")
            print("======================")
