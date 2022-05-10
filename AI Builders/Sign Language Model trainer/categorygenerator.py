from filestoarray import fileToArray

filepath = "./data/identifiers/"

fta = fileToArray(filepath)

with open("categories.txt", "w") as file:
    for category in fta.all_categories:
        file.write("%s\n" % category)
    print("Done writing all categories to categories.txt")

