from taquin_viewer import TaquinViewerHTML
from state import State
from state import Directions
from copy import deepcopy

""" This function searches the solution of the game of taquin, using the depth search first method.
    Returns a list of the successives states to follow to solve the taquin."""
def search_depth(init):
    frontiere = [init]
    history = []

    while frontiere:
        etat = frontiere.pop()
        history.append(etat)
        print("Element actuellement traité : ", etat)

        if etat.final():
            solution_path = []

            while not etat.parent is None:
                solution_path.insert(0, etat)
                etat = etat.parent

            return solution_path

        ops = etat.applicable_operations()
        for op in ops:
            new = etat.apply_operation(op)
            print(new, "  // ", op)

            if (new not in frontiere) and (new not in history) and (new.legal()):
                frontiere.append(new)

    return "Pas de solutions"

""" This function searches the solution of the game of taquin, using the width search first method.
    Returns a list of the successives states to follow to solve the taquin."""
def search_width(init):
    frontiere = [init]
    history = []

    while frontiere:
        etat = frontiere.pop()
        history.append(etat)
        # print("Element actuellement traité : ", etat)

        if etat.final():
            solution_path = []

            while not etat.parent is None:
                solution_path.insert(0, etat)
                etat = etat.parent

            return solution_path

        ops = etat.applicable_operations()
        for op in ops:
            new = etat.apply_operation(op)
            # print(new, "  // ", op)

            if (new not in frontiere) and (new not in history) and (new.legal()):
                frontiere.insert(0, new)

    return "Pas de solutions"

if __name__ == '__main__':
    origin = State( [[1, 2, 3],
                    [4, 0, 5],
                    [6, 7, 8]])

    print("Etat d'origine du taquin (0 represente le trou) : ", origin)
    print("Recherche d'une solution via la recherche récursive en profondeur...")

    history = search_width(origin)

    print("Mouvements determines via la recherche :")
    print("[%s]" % ", ".join(map(str, history)))
    print("Consultez le fichier solution.html pour voir les etapes successives pour la resolution.")

    #cette disposition prend trop de temps à résoudre, il faudrait en trouver une autre.
    #origin = State( [[1, 0, 2],
    #                 [3, 4, 5],
    #                 [6, 7, 8]])

    #history = search_depth(origin)

    with TaquinViewerHTML('solution.html') as viewer:
        viewer.add_taquin_state(origin, "position d'origine")

        for item in history:
            viewer.add_taquin_state(item, "mouvement")
