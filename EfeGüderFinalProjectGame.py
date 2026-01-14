import random

# Resets the game data when starting or replaying
def resetGame():
    return {
        "place": "desert",
        "bag": ["notebook"],
        "hp": 100,
        "alive": True
    }

# Player data
playerData = resetGame()

# Map connections between locations
locs = {
    "desert": ["village"],
    "village": ["desert", "pyramid"],
    "pyramid": ["village", "ancient ruin"],
    "ancient ruin": ["pyramid", "portal"],
    "portal": ["ancient ruin"]
}

# Descriptions of each location
desc = {
    "desert": "a desolate desert where no living thing lives.",
    "village": "a village where people used to live.",
    "pyramid": "a giant pyramid with treasure at its top.",
    "ancient ruin": "ancient ruins that prove the existence of mummies.",
    "portal": "a portal that teleports you to a biome where life exists."
}

# Puzzle and story flags
pz = {
    "village": False,
    "pyramid": False,
    "ancientruin": False,
    "mummy_dead": False,
    "notebook_used": False
}

print("\nWelcome to the game where you'll be searching in the desert. Here you have two objectives: first, find the portal that teleports you to a biome where life exists; and second, find the ancient artifacts that prove the existence of mummies.")

# Shows current location and possible paths
def showPlace():
    print("\nLocation:", playerData["place"])
    print(desc[playerData["place"]])
    print("You can go:", locs[playerData["place"]])

# Shows player inventory
def showBag():
    print("Bag:", playerData["bag"])

# Shows player health
def showStatus():
    print("HP:", playerData["hp"])

# Village puzzle where player chooses to open a box or not
def villagePuzzle():
    answer = input("\nThere's a box in front of you, would you like to open it?\nyes or no? :")

    if answer == "yes":
        print("\nA spider came out of the box and attacked you.")
        playerData["hp"] -= 25
        print("You lost 25 HP")

        if playerData["hp"] <= 0:
            playerData["alive"] = False
            return

        print("\nYou left there, explored the village, and found a map showing the inside of the pyramid and the key to the ancient ruins chamber.")
        playerData["bag"].append("key")
        playerData["bag"].append("map")
        pz["village"] = True

    elif answer == "no":
        print("\nYou decided not to open the box and instead began searching the village. Then you found the key to the room containing the ancient ruins and a map describing the inside of the pyramid.")
        playerData["bag"].append("key")
        playerData["bag"].append("map")
        pz["village"] = True

    else:
        print("Invalid choice.")

# Pyramid puzzle that forces the player to use the map
def pyramidPuzzle():
    no_count = 0

    while not pz["pyramid"] and playerData["alive"]:
        answer = input("Would you like to explore the inside using the map?\nyes or no? :")

        if answer == "yes":
            print("You use the map and start researching the inside of the pyramid.")
            if "map" in playerData["bag"]:
                playerData["bag"].remove("map")
            pz["pyramid"] = True

        elif answer == "no":
            no_count += 1
            if no_count >= 3:
                print("You finally decide to use the map.")
                if "map" in playerData["bag"]:
                    playerData["bag"].remove("map")
                pz["pyramid"] = True
            else:
                print("You decide not to use the map yet.")

        else:
            print("Invalid choice.")

# Combat system with the mummy
def mummyCombat():
    print("The mummy attacks you!")

    choice = input("Do you want to kill it using the key or run away?\nkill or run? :")

    if choice == "kill":
        if "key" in playerData["bag"]:
            print("You killed the mummy with the key and took the flintstone that fell from it.")
            playerData["bag"].append("flintstone")
            pz["mummy_dead"] = True
        else:
            dmg = random.randint(10, 20)
            playerData["hp"] -= dmg
            print("You lost", dmg, "HP")

    elif choice == "run":
        dmg = random.randint(40, 50)
        playerData["hp"] -= dmg
        print("You escaped from the mummy but lost", dmg, "HP")

    if playerData["hp"] <= 0:
        playerData["alive"] = False

# Ancient ruin puzzle and notebook usage
def ancientruinPuzzle():
    if "key" in playerData["bag"]:
        if not pz["notebook_used"]:
            answer = input("\nYou unlocked the door with the key and saw evidence of mummies from the past on the walls. Would you like to draw it in your notebook?\nyes or no? :")
            pz["notebook_used"] = True
            if answer == "yes":
                print("\nYou drew the findings in your notebook.")

        if not pz["mummy_dead"]:
            mummyCombat()

        if pz["mummy_dead"]:
            pz["ancientruin"] = True
    else:
        print("\nYou don't have the key. Find the key.")

# Final room where the game can end
def portalRoom():
    code = input("\nDo you want to stay here, or do you want to escape using the flintstone?\nescape or stay? :")

    if code == "escape" and "flintstone" in playerData["bag"]:
        print("\nCongratulations, you managed to escape the arid desert! Now you can tell the people in this biome about what you saw and experienced.")
        playerData["bag"].remove("flintstone")
    elif code == "stay":
        print("\nStaying was an option; I suppose you'll continue your research in the desert.")
    else:
        print("\nYou didn't notice the mummies approaching from behind and you died :(")

    playerData["alive"] = False

# Main game loop
while True:
    while playerData["alive"]:
        showPlace()
        showBag()
        showStatus()

        cmd = input("\nCommand (go/status/quit): ")

        if cmd == "go":
            where = input("Where?: ")

            if where in locs[playerData["place"]]:
                playerData["place"] = where

                if where == "village" and not pz["village"]:
                    villagePuzzle()

                if where == "pyramid" and not pz["pyramid"]:
                    pyramidPuzzle()

                if where == "ancient ruin" and not pz["ancientruin"]:
                    ancientruinPuzzle()

                if where == "portal":
                    if "flintstone" in playerData["bag"]:
                        portalRoom()
                    else:
                        print("\nYou feel like you're missing something important.")
            else:
                print("There's no such place, try somewhere else.")

        elif cmd == "status":
            showStatus()

        elif cmd == "quit":
            playerData["alive"] = False

    # Restart option
    again = input("\nGame over! Do you want to play again? yes or no? :")
    if again == "yes":
        playerData = resetGame()
        pz = {
            "village": False,
            "pyramid": False,
            "ancientruin": False,
            "mummy_dead": False,
            "notebook_used": False
        }
    else:
        break
